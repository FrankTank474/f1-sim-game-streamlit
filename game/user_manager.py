import json
from pathlib import Path
import logging
from typing import Dict, Optional
import hashlib
import secrets

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self._initialize_data_store()
    
    def _initialize_data_store(self):
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_users(self) -> Dict:
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Error reading users file, returning empty dict")
            return {}

    def _save_users(self, users: Dict):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def _hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        if not salt:
            salt = secrets.token_hex(16)
        salted = password + salt
        hashed = hashlib.sha256(salted.encode()).hexdigest()
        return hashed, salt

    def create_user(self, username: str, password: str) -> bool:
        """Create a new user. Returns True if successful, False if username exists"""
        users = self._load_users()
        
        if username in users:
            return False
            
        hashed_pw, salt = self._hash_password(password)
        users[username] = {
            'password_hash': hashed_pw,
            'salt': salt
        }
        
        self._save_users(users)
        return True

    def verify_login(self, username: str, password: str) -> bool:
        """Verify login credentials. Returns True if valid."""
        users = self._load_users()
        
        if username not in users:
            return False
            
        user = users[username]
        hashed_input, _ = self._hash_password(password, user['salt'])
        
        return hashed_input == user['password_hash']