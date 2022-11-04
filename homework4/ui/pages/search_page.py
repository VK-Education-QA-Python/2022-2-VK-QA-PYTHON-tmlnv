from ui.pages.base_page import BasePage
from ui.locators.locators_android import SearchPageANDROIDLocators
import allure


class SearchPage(BasePage):

    def enter_value_in_search_field(self, text):
        pass

    def check_country_info(self):
        pass

    def tap_on_search_button(self):
        pass

    def swipe_to_population(self):
        pass

    def hide_keyboard(self):
        pass

    def tap_on_size_info(self):
        pass

    def size_info(self):
        pass

    def check_calculation_result(self):
        pass

    def check_news(self):
        pass


class SearchPageANDROID(SearchPage):
    locators = SearchPageANDROIDLocators()

    @allure.step("Entering value in search field.")
    def enter_value_in_search_field(self, text):
        self.find(self.locators.SEARCH_FIELD).send_keys(text)

    @allure.step("Checking country info appeared.")
    def check_country_info(self):
        country_info = self.find(self.locators.RUSSIA_INFO)
        return country_info.text

    @allure.step("Tapping send button.")
    def tap_on_search_button(self):
        self.click_for_android(self.locators.SEND_BUTTON)

    @allure.step("Scrolling to population info.")
    def swipe_to_population(self):
        self.swipe_left()
        self.swipe_left()
        self.swipe_left()

    @allure.step("Hiding keyboard.")
    def hide_keyboard(self):
        self.driver.hide_keyboard()

    @allure.step('Tapping on population info block.')
    def tap_on_size_info(self):
        self.click_for_android(self.locators.RUSSIAN_SIZE)

    @allure.step("Population info block checking.")
    def size_info(self):
        text_population = self.find(self.locators.SIZE_SEARCH_RESULT)
        return text_population.text

    @allure.step("Checking calculation result.")
    def check_calculation_result(self):
        calc_res = self.find(self.locators.CALCULATION_RESULT)
        return calc_res.text

    @allure.step("Checking news appeared.")
    def check_news(self):
        news = self.find(self.locators.TURNING_ON_NEWS_LOCATOR)
        return news.text
