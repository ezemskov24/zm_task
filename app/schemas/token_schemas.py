from pydantic import BaseModel


class TokenData(BaseModel):
    """
    Базовая схема токена
    """
    sub: str
