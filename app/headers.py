from fastapi import APIRouter, Header, Response
from datetime import datetime
from app.models import CommonHeaders

router = APIRouter()

# Задание 5.4 - Простой маршрут /headers
@router.get("/headers")
async def get_headers(
    user_agent: str = Header(...),
    accept_language: str = Header(...)
):
    """
    Возвращает заголовки User-Agent и Accept-Language
    """
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }

# Задание 5.4 - Маршрут с моделью CommonHeaders
@router.get("/headers-model")
async def get_headers_model(headers: CommonHeaders = Header()):
    """
    Возвращает заголовки с использованием модели CommonHeaders
    """
    return headers

# Задание 5.4 - Маршрут /info с расширенным ответом
@router.get("/info")
async def get_info(
    response: Response,
    headers: CommonHeaders = Header()
):
    """
    Возвращает информацию о заголовках с дополнительным полем message
    и HTTP-заголовком X-Server-Time
    """
    # Устанавливаем заголовок с серверным временем
    current_time = datetime.now().isoformat()
    response.headers["X-Server-Time"] = current_time
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }