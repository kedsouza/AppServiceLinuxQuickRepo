import unittest
import app

class TestApp(unittest.TestCase):

    def test_generate_random_name(self):
        result = app.generate_random_name()
        self.assertIsNotNone(result)
        self.assertTrue(len(result) < 9)

