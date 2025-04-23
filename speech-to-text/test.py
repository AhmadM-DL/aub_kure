import os
import unittest
import base64
import tempfile
from unittest.mock import patch, MagicMock
import app


app.MODEL_CACHE_DIR = tempfile.gettempdir()
app.model_path = os.path.join(app.MODEL_CACHE_DIR, "base.pt")

class TestWhisperAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()
        self.temp_audio_path = "./resources/suicidal_sample.wav"

        with open(self.temp_audio_path, "rb") as audio:
            self.valid_audio_base64 = base64.b64encode(audio.read()).decode("utf-8")

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Message", response.get_json())

    @patch("app.get_model")
    def test_transcribe_with_mock_model(self, mock_get_model):
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "Test transcription from mock."}
        mock_get_model.return_value = (mock_model, True)

        response = self.client.post(
            "/transcribe",
            json={"audio_base64": self.valid_audio_base64}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Text", response.get_json())
        self.assertEqual(response.get_json()["Text"], "Test transcription from mock.")
        
    @patch("app.get_model")
    def test_transcribe_model_not_loaded(self, mock_get_model):
        mock_get_model.return_value = (None, False)

        response = self.client.post(
            "/transcribe",
            json={"audio_base64": self.valid_audio_base64}
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.get_json())


    @patch("app.get_model")
    def test_transcribe_missing_audio_field(self, mock_get_model):
        mock_model = MagicMock()
        mock_get_model.return_value = (mock_model, True)

        response = self.client.post("/transcribe", json={"wrong_field": "data"})
        self.assertEqual(response.status_code, 400)

    @patch("app.get_model")
    def test_transcribe_invalid_base64(self, mock_get_model):
        mock_model = MagicMock()
        mock_get_model.return_value = (mock_model, True)

        response = self.client.post("/transcribe", json={"audio_base64": "invalid@@@"})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
