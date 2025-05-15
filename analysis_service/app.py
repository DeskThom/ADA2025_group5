# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from resources.customTypes import User, Session, Report, CtScan, CtScanAnalysis, Error
import json
import sqlite3
import random
from datetime import datetime
import requests

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
DATABASE_URL = '/data/aidence.db'
EMAIL_SERVICE_URL = "https://us-central1-adaaaaa.cloudfunctions.net/send-email"  # This needs a valid project ID and region , please help

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
    data = request.get_json()
    anonymized_file = data.get('file')
    owner = data.get('owner', 1)

    created_at = datetime.now().isoformat()

    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO CtScan (image, createdAt, owner)
        VALUES (?, ?, ?)
        """,
        (anonymized_file, created_at, owner)
    )
    ct_scan_id = cursor.lastrowid  # auto-generated ID
    conn.commit()
    conn.close()

    return {
        "id": ct_scan_id,
        "createdAt": created_at,
        "owner": owner
    }, 200




@app.route('/analyse', methods=['POST'])
def analyse_ct_scan():
    data = request.get_json()
    ct_scan_id = data.get('ctScanId')
    owner = data.get('owner', 1)

    created_at = datetime.now().isoformat()
    score = round(random.uniform(0.0, 1.0), 2)  # Simulate score

    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Verify CT Scan exists
    cursor.execute("SELECT id, image, createdAt FROM CtScan WHERE id = ?", (ct_scan_id,))
    ct_scan_row = cursor.fetchone()
    if not ct_scan_row:
        return {"code": "404", "message": "CT Scan not found"}, 404

    # Save analysis
    cursor.execute(
        """
        INSERT INTO CtScanAnalysis (createdAt, score, owner, ctScan)
        VALUES (?, ?, ?, ?)
        """,
        (created_at, score, owner, ct_scan_id)
    )
    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()

    ct_scan = {
        "id": ct_scan_row[0],
        "image": ct_scan_row[1],
        "createdAt": ct_scan_row[2],
        "owner": owner
    }

    response = {
        "id": analysis_id,
        "createdAt": created_at,
        "score": score,
        "owner": owner,
        "ctScan": [ct_scan]
    }

    return response, 200


@app.route('/report/<int:reportId>', methods=['GET'])
def get_report(reportId):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Get Report
    cursor.execute(
        "SELECT id, createdAt, ctScanAnalysis, content, owner FROM Report WHERE id = ?",
        (reportId,)
    )
    report_row = cursor.fetchone()
    if not report_row:
        return {"code": "404", "message": "Report not found"}, 404

    report_id, report_created_at, analysis_id, content, report_owner = report_row
    
    # Get CtScanAnalysis
    cursor.execute(
        "SELECT id, createdAt, score, owner, ctScan FROM CtScanAnalysis WHERE id = ?",
        (analysis_id,)
    )
    analysis_row = cursor.fetchone()
    if not analysis_row:
        return {"code": "404", "message": "Analysis not found"}, 404

    analysis_id, analysis_created_at, score, analysis_owner, ct_scan_id = analysis_row

    # Get CtScan
    cursor.execute(
        "SELECT id, image, createdAt, owner FROM CtScan WHERE id = ?",
        (ct_scan_id,)
    )
    scan_row = cursor.fetchone()
    if not scan_row:
        return {"code": "404", "message": "CT Scan not found"}, 404

    scan_id, image, scan_created_at, scan_owner = scan_row

    conn.close()

    # Build nested response
    response = {
        "id": report_id,
        "createdAt": report_created_at,
        "content": content,
        "owner": report_owner,
        "ctScanAnalysis": [{
            "id": analysis_id,
            "createdAt": analysis_created_at,
            "score": score,
            "owner": analysis_owner,
            "ctScan": [{
                "id": scan_id,
                "image": image,
                "createdAt": scan_created_at,
                "owner": scan_owner
            }]
        }]
    }

    return response, 200

def trigger_email(user_email,type_email,other_data):
    try:
        response = requests.post(
            EMAIL_SERVICE_URL,
            json={
                "email": user_email,
                "type": type_email,
                "other_data": other_data  # Add any other data you want to send
            }
        )
        if response.status_code == 200:
            print("Email service triggered successfully.")
        else:
            print(f"Failed to trigger email service: {response.status_code}")
    except request.exceptions.RequestException as e:
        print(f"Error triggering email service: {e}")
    finally:
        print(f"Email service triggered successfully.")


@app.route('/report', methods=['POST'])
def create_report():
    data = request.get_json()
    analysis_id = data.get('ctScanAnalysisId')
    owner = data.get('owner', 1)
     # Get the owner's email from the User table
    cursor.execute(
        "SELECT email FROM User WHERE id = ?",
        (owner,)
    )
    user_row = cursor.fetchone()
    if user_row:
        report_owner_email = user_row[0]
    else:
        report_owner_email = None  # or handle not found
    created_at = datetime.now().isoformat()

    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Verify analysis and get its score
    cursor.execute("SELECT score FROM CtScanAnalysis WHERE id = ?", (analysis_id,))
    analysis_row = cursor.fetchone()
    if not analysis_row:
        return {"code": "404", "message": "CT Scan Analysis not found"}, 404

    score = analysis_row[0]

    # Dynamically generate HTML content
    content = f"""
    <html>
        <head><title>CT Scan Report</title></head>
        <body>
            <h2>CT Scan Analysis Report</h2>
            <p>Analysis Score: <strong>{score:.2f}</strong></p>
            <p>Report generated at: {created_at}</p>
        </body>
    </html>
    """
    result = trigger_email(report_owner_email,1,content)  # Trigger email service
    print(f"Trigger mail succes: {result}")

    # Insert report
    cursor.execute(
        """
        INSERT INTO Report (createdAt, ctScanAnalysis, content, owner)
        VALUES (?, ?, ?, ?)
        """,
        (created_at, analysis_id, content, owner)
    )
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "id": report_id,
        "createdAt": created_at,
        "ctScanAnalysis": analysis_id,
        "content": content,
        "owner": owner
    }, 200



# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)