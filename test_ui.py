import pytest
from selenium import webdriver
from ui_class_page import ui_class
import allure


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    """Фикстура для создания и завершения сессии браузера."""
    yield driver
    driver.quit()  # Закрываем браузер после завершения теста


@pytest.mark.ui
@allure.title("Кнопка 'Оценить'")
@allure.description("При нажатии на кнопку 'Оценить' ниже появляется "
                    + "табличка для проставления звёзд рейтинга")
@allure.suite("Функциональное тестирование пользовательского интерфейса")
@allure.feature('UI функциональность')
@allure.story('Проверка кнопки "Оценить" и появления таблички с рейтингом')
@allure.severity(allure.severity_level.CRITICAL)
def test_click_rate_button(driver):
    """Тест для проверки кнопки 'Оценить' и появления таблички с рейтингом."""
    UIclass = ui_class(driver)
    with allure.step("Нажимаем на кнопку 'Оценить'"):
        UIclass.get_rate_button().click()

    with allure.step("Ожидаем появления таблички с рейтингом"):
        UIclass.wait_for_rating_table()

    with allure.step("Проверяем, что таблица с рейтингом появилась"):
        assert UIclass.get_rating_table().is_displayed()


@pytest.mark.ui
@allure.title("Кнопка 'Перейти в описание'")
@allure.description("При нажатии на кнопку 'Перейти в описание' страница "
                    + "сползает вниз на блок 'Описание и характеристики'")
@allure.suite("Функциональное тестирование пользовательского интерфейса")
@allure.feature('UI функциональность')
@allure.story('Проверка перехода в описание и характеристики')
@allure.severity(allure.severity_level.NORMAL)
def test_go_to_description_and_features(driver):
    UIclass = ui_class(driver)

    with allure.step("Жмём кнопку для перехода в описание и характеристики"):
        UIclass.click_button_go_to_description_and_features()

    with allure.step("Проверяем, что открылось описание и характеристики"):
        description_title = UIclass.get_element_text(
            UIclass.DESCR_SECTION_LOCATOR)
        assert "ОПИСАНИЕ И ХАРАКТЕРИСТИКИ" in description_title


@pytest.mark.ui
@allure.title("Кнопка 'Купить'")
@allure.description("При нажатии на кнопку 'Купить' книга "
                    + "добавляется в корзину, кнопка меняется на 'Оформить'")
@allure.suite("Функциональное тестирование пользовательского интерфейса")
@allure.feature('UI функциональность')
@allure.story('Добавление книги в корзину')
@allure.severity(allure.severity_level.CRITICAL)
def test_add_book_to_cart(driver):
    """Тест для проверки добавления книги в корзину"""
    UIclass = ui_class(driver)

    with allure.step("Добавляем книгу в корзину"):
        UIclass.add_book_to_cart()

    with allure.step("Ожидаем изменения текста кнопки на 'Оформить'"):
        UIclass.wait_for_buy_button_change()

    with allure.step("Проверяем, что текст кнопки изменился на 'Оформить'"):
        assert 'Оформить' in UIclass.get_buy_button().text


@pytest.mark.ui
@allure.title("Кнопка 'Корзина'")
@allure.description("При нажатии на значок 'Корзина' открывается "
                    + "корзина с добавленной нами книгой'")
@allure.suite("Функциональное тестирование пользовательского интерфейса")
@allure.feature('UI функциональность')
@allure.story('Открытие корзины с добавленной книгой')
@allure.severity(allure.severity_level.NORMAL)
def test_open_shopping_cart_with_added_book(driver):
    UIclass = ui_class(driver)

    with allure.step("Добавляем книгу в корзину"):
        UIclass.add_book_to_cart()

    with allure.step("Открываем корзину"):
        UIclass.click_open_cart_button()

    with allure.step("Проверяем, что книга 'Повелитель мух' в корзине"):
        product_title = UIclass.get_element_text(UIclass.PRODUCT_TITLE_LOCATOR)
        assert "Повелитель мух" in product_title


@pytest.mark.ui
@allure.title("Кнопка 'Избранное'")
@allure.description("При нажатии на кнопку 'Избранное' книга добавляется "
                    + "в избранное, кнопка меняет цвет с голубой на зеленую")
@allure.suite("Функциональное тестирование пользовательского интерфейса")
@allure.feature('UI функциональность')
@allure.story('Добавление книги в избранное')
@allure.severity(allure.severity_level.NORMAL)
def test_add_book_to_favorite(driver):
    UIclass = ui_class(driver)

    with allure.step("Нажимаем на кнопку добавления в избранное"):
        UIclass.add_to_favorite_button()

    with allure.step("Ожидаем изменения кнопки избранного"):
        UIclass.wait_for_favorite_button_change()

    with allure.step("Проверяем, что кнопка 'Избранное' видна"):
        assert UIclass.wait_for_favorite_button_change()
