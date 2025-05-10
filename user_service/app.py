# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask import request, jsonify

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return {
        'function': 'hello_world',
        'emoji': '🌍'
    }

@app.route('/login', methods=['GET'])
def login_user():
    return {
        "sessionId": "1234567890abcdef",
        "userId": 1,
        "expiryTime": "2023-12-31T23:59:59Z"
    }

@app.route('/logout', methods=['POST'])
def logout_user():
    return '', 200

@app.route('/account', methods=['POST'])
def create_account():
    return jsonify({
        "userId": 1,
        "username": "john doe",
        "email": "john@email.com",
        "type": 2
    }), 200

@app.route('/account/<int:userId>', methods=['POST'])
def get_user_by_id(userId):
    return jsonify({
        "userId": userId,
        "username": "john doe",
        "email": "john@email.com",
        "type": 2
    }), 200

@app.route('/upload', methods=['POST'])
def upload_ct_scan():
    return jsonify({
        "id": 1,
        "image": "binary_data",
        "createdAt": "2023-12-31T23:59:59Z",
        "owner": 1
    }), 200

@app.route('/analyse', methods=['POST'])
def analyse_ct_scan():
    return jsonify({
        "id": 1,
        "createdAt": "2023-12-31T23:59:59Z",
        "ctScan": [{
            "id": 1,
            "image": "binary_data",
            "createdAt": "2023-12-31T23:59:59Z",
            "owner": 1
        }],
        "score": 95.5,
        "owner": 1
    }), 200

@app.route('/report', methods=['POST'])
def get_report():
    return jsonify({
        "id": 1,
        "createdAt": "2023-12-31T23:59:59Z",
        "content": "<html>Report Content</html>",
        "owner": 1,
        "ctScanAnalysis": [{
            "id": 1,
            "createdAt": "2023-12-31T23:59:59Z",
            "ctScan": [{
                "id": 1,
                "image": "binary_data",
                "createdAt": "2023-12-31T23:59:59Z",
                "owner": 1
            }],
            "score": 95.5,
            "owner": 1
        }]
    }), 200

@app.route('/create_report', methods=['POST'])
def create_report():
    return jsonify({
        "id": 1,
        "createdAt": "2023-12-31T23:59:59Z",
        "content": "<html>Report Content</html>",
        "owner": 1,
        "ctScanAnalysis": [{
            "id": 1,
            "createdAt": "2023-12-31T23:59:59Z",
            "ctScan": [{
                "id": 1,
                "image": "binary_data",
                "createdAt": "2023-12-31T23:59:59Z",
                "owner": 1
            }],
            "score": 95.5,
            "owner": 1
        }]
    }), 200

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)