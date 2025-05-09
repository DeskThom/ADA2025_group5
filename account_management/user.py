from typing import Dict


# --- Simple User model ---

class User:
    def __init__(self, user_id: str, username: str, password: str):
        self.id = user_id
        self.username = username
        self.password = password  # NOTE: plaintext for demo — NEVER store like this in real systems!
        
    def __repr__(self):
        return f"User(user_id='{self.user_id}', username='{self.username}')"

    def check_password(self, password: str) -> bool:
        return self.password == password

# --- Simple in-memory UserRepository ---   (inplace of a database for demo purposes)

class UserRepository:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def add_user(self, user: User):
        self.users[user.username] = user

    def find_by_username(self, username: str) -> User:
        return self.users.get(username)
    
    
