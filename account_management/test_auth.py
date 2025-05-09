# Usage: python -m unittest account_management/test_auth.py
import unittest
import time
from datetime import datetime, timedelta, timezone
from account_management.user import User, UserRepository
from account_management.auth_session import LoginSession, Authenticator

class TestUser(unittest.TestCase):
    def test_check_password(self):
        user = User(user_id='1', username='alice', password='secret')
        self.assertTrue(user.check_password('secret'))
        self.assertFalse(user.check_password('wrong'))

class TestLoginSession(unittest.TestCase):
    def test_session_initialization_and_expiry(self):
        session = LoginSession(user_id='1')
        self.assertEqual(session.user_id, '1')
        self.assertFalse(session.is_expired())

    def test_session_refresh_expiry(self):
        session = LoginSession(user_id='1')
        with self.assertRaises(ValueError) as context:
            session.refresh_expiry()
        self.assertIn("Expiry refresh not needed yet", str(context.exception))

    def test_session_is_expired(self):
        session = LoginSession(user_id='1')
        session.expiry_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        self.assertTrue(session.is_expired())

class TestAuthenticator(unittest.TestCase):
    def setUp(self):
        self.repo = UserRepository()
        self.repo.add_user(User(user_id='1', username='alice', password='secret'))
        self.auth = Authenticator(self.repo)

    def test_successful_login(self):
        session = self.auth.login('alice', 'secret')
        self.assertEqual(session.user_id, '1')
        self.assertIn(session.session_id, self.auth.sessions)

    def test_failed_login(self):
        with self.assertRaises(ValueError):
            self.auth.login('alice', 'wrongpassword')

    def test_validate_session(self):
        session = self.auth.login('alice', 'secret')
        valid = self.auth.validate_session(session.session_id)
        self.assertTrue(valid)

    def test_validate_expired_session(self):
        session = self.auth.login('alice', 'secret')
        self.auth.sessions[session.session_id].expiry_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        valid = self.auth.validate_session(session.session_id)
        self.assertFalse(valid)

    def test_logout(self):
        session = self.auth.login('alice', 'secret')
        self.auth.logout(session.session_id)
        self.assertNotIn(session.session_id, self.auth.sessions)

    def test_refresh_session(self):        # Checks whether the refresh_session method extends the expiration time of a session
        session = self.auth.login('alice', 'secret')
        old_expiry = session.expiry_time
        time.sleep(2)
        self.auth.refresh_session(session.session_id)
        self.assertGreater(session.expiry_time, old_expiry)

    def test_refresh_expired_session_raises(self):
        session = self.auth.login('alice', 'secret')
        self.auth.sessions[session.session_id].expiry_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        with self.assertRaises(ValueError):
            self.auth.refresh_session(session.session_id)

if __name__ == '__main__':
    unittest.main()
