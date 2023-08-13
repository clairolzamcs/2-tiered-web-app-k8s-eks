import unittest
from app_routes import app

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page', response.data)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Us', response.data)

    def test_nonexistent_route(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
