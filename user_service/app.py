# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from resources.customTypes import User, Session, CtScan, CtScanAnalysis, Error

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/login', methods=['POST'])
def login_user():
    # Simulate login logic
    response = Session(
        sessionId="1234567890abcdef",
        userId=1,
        expiryTime="2023-12-31T23:59:59"
    ).__dict__

    print(response)
    return response, 200


@app.route('/logout', methods=['POST'])
def logout_user():

    return {}, 200


@app.route('/account', methods=['POST'])
def create_user_account():
    response = User(
        userId=1,
        username="john doe",
        email="john@email.com",
        type=2,
        password="password123"
    ).__dict__

    print(response)
    return response, 200


@app.route('/account/<int:userId>', methods=['GET'])
def get_user_account(userId):

    response = User(
        userId=1,
        username="john doe",
        email="john@email.com",
        type=2,
        password="password123"
    ).__dict__

    print(response)
    return response, 200


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)