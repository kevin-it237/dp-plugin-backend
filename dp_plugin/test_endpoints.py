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

    def test_get_paginated_questions(self):
        """ Test """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))

    def test_404_get_paginated_questions(self):
        res = self.client().get('/books?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
    
    def test_create_question(self):
        """ Test """
        res = self.client().post('/questions', 
        data=json.dumps(dict(question='Question', answer='ans', category='1', difficulty=1)), 
        content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    
    def test_400_create_question(self):
        """ Test """
        res = self.client().post('/questions', data=json.dumps(dict(question='bar')), content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()