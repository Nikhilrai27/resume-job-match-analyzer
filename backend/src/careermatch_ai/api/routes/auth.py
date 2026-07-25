from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from careermatch_ai.application.dto.schemas import GoogleAuthRequest, TokenResponse, UserCreateRequest, UserLoginRequest, UserResponse
from careermatch_ai.api.dependencies import get_database
from careermatch_ai.infrastructure.auth.google_oauth import GoogleOAuthService
from careermatch_ai.infrastructure.auth.jwt_service import JWTService
from careermatch_ai.infrastructure.auth.password import hash_password, verify_password
from careermatch_ai.infrastructure.repositories.user_repository import UserRepository


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreateRequest, db: Session = Depends(get_database)) -> UserResponse:
    repository = UserRepository(db)
    if repository.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")
    user = repository.create(payload.email, hash_password(payload.password), payload.full_name)
    return UserResponse.model_validate(user, from_attributes=True)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_database)) -> TokenResponse:
    repository = UserRepository(db)
    user = repository.get_by_email(payload.email)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    return TokenResponse(access_token=JWTService().create_access_token(user.id))


@router.post("/google", response_model=TokenResponse)
async def google_login(payload: GoogleAuthRequest, db: Session = Depends(get_database)) -> TokenResponse:
    google_user = await GoogleOAuthService().verify_id_token(payload.id_token)
    repository = UserRepository(db)
    email = google_user["email"]
    user = repository.get_by_email(email)
    if user is None:
        user = repository.create(email, hash_password(google_user["sub"]), google_user.get("name", email), oauth_provider="google")
    return TokenResponse(access_token=JWTService().create_access_token(user.id))
