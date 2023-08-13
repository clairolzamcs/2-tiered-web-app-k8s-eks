import unittest
from unittest.mock import patch
from app import app

class TestAppRoutes(unittest.TestCase):

    # def setUp(self):
    #     # Set up a test client
    #     self.client = app.test_client()
    
     @patch('app.connections.Connection')
    def test_add_employee(self, mock_connection):
        # Simulate a successful connection
        mock_cursor = mock_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value = None

        # Create a test client for the Flask app
        self.app = app.test_client()

        # Send a POST request to the AddEmp endpoint
        response = self.app.post('/addemp', data={
            'emp_id': '123',
            'first_name': 'John',
            'last_name': 'Doe',
            'primary_skill': 'Python',
            'location': 'New York'
        })

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check if the expected content is present in the response
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'Employee Added Successfully', response.data)
        
    # def test_home_route(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Home Page', response.data)

    # def test_about_route(self):
    #     response = self.client.get('/about')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'About Us', response.data)

    # def test_nonexistent_route(self):
    #     response = self.client.get('/nonexistent')
    #     self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
