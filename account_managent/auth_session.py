# Basic logic: Session is created when a user logs in, and it expires after a certain period of inactivity.
# The session can be refreshed to extend its validity period - Making it malleable (i.e. it is an entity that can be changed).
import uuid
from datetime import datetime, timedelta, timezone

class AuthenticationSession:
    """
    Represents a user authentication session.
    Attributes:
        session_id (str): Unique identifier for the session.
        user_id (str): Identifier for the user.
        login_time (datetime): Time when the user logged in.
        expiry_time (datetime): Time when the session expires.
    """
    def __init__(self, user_id: str):
        self.session_id: str = str(uuid.uuid4())
        self.user_id: str = user_id
        self.login_time: datetime = datetime.now(timezone.utc)
        self.expiry_time: datetime = self.login_time + timedelta(minutes=30)

    def refresh_expiry(self):
        """Extend expiry time by another 30 minutes from now."""
        now = datetime.now(timezone.utc)
        self.expiry_time = now + timedelta(minutes=30)

    def __repr__(self):
        return (f"AuthenticationSession(session_id='{self.session_id}', "
                f"user_id='{self.user_id}', login_time='{self.login_time}', "
                f"expiry_time='{self.expiry_time}')")