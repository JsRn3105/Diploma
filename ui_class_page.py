from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from config import BEARER_TOKEN
from config import TestData
import allure


class ui_class:
    # Локаторы как атрибуты класса
    RATE_BUTTON_LOCATOR = 'button.product-info-stars__btn'
    RATING_TABLE_LOCATOR = 'div.product-info-stars__edit--show'
    BUY_BUTTON_LOCATOR = 'button.product-offer-button.chg-app-button--primary'
    CART_ICON_LOCATOR = "svg.header-cart__icon--desktop"
    DESCR_SECTION_LOCATOR = "h2.detail-product__block-title.description-anchor"
    PRODUCT_TITLE_LOCATOR = (
        "a.cart-item__content-title .product-title .product-title__head")
    GO_TO_DESCR_BUTTON_LOCATOR = "a.product-description-short__btn-to"
    FAVORITE_BUTTON_LOCATOR = "product-offer-favorite"
    FAVORITE_BUTTON_LOCATOR_CHANGED = (
        "//div[contains(@class, 'product-offer-header__buttons')]"
        "//button[contains(@class, 'chg-app-button--primary')]")

    def __init__(self, driver):
        self._driver = driver
        self._driver.get(TestData.url_for_ui)
        self._driver.maximize_window()  # Максимизируем окно браузера
        self.set_authorization_cookie()  # Вносим токен авторизации
        self._driver.implicitly_wait(4)  # Ждём 4 секунды для полной прогрузки

    # Метод для поиска элемента с ожиданием
    def find_element_with_wait(self, locator: str,
                               by: By = By.CSS_SELECTOR,
                               wait_time: int = 10) -> WebElement:
        """Ищем элемент с использованием WebDriverWait"""
        return WebDriverWait(self._driver, wait_time).until(
            EC.presence_of_element_located((by, locator)))

    # Метод для клика по элементу
    def click_element(self, locator: str, by: By = By.CSS_SELECTOR) -> None:
        """Кликаем по элементу"""
        element = self.find_element_with_wait(locator, by)
        element.click()

    # Метод для получения текста элемента
    def get_element_text(self, locator: str, by: By = By.CSS_SELECTOR) -> str:
        """Получаем текст элемента"""
        element = self.find_element_with_wait(locator, by)
        return element.text

    # Метод для проверки наличия элемента
    def element_is_present(self, locator: str,
                           by: By = By.CSS_SELECTOR) -> bool:
        """Проверяем, что элемент присутствует на странице"""
        try:
            self.find_element_with_wait(locator, by)
            return True
        except TimeoutException:
            # Если элемент не найден в течение ожидания, возвращаем False
            return False
        except Exception as e:
            # Логируем или обрабатываем другие исключения, если нужно
            print(f"Произошла ошибка при поиске элемента: {e}")
            return False

    def set_authorization_cookie(self) -> None:
        """Добавляем cookie с токеном авторизации"""
        self._driver.add_cookie({
            'name': 'access-token',
            'value': BEARER_TOKEN,
            'domain': '.chitai-gorod.ru',
            'path': '/',
            'secure': False,
            'httpOnly': True})
        self._driver.refresh()

    @allure.step("Получаем кнопку 'Оценить'")
    def get_rate_button(self) -> WebElement:
        """Получаем кнопку 'Оценить'"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CSS_SELECTOR, self.RATE_BUTTON_LOCATOR)

    @allure.step("Получаем кнопку 'Купить'")
    def get_buy_button(self) -> WebElement:
        """Получаем кнопку 'Купить'"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CSS_SELECTOR, self.BUY_BUTTON_LOCATOR)

    @allure.step("Получаем иконку корзины")
    def get_cart_icon(self) -> WebElement:
        """Получаем иконку корзины"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CSS_SELECTOR, self.CART_ICON_LOCATOR)

    @allure.step("Получаем кнопку 'Избранное'")
    def get_favorite_button(self) -> WebElement:
        """Получаем кнопку добавления в избранное"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CLASS_NAME, self.FAVORITE_BUTTON_LOCATOR)

    @allure.step("Нажимаем кнопку 'Избранное'")
    def add_to_favorite_button(self) -> None:
        """Добавляем книгу в избранное"""
        self.get_favorite_button().click()

    @allure.step("Ожидаем изменения кнопки избранного")
    def wait_for_favorite_button_change(self) -> bool:
        """Ожидаем изменения кнопки избранного (например, изменение класса)"""
        # Используем переменную для локатора
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, self.FAVORITE_BUTTON_LOCATOR_CHANGED)))
        # Проверяем, отображается ли кнопка
        favorite_button = self._driver.find_element(
            By.XPATH, self.FAVORITE_BUTTON_LOCATOR_CHANGED)
        is_displayed = favorite_button.is_displayed()
        # Логируем информацию в отчет Allure
        allure.attach(f"Кнопка 'Избранное' отображается: {is_displayed}",
                      name="Проверка отображения кнопки",
                      attachment_type=allure.attachment_type.TEXT)
        return is_displayed

    @allure.step("Проверяем, что кнопка 'Избранное' активна на странице")
    def is_favorite_button_displayed(self) -> bool:
        """Проверяем, что кнопка 'Избранное' активна на странице"""
        return self.get_favorite_button().is_displayed()

    @allure.step("Получаем название продукта")
    def get_product_title(self) -> WebElement:
        """Получаем название продукта"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CSS_SELECTOR, self.PRODUCT_TITLE_LOCATOR)

    @allure.step("Получаем таблицу с рейтингом")
    def get_rating_table(self) -> WebElement:
        """Получаем таблицу с рейтингом"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CSS_SELECTOR, self.RATING_TABLE_LOCATOR)

    @allure.step("Нажимаем на кнопку 'Оценить'")
    def click_rate_button(self) -> None:
        """Нажимаем на кнопку 'Оценить'"""
        # Используем переменную для локатора
        rate_button = self._driver.find_element(
            By.CSS_SELECTOR, self.RATE_BUTTON_LOCATOR)
        WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable(rate_button))
        rate_button.click()

    @allure.step("Ожидаем появления таблички с рейтингом")
    def wait_for_rating_table(self) -> None:
        """Ожидаем появления таблички с рейтингом"""
        # Используем переменную для локатора
        WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, self.RATING_TABLE_LOCATOR)))

    @allure.step("Добавляем книгу в корзину")
    def add_book_to_cart(self) -> None:
        """Добавляем книгу в корзину"""
        self.get_buy_button().click()

    @allure.step("Ожидаем изменения текста кнопки на 'Оформить'")
    def wait_for_buy_button_change(self) -> None:
        """Ожидаем изменения текста кнопки с 'Купить' на 'Оформить'"""
        # Используем переменную для локатора
        WebDriverWait(self._driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, self.BUY_BUTTON_LOCATOR), 'Оформить'))

    @allure.step("Открываем корзину")
    def click_open_cart_button(self) -> None:
        """Открываем корзину"""
        self.get_cart_icon().click()

    @allure.step("Ожидаем, пока URL не изменится на ожидаемую часть")
    def wait_for_url_to_contain(self, expected_url_part: str) -> None:
        """Ожидаем, пока URL не изменится на ожидаемую часть"""
        WebDriverWait(self._driver, 10).until(
            EC.url_contains(expected_url_part))

    @allure.step("Переходим в описание и характеристики")
    def click_button_go_to_description_and_features(self) -> WebElement:
        """Нажимаем кнопку для перехода в описание и характеристики"""
        # Прокручиваем страницу до элемента с наличием товара
        availability_element = self._driver.find_element(
            By.CSS_SELECTOR, self.GO_TO_DESCR_BUTTON_LOCATOR)
        self._driver.execute_script(
            "arguments[0].scrollIntoView(true);", availability_element)
        button_go_to_descr = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, self.GO_TO_DESCR_BUTTON_LOCATOR)))
        button_go_to_descr.click()
        description_section = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, self.DESCR_SECTION_LOCATOR)))
        return description_section

    @allure.step("Получаем раздел с описанием и характеристиками")
    def get_description_section(self) -> WebElement:
        """Получаем раздел с описанием и характеристиками"""
        # Используем переменную для локатора
        return self._driver.find_element(
            By.CSS_SELECTOR, self.DESCR_SECTION_LOCATOR)
