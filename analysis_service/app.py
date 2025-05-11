# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from resources.customTypes import User, Session, Report, CtScan, CtScanAnalysis, Error
import json
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
        'message': 'Hello, World!'
    }
@app.route('/upload', methods=['POST'])
def upload_ct_scan():
    response = CtScan(
        id=1,
        image="binary_data",
        createdAt="2023-01-01T00:00:00Z",
        owner=1
    ).__dict__
    print(response)
    return response, 200


@app.route('/analyse', methods=['POST'])
def analyse_ct_scan():
    response = CtScanAnalysis(
        id=1,
        createdAt="2023-01-01T00:00:00Z",
        ctScan=[CtScan(id=1, image="binary_data", createdAt="2023-01-01T00:00:00Z", owner=1).__dict__],
        score=95.5,
        owner=1
    ).__dict__
    print(response)
    return response, 200


@app.route('/report/<int:reportId>', methods=['GET'])
def get_report(reportId):
    response = Report(
        id=reportId,
        createdAt="2023-01-01T00:00:00Z",
        content="<html>Report Content</html>",
        owner=1,
        ctScanAnalysis=[CtScanAnalysis(
            id=1,
            createdAt="2023-01-01T00:00:00Z",
            ctScan=[CtScan(id=1, image="binary_data", createdAt="2023-01-01T00:00:00Z", owner=1).__dict__],
            score=95.5,
            owner=1
        ).__dict__]
    ).__dict__
    print(response)
    return response, 200


@app.route('/report', methods=['POST'])
def create_report():
    response = Report(
        id=1,
        createdAt="2023-01-01T00:00:00Z",
        content="<html>Report Content</html>",
        owner=1,
        ctScanAnalysis=[CtScanAnalysis(
            id=1,
            createdAt="2023-01-01T00:00:00Z",
            ctScan=[CtScan(id=1, image="binary_data", createdAt="2023-01-01T00:00:00Z", owner=1).__dict__],
            score=95.5,
            owner=1
        ).__dict__]
    ).__dict__
    print(response)
    return response, 200

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)