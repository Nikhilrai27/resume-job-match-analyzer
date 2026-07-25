from sqlalchemy.orm import Session

from careermatch_ai.infrastructure.db.models.user import UserModel


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_email(self, email: str) -> UserModel | None:
        return self._db.query(UserModel).filter(UserModel.email == email).one_or_none()

    def create(self, email: str, password_hash: str, full_name: str, oauth_provider: str | None = None) -> UserModel:
        user = UserModel(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            oauth_provider=oauth_provider,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
