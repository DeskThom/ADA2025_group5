# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from resources.customTypes import User, Session, CtScan, CtScanAnalysis, Error, Payment
import sqlite3
from datetime import datetime, timedelta
import uuid

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
DATABASE_URL = '/data/aidence.db'
DEBIT_SERVICE = "https://us-central1-adaaaaa.cloudfunctions.net/get-money"  # This needs a valid project ID and region , please help
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/payment', methods=['POST'])
def get_payment():
    userId = request.json.get('userId')
    amount = request.json.get('amount')
    
    if False: #Here use FAAS application to get money DEBIT_SERVICE
        return {"error": "Direct debit procedure failed, external error"}, 401
    # Look up the user in the database
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Payment (createdAt, amount, user) VALUES (?, ?, ?)
            """,
            (datetime.now(), amount, userId)
        )
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"error": "Failed to create payment"}, 500
    finally:
        conn.close()
    
    return {}, 200

@app.route('/payment/<int:userId>', methods=['GET'])
def get_user_account(userId):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM Payment WHERE user = ?
            """,
            (userId,)
        )
        rows = cursor.fetchall()

        if not rows:
            return {"error": "User not found"}, 404

        payments = []
        for row in rows:
            payments.append(Payment(
                id=row[0],
                createdAt=row[1],
                amount=row[2],
                userId=row[3]
            ).__dict__)

    except sqlite3.Error as e:
        error: Error = Error(
            code=500,
            message="Database error",
            details=str(e)
        )
        print(f"Database error: {e}")
        return error.to_dict(), 500
    
    finally:
        conn.close()
    
    return {"payments": payments}, 200

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)