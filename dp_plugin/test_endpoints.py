import unittest
import json
from dp_plugin import create_app

class ApiTestCase(unittest.TestCase):
    """This class represents the apis test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
    
    def tearDown(self):
        """Executed after each test"""
        pass
    
    def test_create_question(self):
        """ Test """
        res = self.client().post('/questions', 
        data=json.dumps(dict(question='Question', answer='ans', category='1', difficulty=1)), 
        content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()