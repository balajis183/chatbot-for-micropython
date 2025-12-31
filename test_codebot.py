import unittest
from unittest.mock import Mock, patch
import codebot_test

class TestCodeBot(unittest.TestCase):

    def test_adc_rules_added(self):
        prompt = codebot_test.build_system_prompt("Read temperature")
        self.assertIn("ADC.ATTN_11DB", prompt)

    def test_ultrasonic_rules_added(self):
        prompt = codebot_test.build_system_prompt("ultrasonic distance")
        self.assertIn("TRIG = GPIO33", prompt)

    def test_generate_code_unauthorized(self):
        mock_resp = Mock()
        mock_resp.status_code = 401
        with patch('codebot_test.requests.post', return_value=mock_resp):
            self.assertEqual(codebot_test.generate_code("any"), "ERROR: Unauthorized – check API key")

    def test_generate_code_cleans_code(self):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = Mock()
        mock_resp.json = Mock(return_value={"choices":[{"message":{"content":"```python\nprint('hi')\n```"}}]})
        with patch('codebot_test.requests.post', return_value=mock_resp):
            out = codebot_test.generate_code("any")
            self.assertNotIn("```", out)
            self.assertIn("print('hi')", out)

if __name__ == '__main__':
    unittest.main()
