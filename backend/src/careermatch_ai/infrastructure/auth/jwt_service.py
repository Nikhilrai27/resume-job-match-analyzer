from datetime import datetime, timedelta, timezone

from jose import jwt

from careermatch_ai.core.settings import get_settings


class JWTService:
    def __init__(self) -> None:
        self._settings = get_settings()

    def create_access_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._settings.access_token_expire_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, self._settings.secret_key, algorithm="HS256")

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(token, self._settings.secret_key, algorithms=["HS256"])
