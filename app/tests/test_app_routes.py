import unittest
from unittest.mock import patch
from app import app

class TestAppDatabaseConnection(unittest.TestCase):

    @patch('app.connections.Connection')
    def test_database_connection(self, mock_connection):
        # Create a test client for the Flask app
        self.app = app.test_client()

        # Send a GET request to the root endpoint
        response = self.app.get('/')

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Optionally, check the response content for a specific string or content

if __name__ == '__main__':
    unittest.main()
