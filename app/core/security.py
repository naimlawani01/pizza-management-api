from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None, user_data: dict = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    logger.info(f"Creating token with expiration: {expire}")
    logger.info(f"Current time: {datetime.utcnow()}")
    
    to_encode = {
        "exp": int(expire.timestamp()),  # Convertir en timestamp Unix
        "sub": str(subject),
        "type": "access"
    }
    
    # Ajouter les informations de l'utilisateur dans un objet user_info
    if user_data:
        to_encode["user_info"] = {
            "email": user_data.get("email"),
            "username": user_data.get("username"),
            "is_active": user_data.get("is_active"),
            "is_superuser": user_data.get("is_superuser"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name")
        }
    
    logger.info(f"Token payload: {to_encode}")
    logger.info(f"Using secret key (first 10 chars): {settings.SECRET_KEY[:10]}...")
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    
    logger.info(f"Generated token (first 10 chars): {encoded_jwt[:10]}...")
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password) 