from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from uuid import UUID

# Задание 3.1
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    age: Optional[int] = Field(None, ge=1, le=150, description="Возраст пользователя")
    is_subscribed: Optional[bool] = Field(False, description="Подписка на рассылку")

# Модель для продуктов (Задание 3.2)
class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float

# Модель для логина (Задание 5.1)
class LoginRequest(BaseModel):
    username: str
    password: str

# Модель для ответа с пользователем
class UserResponse(BaseModel):
    username: str
    message: str

# Модель для заголовков (Задание 5.4)
class CommonHeaders(BaseModel):
    user_agent: str = Field(..., alias="User-Agent")
    accept_language: str = Field(..., alias="Accept-Language")
    
    @validator('accept_language')
    def validate_accept_language(cls, v):
        # Простая валидация формата Accept-Language
        import re
        pattern = r'^([a-zA-Z]{2}(-[a-zA-Z]{2})?)(;q=[0-1](\.[0-9]+)?)?(,([a-zA-Z]{2}(-[a-zA-Z]{2})?)(;q=[0-1](\.[0-9]+)?)?)*$'
        if not re.match(pattern, v):
            raise ValueError('Неверный формат Accept-Language')
        return v
    
    class Config:
        populate_by_name = True