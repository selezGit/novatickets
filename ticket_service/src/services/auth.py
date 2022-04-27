from core.config import MANAGER_PASSWORD
from werkzeug.security import check_password_hash


class AuthService:
    def check_password(self, password: str) -> bool:
        return check_password_hash(MANAGER_PASSWORD, password)
