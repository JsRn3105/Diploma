import requests
from config import BEARER_TOKEN
from typing import Optional
import allure


class api_class:
    def __init__(self) -> None:
        """
        Инициализация клиента для взаимодействия с API.
        Используется токен из BEARER_TOKEN.
        """
        # Токен авторизации из config.py
        self.token: str = BEARER_TOKEN
        self.base_url: str = "https://web-gate.chitai-gorod.ru/api/v1"
        # Драйвер будет инициализирован позже
        self.driver: Optional[None] = None

    def get_headers(self) -> dict[str, str]:
        """
        Возвращает заголовки с авторизацией для запросов.
        """
        headers: dict[str, str] = {
            'Content-Type': 'application/json',
            'Authorization': BEARER_TOKEN,
        }
        # Добавим вывод для проверки заголовков
        print("Headers:", headers)
        return headers

    @allure.step("Добавить книгу в корзину")
    def add_book_to_cart(self, book_id: str, adData: Optional[
                             dict[str, str]] = None) -> requests.Response:
        """
        Добавляет книгу в корзину и возвращает ответ от сервера.
        """
        data: dict[str, str] = {
            "id": book_id,
            "adData": adData or
            {"item_list_name": "catalog-main",
             "product_shelf": ""}
        }
        headers: dict[str, str] = self.get_headers()
        # Выполняем POST-запрос
        try:
            response: requests.Response = requests.post(
                self.base_url + "/cart/product", json=data, headers=headers)
            # Это вызовет исключение для 4xx и 5xx ошибок
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
        return response

    @allure.step("Получить содержимое корзины")
    def view_shopping_cart(self) -> requests.Response:
        """
        Получает содержимое корзины и возвращает ответ от сервера.
        """
        headers: dict[str, str] = self.get_headers()

        # Выполняем GET-запрос для получения корзины
        with allure.step("Отправка запроса для получения корзины"):
            response: requests.Response = requests.get(
                self.base_url + "/cart", headers=headers)
        return response

    @allure.step("Удаление книги из корзины")
    def remove_book_from_cart(self, item_id: str) -> requests.Response:
        """
        Удаляет книгу из корзины по её ID.
        """
        headers: dict[str, str] = self.get_headers()

        # Выполняем DELETE-запрос для удаления товара из корзины
        with allure.step(f"Отправка запроса на удаление книги с ID {item_id}"):
            response: requests.Response = requests.delete(
                self.base_url + f"/cart/product/{item_id}", headers=headers)
        return response

    @allure.step("Получить избранные книги")
    def get_favorites(self) -> requests.Response:
        """
        Получает список книг в избранном.
        """
        headers: dict[str, str] = self.get_headers()
        try:
            response: requests.Response = requests.get(
                self.base_url + "/bookmarks", headers=headers)
            # Это вызовет исключение для 4xx и 5xx ошибок
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
        return response

    @allure.step("Удалить книгу из избранного")
    def remove_book_from_favorite(self, book_id: int) -> requests.Response:
        """
        Удаляет книгу из избранного по ID.
        """
        headers: dict[str, str] = self.get_headers()
        try:
            response: requests.Response = requests.delete(
                f"{self.base_url}/bookmarks/{book_id}", headers=headers)
            response.raise_for_status()  # Проверка на ошибки HTTP
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при удалении книги: {e}")
            return None
        return response
