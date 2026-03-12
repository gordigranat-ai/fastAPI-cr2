from fastapi import APIRouter, HTTPException, Response, Request, status
from fastapi.responses import JSONResponse
from app.models import LoginRequest
import uuid
import time
from itsdangerous import URLSafeTimedSerializer  
from datetime import datetime

router = APIRouter()

# Секретный ключ для подписи
SECRET_KEY = "your-secret-key-here-change-in-production"
serializer = URLSafeTimedSerializer(SECRET_KEY)  # ИСПРАВЛЕНО: было URSafeTimedSerializer, стало URLSafeTimedSerializer

# Простая база данных пользователей (в реальном проекте используйте настоящую БД)
USERS_DB = {
    "user123": "password123",
    "admin": "admin123"
}

# Хранилище сессий (в реальном проекте используйте Redis или БД)
sessions = {}

# Задание 5.1 - Простая аутентификация
@router.post("/login")
async def login(login_data: LoginRequest, response: Response):
    """
    Простой логин с установкой session_token cookie
    """
    # Проверяем учетные данные
    if login_data.username in USERS_DB and USERS_DB[login_data.username] == login_data.password:
        # Генерируем UUID для сессии
        session_uuid = str(uuid.uuid4())
        
        # Устанавливаем cookie
        response.set_cookie(
            key="session_token",
            value=session_uuid,
            httponly=True,
            max_age=3600,  # 1 час
            secure=False,  # Для тестирования, в продакшене True
            samesite="lax"
        )
        
        # Сохраняем сессию
        sessions[session_uuid] = {
            "username": login_data.username,
            "created_at": time.time()
        }
        
        return {"message": "Login successful", "username": login_data.username}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

# Задание 5.1 - Защищенный маршрут /user
@router.get("/user")
async def get_user(request: Request):
    """
    Защищенный маршрут, требующий аутентификации
    """
    session_token = request.cookies.get("session_token")
    
    if not session_token or session_token not in sessions:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized"}
        )
    
    session_data = sessions[session_token]
    return {
        "username": session_data["username"],
        "message": "User profile information",
        "profile": {
            "username": session_data["username"],
            "member_since": datetime.fromtimestamp(session_data["created_at"]).isoformat()
        }
    }

# Задание 5.2 - Логин с подписью
@router.post("/login-signed")
async def login_signed(login_data: LoginRequest, response: Response):
    """
    Логин с подписанным session_token в формате user_id.signature
    """
    if login_data.username in USERS_DB and USERS_DB[login_data.username] == login_data.password:
        # Генерируем UUID для пользователя
        user_uuid = str(uuid.uuid4())
        
        # Создаем подпись с помощью itsdangerous
        signed_token = serializer.dumps(user_uuid)
        
        # Устанавливаем cookie
        response.set_cookie(
            key="session_token",
            value=signed_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "username": login_data.username}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

# Задание 5.2 - Защищенный маршрут /profile
@router.get("/profile")
async def get_profile(request: Request):
    """
    Защищенный маршрут с проверкой подписи
    """
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized - No session token"}
        )
    
    try:
        # Проверяем подпись
        user_uuid = serializer.loads(session_token, max_age=3600)
        
        return {
            "user_id": user_uuid,
            "message": "Profile information",
            "profile": {
                "user_id": user_uuid,
                "username": "Authenticated User"
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized - Invalid signature"}
        )

# Задание 5.3 - Логин с динамическим временем сессии
@router.post("/login-session")
async def login_session(login_data: LoginRequest, response: Response):
    """
    Логин с сессией, поддерживающей динамическое продление
    """
    if login_data.username in USERS_DB and USERS_DB[login_data.username] == login_data.password:
        # Генерируем UUID
        user_uuid = str(uuid.uuid4())
        current_time = int(time.time())
        
        # Создаем данные для подписи: user_uuid.timestamp
        session_data = f"{user_uuid}.{current_time}"
        signed_token = serializer.dumps(session_data)
        
        # Устанавливаем cookie
        response.set_cookie(
            key="session_token",
            value=signed_token,
            httponly=True,
            max_age=300,  # 5 минут
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "username": login_data.username}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

# Задание 5.3 - Защищенный маршрут с динамическим продлением сессии
@router.get("/profile-session")
async def get_profile_session(request: Request, response: Response):
    """
    Защищенный маршрут с динамическим продлением сессии
    """
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Unauthorized - No session token"}
        )
    
    try:
        # Проверяем подпись
        session_data = serializer.loads(session_token)
        
        # Разбираем данные: user_uuid.timestamp
        parts = session_data.split('.')
        if len(parts) != 2:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Invalid session format"}
            )
        
        user_uuid, last_activity = parts
        last_activity = int(last_activity)
        current_time = int(time.time())
        time_diff = current_time - last_activity
        
        # Проверяем, не истекла ли сессия (более 5 минут)
        if time_diff > 300:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Session expired"}
            )
        
        # Проверяем, нужно ли обновить сессию (прошло от 3 до 5 минут)
        if 180 <= time_diff < 300:
            # Обновляем время
            new_session_data = f"{user_uuid}.{current_time}"
            new_signed_token = serializer.dumps(new_session_data)
            
            response.set_cookie(
                key="session_token",
                value=new_signed_token,
                httponly=True,
                max_age=300,
                secure=False,
                samesite="lax"
            )
            
            return {
                "message": "Session renewed",
                "user_id": user_uuid,
                "profile": {"username": "Authenticated User"}
            }
        
        # Если прошло менее 3 минут, просто возвращаем данные
        return {
            "message": "Profile information",
            "user_id": user_uuid,
            "profile": {"username": "Authenticated User"},
            "session_status": "active"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid session"}
        )