import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.schemas.token_schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Функция для верификации JWT токена

    :param token: JWT токен
    :return: Объект TokenData, содержащий информацию о пользователе
    :raises HTTPException: Если токен недействителен, выбрасывается исключение с кодом 401.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData(sub=payload.get("sub"))
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
