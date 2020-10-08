"""
Unittests for REST service for storing, retrieving and summarizing texts
author: leonardo.echeverria@gmail.com
"""

from run import app
import unittest
from summarize import retrieve_text

class FlaskTest(unittest.TestCase):
    def test_store(self):
        text = 'this is a very long text to store'
        request_data = dict(text=text)
        tester = app.test_client(self)
        response = tester.post('/', data=request_data)
        data = response.get_data()
        print('stored data:', data)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        text = 'this is a very long text to retrieve'
        dummy_data = dict(text=text)
        request_data = dict(doc_id='1')
        tester = app.test_client(self)
        tester.post('/', data=dummy_data)
        response = tester.get('/', query_string=request_data)
        #response = tester.get('/1')
        data = response.get_data()
        print('retrieved data:', data)
        self.assertEqual(response.status_code, 200)

    def test_summarize(self):
        #text = "this is a very long test to summarize"
        text = retrieve_text()
        dummy_data = dict(text=text)
        request_data = dict(doc_id='3')
        tester = app.test_client(self)
        tester.post('/', data=dummy_data)
        response = tester.get('/summary', query_string=request_data)
        #response = tester.get('/summary/1')
        data = response.get_data()
        print('summarized data:', data)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()