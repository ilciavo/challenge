from run import app
import unittest
import json

class FlaskTest(unittest.TestCase):
    def test_store(self):
        request_data = dict(text='this is a very long test to store')
        tester = app.test_client(self)
        response = tester.post('/', data=request_data)
        data = response.get_data()
        print('stored data:', data)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        dummy_data = dict(text='this is a very long test to retrieve')
        request_data = dict(doc_id='1')
        tester = app.test_client(self)
        tester.post('/', data=dummy_data)
        response = tester.get('/', query_string=request_data)
        data = response.get_data()
        print('retrieved data:', data)
        self.assertEqual(response.status_code, 200)

    def test_summarize(self):
        dummy_data = dict(text='this is a very long test to summarize')
        request_data = dict(sum_id='3')
        tester = app.test_client(self)
        tester.post('/', data=dummy_data)
        response = tester.get('/', query_string=request_data)
        data = response.get_data()
        print('summarized data:', data)
        #self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()