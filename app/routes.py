from flask import jsonify, request
from app import app
from app.logic import add, subtract, multiply, square, divide
from werkzeug.exceptions import BadRequest
from http import HTTPStatus
from app.exceptions import NotFoundClientError, BadRequestClientError, ClientError

@app.before_request
def check_json():
    if request.method in ['POST', 'PUT'] and not request.is_json:
        raise BadRequestClientError()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Simple Calculator API!"})

def get_required_params(data, params):
    missing = [p for p in params if p not in data]
    if missing:
        raise BadRequest(f"Missing required parameters: {', '.join(missing)}")
    try:
        return [float(data[p]) for p in params]
    except ValueError:
        raise BadRequestClientError("Values are invalid!!")

@app.route('/add', methods=['POST'])
def add_endpoint():
    data = request.get_json()
    a, b = get_required_params(data, ['a', 'b'])
    result = add(a, b)
    return jsonify({'result': result})

@app.route('/subtract', methods=['POST'])
def subtract_endpoint():
    data = request.get_json()
    a, b = get_required_params(data, ['a', 'b'])
    result = subtract(a, b)
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply_endpoint():
    data = request.get_json()
    a, b = get_required_params(data, ['a', 'b'])
    result = multiply(a, b)
    return jsonify({'result': result})

@app.route('/square', methods=['POST'])
def square_endpoint():
    data = request.get_json()
    a, = get_required_params(data, ['a'])
    result = square(a)
    return jsonify({'result': result})

@app.route('/divide', methods=['POST'])
def divide_endpoint():
    data = request.get_json()
    a, b = get_required_params(data, ['a', 'b'])
    try:
        result = divide(a, b)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero is not allowed.'}), 400
    
# Explicitly handle OPTIONS method for /add
@app.route('/add', methods=['OPTIONS'])
def add_options():
    return '', 200

@app.errorhandler(ClientError)
def handle_bad_request(e):
    return jsonify(e.to_json())
    # return jsonify(status_code=e.status_code, message=e.message)
    # if "Failed to decode JSON object" in str(e) or "Request must be JSON" in str(e):
    #     return jsonify({'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST
    # return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'})

@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Not found'}), 404
