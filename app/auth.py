import os
import json
import urllib.request

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Auth0 configuration
AUTH0_DOMAIN = os.getenv(
    "AUTH0_DOMAIN",
    "dev-xnilgkpf7p7ikpau.us.auth0.com"
)

AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

if not AUTH0_CLIENT_ID:
    raise ValueError("AUTH0_CLIENT_ID is not set in .env")

AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_auth0_id_token(id_token: str) -> dict:
    """
    Verify an Auth0 ID token and return its claims.
    """

    try:
        # Get Auth0 public keys
        with urllib.request.urlopen(
            AUTH0_JWKS_URL,
            timeout=10
        ) as response:
            jwks = json.loads(
                response.read().decode("utf-8")
            )

        # Read token header
        unverified_header = jwt.get_unverified_header(
            id_token
        )

        rsa_key = None

        for key in jwks["keys"]:
            if key["kid"] == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break

        if not rsa_key:
            raise ValueError(
                "Auth0 signing key not found"
            )

        # Verify signature, issuer and audience
        payload = jwt.decode(
            id_token,
            rsa_key,
            algorithms=["RS256"],
            audience=AUTH0_CLIENT_ID,
            issuer=AUTH0_ISSUER
        )

        # Require a verified email
        if not payload.get("email"):
            raise ValueError(
                "Email not found in Auth0 token"
            )

        if payload.get("email_verified") is not True:
            raise ValueError(
                "Auth0 email is not verified"
            )

        return payload

    except Exception as e:
        raise ValueError(
            f"Invalid Auth0 ID token: {str(e)}"
        )