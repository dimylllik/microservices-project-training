from pwdlib import PasswordHash
import jwt
import os
from dotenv import load_dotenv
from user_schemas import Token
from datetime import UTC, datetime, timedelta

load_dotenv()

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    return password_hash.verify(password, stored_hash)

# jwt
SECRET_KEY = os.environ["jwt_key"]
ALGORITHM = os.environ["algorithm"]

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt