import unittest
import app
import io, sys


# Function we want to test.
def get_az_account_data():
    subprocess_use_shell = True if len(sys.argv) > 1  and sys.argv[1] == 'DEBUG' else False
    data = subprocess.run(["az", "account", "show"], capture_output=True, shell=subprocess_use_shell)
    account_data = json.loads(data.stdout)
    subscription_id = account_data['id']
    subscription_name = account_data['name']
    user_name = account_data['user']['name'].split('@')[0]

    return [user_name, subscription_name, subscription_id]


#####################
from unittest import MagicMock

class ProductionClass():
    pass

class TestApp(unittest.TestCase):
    




