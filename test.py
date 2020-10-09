"""
Tests for REST service to store, retrie and summarize texts
author: leonardo.echeverria@gmail.com
"""

from run import app
import unittest
from summarize import retrieve_text
import json

class Test(unittest.TestCase):
    def test_store(self):
        text = 'this is a very long text to store'
        request_data = dict(text=text)
        tester = app.test_client(self)
        response = tester.post('/', data=request_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        print('+++Test store document+++')
        print('stored document_id:', data['document_id'])

    def test_retrieve(self):
        #storing data to retrieve
        text = 'this is a very long text to retrieve'
        dummy_data = dict(text=text)
        tester = app.test_client(self)
        response = tester.post('/', data=dummy_data)
        data = json.loads(response.get_data())

        #retrieving data
        request_data = dict(doc_id=data['document_id'])
        response = tester.get('/', query_string=request_data)
        #response = tester.get('/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        print('+++Test retrieve document+++')
        print('retrieved document_id:', data['document_id'])
        print('text:', data['text'])


    def test_summarize(self):
        #text = "this is a very long test to summarize"
        text = retrieve_text()
        dummy_data = dict(text=text)
        request_data = dict(doc_id='3')
        tester = app.test_client(self)
        tester.post('/', data=dummy_data)
        response = tester.get('/summary', query_string=request_data)
        #response = tester.get('/summary/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        print('+++Test summarize document+++')
        print('summarized data:', data['summary'])


if __name__ == "__main__":
    unittest.main()