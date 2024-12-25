# Токен авторизации можнo получить в личном кабинете на сайте
# https://www.chitai-gorod.ru/ через Devtools - Application -
# Cookies - https://www.chitai-gorod.ru/ - access-token.
# Необходимо скопировать значение, вставить в кавычки в переменную ниже,
# заменив 20% после Bearer на пробел. Токен единый для тестов по API и по UI
# Ниже указан недействительный экземпляр токена для демонстрации

BEARER_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIxNzQ5NzAwLCJpYXQiOjE3MzUxMzEyOTIsImV4cCI6MTczNTEzNDg5MiwidHlwZSI6MjB9.kcyIBHfdlDAJ0tK6sE2BZSL5RCzplY_11pp7GeRyspw"  # noqa: E501


class TestData:
    """
    Класс для хранения тестовых данных.
    """
    goods_id_ui = 2398281  # ID книги "Повелитель Мух"
    url_for_ui = "https://www.chitai-gorod.ru/product/povelitel-muh-2398281"
    goods_id_api = 3040344  # ID книги "Город Полумесяца. Дом Пламени и Тени"
    title = "Город Полумесяца. Дом Пламени и Тени"
    nonexistent_book_id = 9999999  # рандомное число, несуществующее ID
    wrong_book_id = 142179123  # ID существующей книги, которой нет в корзине
