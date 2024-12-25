import pytest
import allure
from api_class_page import api_class
from config import TestData


# Фикстура для создания экземпляра API-класса
@pytest.fixture
def api_client():
    return api_class()


@pytest.mark.api
@allure.title("Добавление в корзину")
@allure.description("При отправке POST запроса с id книги " +
                    "- эта книга добавляется в корзину")
@allure.suite("Тестирование API-запросов")
@allure.feature('Корзина')
@allure.story('Добавление книги в корзину')
@allure.severity(allure.severity_level.CRITICAL)
def test_add_book_to_cart_positive():
    """
    Тест на добавление книги в корзину.
    """
    api_client = api_class()  # Создаем экземпляр API-класса

    with allure.step("Отправка запроса на добавление книги в корзину"):
        response = api_client.add_book_to_cart(TestData.goods_id_api)

    with allure.step("Проверка кода ответа на успешное добавление книги"):
        # Проверяем, что книга была добавлена в корзину
        assert response.status_code == 200


@pytest.mark.api
@allure.title("Получение содержимого корзины")
@allure.description("При отправке GET запроса в корзину " +
                    "- получаем содержимое корзины")
@allure.suite("Тестирование API-запросов")
@allure.feature('Корзина')
@allure.story('Просмотр корзины с книгой')
@allure.severity(allure.severity_level.NORMAL)
def test_view_shopping_card_with_book_positive():
    """
    Тест на проверку наличия добавленной книги в корзине.
    """
    api_client = api_class()  # Создаем экземпляр API-класса

    with allure.step("Отправка запроса на добавление книги в корзину"):
        response = api_client.add_book_to_cart(TestData.goods_id_api)

    with allure.step("Проверка кода ответа на успешное добавление книги"):
        # Проверяем, что книга была добавлена в корзину
        assert response.status_code == 200

    with allure.step("Получаем содержимое корзины"):
        response_cart = api_client.view_shopping_cart()

    with allure.step("Проверяем, что ответ успешен (200 OK)"):
        assert response_cart.status_code == 200

    with allure.step("Получаем список товаров из корзины"):
        cart_items = response_cart.json().get('products', [])

    with allure.step(f"Ищем книгу с названием {TestData.title} в корзине"):
        found_book = None
        for item in cart_items:
            if item.get('title') == TestData.title:
                found_book = item
                break

    with allure.step("Проверяем, что книга найдена в корзине"):
        cart_item_id = found_book.get('id') if found_book else None
        assert cart_item_id is not None


@pytest.mark.api
@allure.title("Удаление книги из корзины")
@allure.description("При отправке DELETE запроса c id книги в корзину " +
                    "- эта книга удаляется из корзины")
@allure.suite("Тестирование API-запросов")
@allure.feature('Корзина')
@allure.story('Удаление книги из корзины')
@allure.severity(allure.severity_level.CRITICAL)
def test_remove_book_from_cart_positive():
    """
    Тест на удаление книги из корзины.
    """
    api_client = api_class()  # Создаем экземпляр API-класса

    # Добавляем книгу в корзину
    with allure.step("Отправка запроса на добавление книги в корзину"):
        response_add = api_client.add_book_to_cart(TestData.goods_id_api)

    with allure.step("Проверка кода ответа на успешное добавление книги"):
        assert response_add.status_code == 200

    # Получаем содержимое корзины
    with allure.step("Получаем содержимое корзины"):
        response_cart = api_client.view_shopping_cart()

    with allure.step("Проверяем, что ответ успешен (200 OK)"):
        assert response_cart.status_code == 200

    with allure.step("Получаем список товаров из корзины"):
        cart_items = response_cart.json().get('products', [])

    # Ищем ID книги в корзине
    with allure.step(f"Ищем книгу с названием {TestData.title} в корзине"):
        found_book = None
        for item in cart_items:
            if item.get('title') == TestData.title:
                found_book = item
                break

    with allure.step("Проверяем, что книга найдена в корзине"):
        cart_item_id = found_book.get('id') if found_book else None
        assert cart_item_id is not None

    # Удаляем книгу из корзины
    with allure.step("Отправка запроса на удаление книги из корзины"):
        response_remove = api_client.remove_book_from_cart(cart_item_id)

    with allure.step("Проверка кода ответа на успешное удаление книги" +
                     "(204 No Content)"):
        assert response_remove.status_code == 204

    # Проверяем, что книга удалена из корзины
    with allure.step("Проверка, что книга удалена из корзины"):
        response_cart_after_removal = api_client.view_shopping_cart()
        assert response_cart_after_removal.status_code == 200
        cart_items_after_removal = response_cart_after_removal.json().get(
            'products', [])
        assert cart_item_id not in [
            item['id'] for item in cart_items_after_removal]


@pytest.mark.api
@allure.title("Добавление в корзину книги с несущестующим id")
@allure.description("При отправке POST запроса с несуществующим id " +
                    "- ожидаем статус-код 500")
@allure.suite("Тестирование API-запросов")
@allure.feature('Корзина')
@allure.story('Добавление несуществующей книги с несуществующим ID в корзину')
@allure.severity(allure.severity_level.CRITICAL)
def test_add_book_with_nonexistent_id_to_cart_negative():
    """
    Тест на добавление несуществующей книги с несуществующим ID в корзину.
    """
    api_client = api_class()  # Создаем экземпляр API-класса

    with allure.step("Отправка запроса на добавление книги " +
                     "с несуществующим ID"):
        response = api_client.add_book_to_cart(TestData.nonexistent_book_id)

    with allure.step("Проверка кода ответа на ошибку добавления " +
                     "(Status Code: 500 Internal Server Error)"):
        # Проверяем, что выдает Status Code: 500 Internal Server Error
        assert response.status_code == 500


@pytest.mark.api
@allure.title("Удаление из корзины книги, которой там нет")
@allure.description("При отправке DELETE запроса с id книги, которой " +
                    "нет в корзине - ожидаем статус-код 404")
@allure.suite("Тестирование API-запросов")
@allure.feature('Корзина')
@allure.story('Удаление книги с неправильным ID из корзины')
@allure.severity(allure.severity_level.CRITICAL)
def test_remove_book_with_wrong_id_from_cart_negative():
    """
    Тест на удаление книги с неправильным ID из корзины.
    """
    api_client = api_class()  # Создаем экземпляр API-класса

    with allure.step("Отправка запроса на удаление книги с неправильным ID"):
        response_remove = api_client.remove_book_from_cart(
            TestData.wrong_book_id)

    with allure.step("Проверка кода ответа на ошибку удаления " +
                     "(404 Not Found)"):
        # Проверяем, что Status Code: 404 Not Found
        assert response_remove.status_code == 404
