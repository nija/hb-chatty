'''Tests for chatty'''
import unittest

from server import app
from model import *

class ChatModelTests(unittest.TestCase):
    '''Tests for the data model and ORM'''

    def setUp(self):
        pass
    def tearDown(self):
        pass


class ChatAPITests(unittest.TestCase):
    '''Tests for the API routes'''

    def setUp(self):
        pass
    def tearDown(self):
        pass


class ChatWebTests(unittest.TestCase):
    """Tests for the routes"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_page(self):
        '''Checking the root route'''
        result = self.client.get("/")
        self.assertIn("Please chat with me", result.data)
        self.assertEqual(result.status_code, 200)

    # def test_rsvp(self):
    #     '''Checking... post something something'''
    #     result = self.client.post("/process_msg_event",
    #                               data={'name': "Jane", 'data': "jane@jane.com"},
    #                               follow_redirects=True)

    #     self.assertIn("jane@jane", result.data)
    #     self.assertEqual(result.status_code, 200)
        #self.assertNotIn("Please RSVP", result.data)


if __name__ == "__main__":
    unittest.main()
