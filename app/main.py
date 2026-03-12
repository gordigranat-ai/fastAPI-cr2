from fastapi import FastAPI
from app import auth, products, headers

app = FastAPI(title="Контрольная работа №2", 
              description="Технологии разработки серверных приложений")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(headers.router)

# Задание 3.1 - Создание пользователя
from app.models import UserCreate

@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate):
    """
    Создание пользователя с валидацией данных
    """
    # Просто возвращаем полученные данные
    return user

@app.get("/")
async def root():
    return {
        "message": "Контрольная работа №2",
        "endpoints": [
            "/create_user (POST) - создание пользователя",
            "/product/{product_id} (GET) - получение продукта",
            "/products/search (GET) - поиск продуктов",
            "/login (POST) - вход в систему",
            "/user (GET) - профиль пользователя",
            "/login-signed (POST) - вход с подписью",
            "/profile (GET) - профиль с подписью",
            "/login-session (POST) - вход с динамической сессией",
            "/profile-session (GET) - профиль с динамической сессией",
            "/headers (GET) - получение заголовков",
            "/headers-model (GET) - получение заголовков через модель",
            "/info (GET) - информация с заголовками"
        ]
    }