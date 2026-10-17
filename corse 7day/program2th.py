import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROFILE_FILE = Path(__file__).with_name("chatbot_profile.json")
API_BASE_URL = os.environ.get(
	"CHATBOT_API_BASE_URL",
	"https://integrate.api.nvidia.com/v1/chat/completions",
)
MODEL = os.environ.get("CHATBOT_MODEL", "deepseek-ai/deepseek-v4.1-flash")
MAX_HISTORY_MESSAGES = 12

EMOTION_SCHEMA = {
	"type": "object",
	"properties": {
		"emotion": {
			"type": "string",
			"enum": [
				"neutral",
				"happy",
				"sad",
				"frustrated",
				"anxious",
				"confused",
				"excited",
				"other",
			],
		},
		"confidence": {
			"type": "string",
			"enum": ["low", "medium", "high"],
		},
		"reply": {"type": "string"},
	},
	"required": ["emotion", "confidence", "reply"],
	"additionalProperties": False,
}


def ask(prompt, default):
	answer = input("{} [{}]: ".format(prompt, default)).strip()
	return answer or default


def load_profile():
	if PROFILE_FILE.exists():
		try:
			with PROFILE_FILE.open("r", encoding="utf-8") as profile_file:
				profile = json.load(profile_file)
			if all(key in profile for key in ("name", "interests", "experience", "style")):
				return profile
		except (OSError, ValueError):
			pass

	print("Let's personalize your chatbot. These preferences are saved locally.")
	profile = {
		"name": ask("What should I call you?", "friend"),
		"interests": ask("What topics interest you?", "general topics"),
		"experience": ask("What is your experience level?", "not specified"),
		"style": ask("How should I respond?", "friendly and clear"),
	}
	save_profile(profile)
	return profile


def save_profile(profile):
	with PROFILE_FILE.open("w", encoding="utf-8") as profile_file:
		json.dump(profile, profile_file, indent=2, ensure_ascii=False)


def edit_profile(profile):
	print("Update any preference, or press Enter to keep its current value.")
	for key, prompt in (
		("name", "What should I call you?"),
		("interests", "What topics interest you?"),
		("experience", "What is your experience level?"),
		("style", "How should I respond?"),
	):
		profile[key] = ask(prompt, profile[key])
	save_profile(profile)
	print("Preferences saved.\n")


def make_instructions(profile):
	return """You are a thoughtful, conversational assistant speaking with {name}.
Personalize replies using these preferences:
- Interests: {interests}
- Experience level: {experience}
- Preferred response style: {style}

Infer only the apparent emotion expressed in the current message and context.
Emotion inference is uncertain: use neutral with low confidence when unclear.
Never diagnose the user or present an emotion as a fact. Adapt your tone gently,
but answer the user's actual question first and do not over-focus on emotion.
Do not claim to remember anything outside the supplied conversation and profile.
Return a JSON object with exactly these fields: emotion, confidence, and reply.
""".format(**profile)


def request_reply(api_key, instructions, history):
	messages = [{"role": "system", "content": instructions}] + history
	payload = {
		"model": MODEL,
		"messages": messages,
		"temperature": 1.0,
		"top_p": 0.95,
		"max_tokens": 262144,
		"stream": False,
	}
	for attempt_payload in (payload, {"model": MODEL, "messages": messages}):
		request = Request(
			API_BASE_URL,
			data=json.dumps(attempt_payload).encode("utf-8"),
			headers={
				"Authorization": "Bearer " + api_key,
				"Accept": "application/json",
				"Content-Type": "application/json",
			},
			method="POST",
		)
		try:
			with urlopen(request, timeout=60) as response:
				result = json.loads(response.read().decode("utf-8"))
			break
		except HTTPError as error:
			details = error.read().decode("utf-8", errors="replace")
			if error.code == 400 and attempt_payload is payload:
				continue
			raise RuntimeError("API returned HTTP {}: {}".format(error.code, details))
		except URLError as error:
			raise RuntimeError("Could not connect to the API: {}".format(error.reason))

	content = result["choices"][0]["message"]["content"]
	try:
		return json.loads(content)
	except (TypeError, ValueError):
		return {"reply": content, "emotion": "neutral", "confidence": "low"}


def list_provider_models(api_key):
	models_url = API_BASE_URL.rsplit("/chat/completions", 1)[0] + "/models"
	request = Request(
		models_url,
		headers={
			"Authorization": "Bearer " + api_key,
			"Accept": "application/json",
		},
		method="GET",
	)
	try:
		with urlopen(request, timeout=20) as response:
			result = json.loads(response.read().decode("utf-8"))
	except HTTPError as error:
		details = error.read().decode("utf-8", errors="replace")
		raise RuntimeError("API returned HTTP {}: {}".format(error.code, details))
	except URLError as error:
		raise RuntimeError("Could not connect to the API: {}".format(error.reason))

	return [item["id"] for item in result.get("data", []) if isinstance(item, dict) and isinstance(item.get("id"), str)]


def main():
	api_key = os.environ.get("CHATBOT_API_KEY") or os.environ.get("NVIDIA_API_KEY")
	if not api_key:
		print("Set NVIDIA_API_KEY or CHATBOT_API_KEY, then start this program again.")
		return

	profile = load_profile()
	instructions = make_instructions(profile)
	history = []

	print("\nHi, {}. Type /profile to update preferences or /quit to leave.\n".format(
		profile["name"]
	))

	while True:
		try:
			message = input("You: ").strip()
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye!")
			break

		if not message:
			continue
		if message.lower() in {"/quit", "quit", "exit", "bye"}:
			print("Bot: Goodbye, {}!".format(profile["name"]))
			break
		if message.lower() == "/profile":
			edit_profile(profile)
			instructions = make_instructions(profile)
			continue

		history.append({"role": "user", "content": message})
		history = history[-MAX_HISTORY_MESSAGES:]

		try:
			result = request_reply(api_key, instructions, history)
			emotion = result.get("emotion", "neutral")
			confidence = result.get("confidence", "low")
			reply = result.get("reply", "I couldn't form a response just now.")
			if not isinstance(reply, str):
				raise ValueError("The model returned an invalid reply.")
		except (RuntimeError, ValueError, TypeError, KeyError) as error:
			history.pop()
			print("Bot: I couldn't get a response just now: {}\n".format(error))
			continue

		print("Possible emotion: {} ({} confidence)".format(emotion, confidence))
		print("Bot: {}\n".format(reply))
		history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
	main()
