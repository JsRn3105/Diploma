import pytest
from api_class_page import api_class
from config import TestData
from requests import Response


# Фикстура для очистки корзины и избранного
@pytest.fixture(autouse=True)
def cleanup_cart_and_favorites() -> None:
    """
    Очистка корзины и избранного через API после каждого теста.
    """
    api_client = api_class()

    # 1. Удаление книги из избранного (goodsId = 2398281)
    response_favorites: Response = api_client.get_favorites()
    if response_favorites.status_code == 200:
        favorite_items: list[dict[str, str]
                             ] = response_favorites.json().get('products', [])
        for item in favorite_items:
            if item.get('goodsId') == TestData.goods_id_ui:
                favorite_item_id: int = item.get('id')  # ID книги в избранном
                # Удаляем книгу из избранного
                api_client.remove_book_from_favorite(favorite_item_id)

    # 2. Удаление книги из корзины
    response_cart: Response = api_client.view_shopping_cart()
    if response_cart.status_code == 200:
        cart_items: list[dict[str, str]
                         ] = response_cart.json().get('products', [])

        # Проверяем корзину на наличие книг с нужными goodsId
        for item in cart_items:
            goods_id: int = item.get('goodsId')
            cart_item_id: int = item.get('id')
            if goods_id in (TestData.goods_id_ui, TestData.goods_id_api):
                # Удаляем книгу из корзины по её id
                api_client.remove_book_from_cart(cart_item_id)
