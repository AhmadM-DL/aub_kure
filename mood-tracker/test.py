import unittest
from unittest.mock import patch, MagicMock
from app import app


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "healthy"})

    @patch('app.get_model')
    def test_mood_tracking_valid_input(self, mock_get_model):
        mock_model = MagicMock()
        mock_model.return_value = {
        "labels": ["Anger", "Disgust", "Sadness", "Surprise", "Fear", "Trust", "Joy", "Anticipation"],
        "scores": [0.05, 0.1, 0.1, 0.15, 0.2, 0.25, 0.85, 0.3]
        }
        mock_get_model.return_value = (mock_model, True)

        response = self.app.post('/sentiment', json={"text": "I'm feeling sad today!"})

        response_data = response.get_json()
        self.assertIn("Joy", response_data)
        self.assertIn("Sadness", response_data)
        self.assertIn("Anger", response_data)
        self.assertIn("Trust", response_data)
        self.assertIn("Fear", response_data)
        self.assertIn("Disgust", response_data)
        self.assertIn("Anticipation", response_data)
        self.assertIn("Surprise", response_data)
        self.assertIsInstance(response_data["Joy"], float)

    def test_mood_tracking_missing_text(self):
        response = self.app.post('/sentiment', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "No text provided"})

    @patch('app.get_model')
    def test_mood_tracking_model_failure(self, mock_get_model):
        mock_get_model.return_value = (None, False)
        response = self.app.post('/sentiment', json={"text": "Not sure how I feel."})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "Internal Server Error"})


if __name__ == '__main__':
    unittest.main()
