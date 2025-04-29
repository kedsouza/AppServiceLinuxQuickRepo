import unittest
import app
import io, sys

from unittest.mock import patch

class TestApp(unittest.TestCase):

    maxDiff = None


    def test_generate_random_name(self):
        result = app.generate_random_name()
        self.assertIsNotNone(result)
        self.assertTrue(len(result) < 9)

    def test_print_subscription_information(self):
        user_name, subscription_name, subscription_id = ['kedsouza', 'MCAPS-Support-REQ-76423-2024-kedsouza', 'bf7728b1-4728-478d-96bc-db17b8ebc9ff']
        expected_output = "\nThis is the account information you are running with. If this is not correct please use `az account set` to correct this before continuing.\n"
        expected_output += ("--------------------------------------------------------------------------------\n")
        expected_output += ("User: {0}\n".format(user_name))
        expected_output += ("Subscription Name: {0}\n".format(subscription_name))
        expected_output += ("Subscription Id: {0}\n".format(subscription_id))
        expected_output += ("--------------------------------------------------------------------------------\n\n")
        
        with patch('sys.stdout', new = io.StringIO()) as fake_out:
            app.print_subscription_information('kedsouza', 'MCAPS-Support-REQ-76423-2024-kedsouza', 'bf7728b1-4728-478d-96bc-db17b8ebc9ff')
            self.assertEqual(fake_out.getvalue(), expected_output) 
