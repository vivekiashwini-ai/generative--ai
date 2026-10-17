import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from program2th import list_provider_models, make_instructions, request_reply


ROOT = Path(__file__).resolve().parent
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
}
MAX_BODY_BYTES = 65536
MAX_MESSAGE_CHARS = 4000
MAX_HISTORY_MESSAGES = 12
EMOTIONS = {
    "neutral", "happy", "sad", "frustrated", "anxious", "confused", "excited", "other"
}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
DEFAULT_PROFILE = {
    "name": "friend",
    "interests": "general topics",
    "experience": "not specified",
    "style": "friendly and clear",
}


class ChatHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_json(200, {
                "status": "ok",
                "llmConfigured": bool(
                    os.environ.get("CHATBOT_API_KEY") or os.environ.get("NVIDIA_API_KEY")
                ),
            })
            return

        if self.path == "/api/models":
            api_key = os.environ.get("CHATBOT_API_KEY") or os.environ.get("NVIDIA_API_KEY")
            if not api_key:
                self.send_json(503, {"error": "NVIDIA_API_KEY is not configured."})
                return
            try:
                self.send_json(200, {"models": list_provider_models(api_key)})
            except RuntimeError as error:
                details = str(error).replace(api_key, "[redacted]")[:500]
                self.send_json(502, {"error": details})
            return

        resource = STATIC_FILES.get(self.path.split("?", 1)[0])
        if resource is None:
            self.send_json(404, {"error": "Not found"})
            return

        filename, content_type = resource
        body = (ROOT / filename).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid request length"})
            return
        if content_length < 1 or content_length > MAX_BODY_BYTES:
            self.send_json(413, {"error": "Request body is empty or too large"})
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "Request body must be valid JSON"})
            return
        if not isinstance(payload, dict):
            self.send_json(400, {"error": "Request body must be a JSON object"})
            return

        message = payload.get("message")
        if not isinstance(message, str) or not message.strip():
            self.send_json(400, {"error": "A non-empty message is required"})
            return
        message = message.strip()
        if len(message) > MAX_MESSAGE_CHARS:
            self.send_json(413, {"error": "Message is too long"})
            return

        api_key = os.environ.get("CHATBOT_API_KEY") or os.environ.get("NVIDIA_API_KEY")
        if not api_key:
            self.send_json(503, {"error": "Set NVIDIA_API_KEY in the server environment to enable replies."})
            return

        profile = payload.get("profile", {})
        if not isinstance(profile, dict):
            profile = {}
        safe_profile = {}
        for key, default in DEFAULT_PROFILE.items():
            value = profile.get(key, default)
            safe_profile[key] = value.strip()[:160] if isinstance(value, str) and value.strip() else default

        history = payload.get("history", [])
        if not isinstance(history, list):
            history = []
        safe_history = []
        for item in history[-MAX_HISTORY_MESSAGES:]:
            if not isinstance(item, dict) or item.get("role") not in {"user", "assistant"}:
                continue
            content = item.get("content")
            if isinstance(content, str) and content.strip():
                safe_history.append({"role": item["role"], "content": content.strip()[:MAX_MESSAGE_CHARS]})
        safe_history.append({"role": "user", "content": message})

        try:
            result = request_reply(api_key, make_instructions(safe_profile), safe_history)
            if not isinstance(result, dict) or not isinstance(result.get("reply"), str):
                raise ValueError("Missing reply in model response")
        except (RuntimeError, ValueError, TypeError, KeyError, IndexError) as error:
            details = str(error).replace(api_key, "[redacted]")[:500]
            print("LLM request failed: {}".format(details))
            self.send_json(502, {
                "error": "NVIDIA request failed: {}".format(details)
            })
            return

        emotion = result.get("emotion")
        confidence = result.get("confidence")
        self.send_json(200, {
            "reply": result["reply"],
            "emotion": emotion if emotion in EMOTIONS else "neutral",
            "confidence": confidence if confidence in CONFIDENCE_LEVELS else "low",
        })

    def log_message(self, format_string, *args):
        print("{} - {}".format(self.address_string(), format_string % args))


def main():
    host = os.environ.get("CHATBOT_HOST", "127.0.0.1")
    port = int(os.environ.get("CHATBOT_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), ChatHandler)
    print("Chatbot running at http://{}:{}/".format(host, port))
    if os.environ.get("CHATBOT_API_KEY") or os.environ.get("NVIDIA_API_KEY"):
        print("NVIDIA API key detected; LLM replies are enabled.")
    else:
        print("Set NVIDIA_API_KEY in this terminal before launching to enable LLM replies.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping chatbot server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
