from fastapi import Request, HTTPException, status

# Здесь можно разместить общие зависимости для всего приложения
# Например, функции проверки аутентификации

def verify_session(request: Request):
    """
    Функция для проверки сессии (может использоваться как зависимость)
    """
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return session_token