import json
import os
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer
from unittest.mock import patch

import chatbot_server
import program2th


class ChatbotWebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), chatbot_server.ChatHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        cls.base_url = "http://127.0.0.1:{}".format(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def post_json(self, path, payload):
        request = Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=3) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    def test_frontend_assets_and_health_route_load(self):
        with patch.dict(os.environ, {}, clear=True):
            with urlopen(self.base_url + "/api/health", timeout=3) as response:
                health = json.loads(response.read().decode("utf-8"))
            self.assertEqual(health, {"status": "ok", "llmConfigured": False})

        for path, marker in (("/", "Mira"), ("/styles.css", ".app-shell"), ("/app.js", "/api/chat")):
            with urlopen(self.base_url + path, timeout=3) as response:
                self.assertEqual(response.status, 200)
                self.assertIn(marker, response.read().decode("utf-8"))

    def test_chat_passes_profile_and_history_to_model_boundary(self):
        profile = {
            "name": "Riley",
            "interests": "coding",
            "experience": "beginner",
            "style": "concise",
        }
        history = [
            {"role": "user", "content": "I am learning loops"},
            {"role": "assistant", "content": "We can take it slowly."},
        ]
        expected = {"reply": "Let's try a small loop.", "emotion": "confused", "confidence": "medium"}
        with patch.dict(os.environ, {"NVIDIA_API_KEY": "test-key"}):
            with patch.object(chatbot_server, "request_reply", return_value=expected) as model_call:
                status, result = self.post_json("/api/chat", {
                    "message": "Can you show me one?",
                    "history": history,
                    "profile": profile,
                })

        self.assertEqual(status, 200)
        self.assertEqual(result, expected)
        api_key, instructions, sent_history = model_call.call_args[0]
        self.assertEqual(api_key, "test-key")
        self.assertIn("Riley", instructions)
        self.assertIn("coding", instructions)
        self.assertEqual(sent_history, history + [{"role": "user", "content": "Can you show me one?"}])

    def test_missing_key_is_reported_without_calling_model(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(chatbot_server, "request_reply") as model_call:
                status, result = self.post_json("/api/chat", {"message": "Hello"})

        self.assertEqual(status, 503)
        self.assertIn("NVIDIA_API_KEY", result["error"])
        model_call.assert_not_called()

    def test_invalid_message_is_rejected(self):
        with patch.dict(os.environ, {"NVIDIA_API_KEY": "test-key"}):
            status, result = self.post_json("/api/chat", {"message": "   "})

        self.assertEqual(status, 400)
        self.assertIn("message", result["error"])

    def test_python_source_is_not_served(self):
        try:
            urlopen(self.base_url + "/program2th.py", timeout=3)
        except HTTPError as error:
            self.assertEqual(error.code, 404)
        else:
            self.fail("Python source should not be reachable from the web server")

    def test_llm_request_uses_server_key_and_expected_chat_endpoint(self):
        model_result = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "reply": "Hello there.",
                        "emotion": "happy",
                        "confidence": "low",
                    })
                }
            }]
        }

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(model_result).encode("utf-8")

        with patch.object(program2th, "urlopen", return_value=FakeResponse()) as send_request:
            result = program2th.request_reply(
                "test-key",
                "Use a concise friendly style.",
                [{"role": "user", "content": "Hello"}],
            )

        request = send_request.call_args[0][0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(request.full_url, "https://integrate.api.nvidia.com/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(request.get_header("Accept"), "application/json")
        self.assertEqual(payload["model"], "deepseek-ai/deepseek-v4.1-flash")
        self.assertEqual(payload["temperature"], 1.0)
        self.assertEqual(payload["top_p"], 0.95)
        self.assertEqual(payload["max_tokens"], 262144)
        self.assertIs(payload["stream"], False)
        self.assertEqual(payload["messages"][-1], {"role": "user", "content": "Hello"})
        self.assertNotIn("response_format", payload)
        self.assertEqual(result["reply"], "Hello there.")

    def test_bad_request_retries_with_minimal_payload(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({
                    "choices": [{"message": {"content": "Hello."}}]
                }).encode("utf-8")

        def reject_full_payload_then_accept_minimal(request, timeout):
            if json.loads(request.data.decode("utf-8")).get("temperature") is not None:
                raise HTTPError(request.full_url, 400, "Bad Request", {}, None)
            return FakeResponse()

        with patch.object(program2th, "urlopen", side_effect=reject_full_payload_then_accept_minimal):
            result = program2th.request_reply(
                "test-key", "Reply conversationally.", [{"role": "user", "content": "Hello"}]
            )

        self.assertEqual(result["reply"], "Hello.")

    def test_plain_text_model_response_is_kept_as_reply(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({
                    "choices": [{"message": {"content": "Hello, happy to help."}}]
                }).encode("utf-8")

        with patch.object(program2th, "urlopen", return_value=FakeResponse()):
            result = program2th.request_reply(
                "test-key", "Reply conversationally.", [{"role": "user", "content": "Hello"}]
            )

        self.assertEqual(result["reply"], "Hello, happy to help.")
        self.assertEqual(result["emotion"], "neutral")

    def test_model_list_uses_authorization_without_exposing_key(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps({"data": [{"id": "example/chat-model"}]}).encode("utf-8")

        with patch.object(program2th, "urlopen", return_value=FakeResponse()) as send_request:
            models = program2th.list_provider_models("test-key")

        request = send_request.call_args[0][0]
        self.assertTrue(request.full_url.endswith("/v1/models"))
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(models, ["example/chat-model"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
