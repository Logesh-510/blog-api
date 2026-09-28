from secrets import token_urlsafe

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth import (
    create_access_token,
    hash_password,
    verify_password,
    verify_auth0_id_token
)
from ..database import get_db
from ..models import User
from ..schemas import Token, UserRegister, UserResponse
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        (User.email == form_data.username) |
        (User.username == form_data.username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
    "/auth0-login",
    response_model=Token
)
def auth0_login(
    id_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Authenticate a user using an Auth0 ID token.

    If the Auth0 email already exists in our database,
    the existing user is used.

    Otherwise, a new local user is created.
    """

    # 1. Verify Auth0 ID token
    try:
        payload = verify_auth0_id_token(id_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    # 2. Get verified Auth0 information
    email = payload.get("email")
    auth0_name = payload.get("name") or payload.get("nickname")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not available from Auth0"
        )

    # 3. Check whether user already exists
    user = db.query(User).filter(
        User.email == email
    ).first()

    # 4. Create local user if necessary
    if not user:

        # Create a username from Auth0 name/email
        if auth0_name:
            base_username = "".join(
                char for char in auth0_name
                if char.isalnum()
            ).lower()
        else:
            base_username = email.split("@")[0]

        if not base_username:
            base_username = "user"

        base_username = base_username[:50]

        username = base_username
        counter = 1

        while db.query(User).filter(
            User.username == username
        ).first():

            suffix = str(counter)
            username = (
                base_username[:50 - len(suffix)]
                + suffix
            )

            counter += 1

        # OAuth users don't need a normal password.
        # We still store a secure random hash because
        # the existing database column requires a password.
        random_password = token_urlsafe(32)
        hashed_password = hash_password(random_password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # 5. Generate our existing FastAPI JWT
    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user