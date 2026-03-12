from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import Product

router = APIRouter()

# Задание 3.2 - Пример данных продуктов
sample_products = [
    Product(product_id=123, name="Smartphone", category="Electronics", price=599.99),
    Product(product_id=456, name="Phone Case", category="Accessories", price=19.99),
    Product(product_id=789, name="Iphone", category="Electronics", price=1299.99),
    Product(product_id=101, name="Headphones", category="Accessories", price=99.99),
    Product(product_id=202, name="Smartwatch", category="Electronics", price=299.99)
]

# Задание 3.2 - Получение продукта по ID
@router.get("/product/{product_id}")
async def get_product(product_id: int):
    """
    Получение информации о продукте по ID
    """
    for product in sample_products:
        if product.product_id == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")

# Задание 3.2 - Поиск продуктов
@router.get("/products/search")
async def search_products(
    keyword: str = Query(..., description="Ключевое слово для поиска"),
    category: Optional[str] = Query(None, description="Категория для фильтрации"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество результатов")
):
    """
    Поиск продуктов по ключевому слову и категории
    """
    results = []
    
    for product in sample_products:
        # Проверяем, содержит ли название ключевое слово (регистронезависимо)
        if keyword.lower() in product.name.lower():
            # Если указана категория, фильтруем по ней
            if category and product.category.lower() != category.lower():
                continue
            results.append(product)
    
    # Ограничиваем количество результатов
    return results[:limit]