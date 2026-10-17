#pip install openai
#senv:OPENAI_API_KEY = "your-api-key"

#import json
#from openai import OpenAI

#client = OpenAI()

name = input("What should I call you? ").strip() or "there"
interests = input("What topics interest you? ").strip() or "general topics"
experience = input("Your experience level? ").strip() or "not specified"
style = input("How should I respond? (for example, concise or detailed) ").strip()
style = style or "friendly and clear"

instructions = f"""
You are a helpful chatbot speaking with {name}.

Personalize your answers using these preferences:
- Interests: {interests}
- Experience level: {experience}
- Preferred response style: {style}

For every message, infer the user's apparent emotion from their words and context.
Emotion inference is uncertain: never present it as a fact, diagnose the user, or
over-focus on it. If the cues are unclear, choose "neutral" with low confidence.
Respond naturally and adapt your tone when it seems useful. Do not mention the
emotion label unless the user asks. Focus on answering what the user said.
"""

emotion_schema = {
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

history = []

print(f"\nHi, {name}. Type 'quit' to end the chat.\n")

while True:
    message = input("You: ").strip()

    if message.lower() in {"bye", "see you", }:
        print("Bot: ok bye!,now get out of here and go do something productive -_- ashii")
        break

    if not message:
        continue

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=instructions,
        input=history + [{"role": "user", "content": message}],
        text={
            "format": {
                "type": "json_schema",
                "name": "personalized_chat_reply",
                "schema": emotion_schema,
                "strict": True,
            }
        },
    )

    result = json.loads(response.output_text)
    reply = result["reply"]

    print(f"\nBot: {reply}\n")

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})