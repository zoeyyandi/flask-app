import unittest
from app import app
from werkzeug.exceptions import BadRequest

class TestMathEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test home endpoint
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'Simple Calculator API!')

    # Test add endpoint
    def test_add(self):
        response = self.app.post('/add', json={'a': 5, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['result'], 8)

    def test_add_negative_numbers(self):
        response = self.app.post('/add', json={'a': -5, 'b': -3})
        self.assertEqual(response.json['result'], -8)

    def test_add_missing_params(self):
        response = self.app.post('/add', json={'a': 5})  # missing 'b'
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameters: b', response.json['error'])

    def test_add_invalid_params(self):
        response = self.app.post('/add', json={'a': 'five', 'b': 3})  # invalid type
        self.assertEqual(response.status_code, 400)
        self.assertIn('Parameters must be numbers', response.json['error'])

    # Test subtract endpoint
    def test_subtract(self):
        response = self.app.post('/subtract', json={'a': 5, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 2)

    def test_subtract_negative_result(self):
        response = self.app.post('/subtract', json={'a': 3, 'b': 5})
        self.assertEqual(response.json['result'], -2)

    # Test multiply endpoint
    def test_multiply(self):
        response = self.app.post('/multiply', json={'a': 5, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 15)

    def test_multiply_by_zero(self):
        response = self.app.post('/multiply', json={'a': 5, 'b': 0})
        self.assertEqual(response.json['result'], 0)

    # Test square endpoint
    def test_square(self):
        response = self.app.post('/square', json={'a': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 16)

    def test_square_negative(self):
        response = self.app.post('/square', json={'a': -4})
        self.assertEqual(response.json['result'], 16)

    def test_square_missing_param(self):
        response = self.app.post('/square', json={})  # missing 'a'
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameters: a', response.json['error'])

    # Test divide endpoint
    def test_divide(self):
        response = self.app.post('/divide', json={'a': 6, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 2)

    def test_divide_float_result(self):
        response = self.app.post('/divide', json={'a': 5, 'b': 2})
        self.assertEqual(response.json['result'], 2.5)

    def test_divide_by_zero(self):
        response = self.app.post('/divide', json={'a': 6, 'b': 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Division by zero is not allowed.')

    def test_divide_missing_params(self):
        response = self.app.post('/divide', json={'a': 6})  # missing 'b'
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameters: b', response.json['error'])

    def test_not_found(self):
        response = self.app.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Not found')

if __name__ == '__main__':
    unittest.main()