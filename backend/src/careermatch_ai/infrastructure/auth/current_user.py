from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from careermatch_ai.api.dependencies import get_database
from careermatch_ai.infrastructure.auth.jwt_service import JWTService
from careermatch_ai.infrastructure.db.models.user import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_database),
) -> UserModel:
    try:
        payload = JWTService().decode_access_token(token)
        user_id = payload.get("sub")
    except JWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        ) from error

    user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found.",
        )

    return user
