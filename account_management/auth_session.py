# Basic logic: Session is created when a user logs in, and it expires after a certain period of inactivity.
# The session can be refreshed to extend its validity period - Making it malleable (i.e. it is an entity that can be changed).
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict

from user import User, UserRepository

# LOGINSESSION ENTITY
class LoginSession:
    """
    Represents a user authentication session.
    Attributes:
        session_id (str): Unique identifier for the session.
        user_id (str): Identifier for the user.
        login_time (datetime): Time when the user logged in.
        expiry_time (datetime): Time when the session expires.
    """
    def __init__(self, user_id: str):
        # Initialize a new session with a unique ID and user ID
        self.session_id: str = str(uuid.uuid4())
        self.user_id: str = user_id
        self.login_time: datetime = datetime.now(timezone.utc)
        self.expiry_time: datetime = self.login_time + timedelta(minutes=30)

    def refresh_expiry(self):
        # Refresh the session expiry time to 30 minutes from now
        now = datetime.now(timezone.utc)
        new_expiry = now + timedelta(minutes=30)
        if new_expiry <= self.expiry_time:
            print("Expiry refresh not needed yet")
        self.expiry_time = new_expiry

    def is_expired(self):
        # Check if the session has expired - returns True if expired
        return datetime.now(timezone.utc) > self.expiry_time

    def __repr__(self):
        # String representation of the session
        return (f"LoginSession(session_id='{self.session_id}', "
                f"user_id='{self.user_id}', login_time='{self.login_time}', "
                f"expiry_time='{self.expiry_time}')")
        
# AUTHENTICATOR SERVICE
class Authenticator:
    """
    Handles user authentication and session management.
    Attributes:
        user_repository (UserRepository): Repository to manage user data.
        sessions (Dict[str, LoginSession]): Active sessions keyed by session ID.
    """
    def __init__(self, user_repository: UserRepository):
        # Initialize the authenticator with a user repository
        self.user_repository = user_repository
        self.sessions: Dict[str, LoginSession] = {}

    def login(self, username: str, password: str) -> LoginSession:
        # Authenticate the user and create a session
        user = self.user_repository.find_by_username(username)
        if not user or not user.check_password(password):
            raise ValueError("Invalid username or password")

        session = LoginSession(user_id=user.id)
        self.sessions[session.session_id] = session
        return session

    def validate_session(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if session and not session.is_expired():
            return True
        return False

    def logout(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def refresh_session(self, session_id: str):
        session = self.sessions.get(session_id)
        if session and not session.is_expired():
            session.refresh_expiry()
        else:
            print("Invalid or expired session")