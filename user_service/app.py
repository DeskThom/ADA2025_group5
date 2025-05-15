# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import requests
from resources.customTypes import User, Session, CtScan, CtScanAnalysis, Error
import sqlite3
from datetime import datetime, timedelta
import uuid
import requests
import multiprocessing
import time

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
DATABASE_URL = '/data/aidence.db'
EMAIL_SERVICE_URL = "https://us-central1-adaaaaa.cloudfunctions.net/send-email"  # This needs a valid project ID and region , please help
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/login', methods=['POST'])
def login_user():
    # Check if the credentials are valid
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Look up the user in the database
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM User WHERE username = ? AND password = ?
            """,
            (username, password)
        )
        row = cursor.fetchone()
        
        if row is None:
            return {"error": "Invalid credentials"}, 401

        user = User(
            userId=row[0],
            username=row[1],
            email=row[2],
            type=row[3],
            password=row[4]
        )
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"error": "Failed to login"}, 500
    finally:
        conn.close()
    
    # Check if the user is already logged in (look up session table)
    # If not, create a new session
    
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM Session WHERE userId = ?
            """,
            (user.userId,)
        )
        row = cursor.fetchone()
        
        if row is None:
            # Create a new session
            session = Session(
                sessionId=str(uuid.uuid4()),
                userId=user.userId,
                expiryTime=datetime.now() + timedelta(minutes=30)
            )
            # Set the expiry time to 30 minutes from now            
            session.expiryTime = datetime.now() + timedelta(minutes=30)
            cursor.execute(
                """
                INSERT INTO Session (sessionId, userId, expiryTime)
                VALUES (?, ?, ?)
                """,
                (session.sessionId, session.userId, session.expiryTime)
            )
            conn.commit()
            
        else:
            # Refresh the session expiry time
            session = Session(
                sessionId=row[0],
                userId=row[1],
                expiryTime=row[2]
            )
            session.expiryTime = datetime.now() + timedelta(minutes=30)
            cursor.execute(
                """
                UPDATE Session SET expiryTime = ? WHERE sessionId = ?
                """,
                (session.expiryTime, session.sessionId)
            )
            conn.commit()
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"error": "Failed to create session"}, 500
    finally:
        conn.close()

    return session.__dict__, 200


@app.route('/logout', methods=['POST'])
def logout_user():
    # Remove the session from the database
    userId = request.json.get('userId')
    
    # Find the latest session for the user
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM Session WHERE userId = ?
            """,
            (userId,)
        )
        row = cursor.fetchone()
        
        if row is None:
            return {"error": "No active session found"}, 404

        session = Session(
            sessionId=row[0],
            userId=row[1],
            expiryTime=row[2]
        )
        # Delete the session
        cursor.execute(
            """
            DELETE FROM Session WHERE sessionId = ?
            """,
            (session.sessionId,)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"error": "Failed to logout"}, 500
    finally:
        conn.close()

    return {}.__dict__, 200
def send_periodic_email():
    i=1
    while True:
        
        try:
            user_email = "aidencemails@gmail.com"
            type_email = 2
            other_data = i
            trigger_email(user_email, type_email, other_data)
            print(f"Periodic email sent to {user_email}")
            i+=1
        except Exception as e:
            print(f"Error sending periodic email: {e}")
        time.sleep(86400)

def trigger_email(user_email, type_email, other_data):
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
            print("Email service send successfully.")
        else:
            print(f"Failed to send email service: {response.status_code}")
    except request.exceptions.RequestException as e:
        print(f"Error sending email service: {e}")
    finally:
        print(f"Email service triggered successfully.")

@app.route('/account', methods=['POST'])
def create_user_account():
    user = User(
        userId=None,
        username= request.json.get('username'),
        email= request.json.get('email'),
        type= request.json.get('type', 2),
        password= request.json.get('password')
    )
    
    result = trigger_email(user.email,1,None)  # Trigger email service
    print(f"Trigger mail succes: {result}")
    # Tests still necessary
    
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO User (username, email, type, password)
            VALUES (?, ?, ?, ?)
            """,
            (user.username, user.email, user.type, user.password)
        )
        conn.commit()
        user.userId = cursor.lastrowid
    
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"error": "Failed to create user account"}, 500
    finally:
        conn.close()

    print(user)
    return user.__dict__, 200


@app.route('/account/<int:userId>', methods=['GET'])
def get_user_account(userId):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM User WHERE userId = ?
            """,
            (userId,)
        )
        row = cursor.fetchone()
        
        if row is None:
            return {"error": "User not found"}, 404

        user = User(
            userId=row[0],
            username=row[1],
            email=row[2],
            type=row[3],
            password=row[4]
        )
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {"error": "Failed to retrieve user account"}, 500
    finally:
        conn.close()
        

    print(user)
    return user.__dict__, 200


# main driver function
if __name__ == '__main__':
    email_process = multiprocessing.Process(target=send_periodic_email)
    email_process.start()
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)