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
    def test_suicide_risk_valid_input(self, mock_get_model):
        mock_model = MagicMock()
        mock_model.return_value = [{"label": "suicide", "score": 0.85}]
        mock_get_model.return_value = (mock_model, True)

        response = self.app.post('/suicide-risk', json={"text": "I feel sad but I'll be okay."})
        self.assertEqual(response.status_code, 200)
        self.assertIn("label", response.get_json())
        self.assertIn("confidence", response.get_json())

    def test_suicide_risk_missing_text(self):
        response = self.app.post('/suicide-risk', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "No text provided"})

    @patch('app.get_model')
    def test_suicide_risk_model_failure(self, mock_get_model):
        mock_get_model.return_value = (None, False)
        response = self.app.post('/suicide-risk', json={"text": "I'm feeling lost."})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "Internal Server Error"})


if __name__ == '__main__':
    unittest.main()
