from ui.pages.base_page import BasePage
from ui.locators.locators_android import MainPageANDROIDLocators
import allure


class MainPage(BasePage):

    def click_on_keyboard_button(self):
        pass

    def click_on_settings_button(self):
        pass


class MainPageANDROID(MainPage):
    locators = MainPageANDROIDLocators()

    @allure.step("Clicking on keyboard button")
    def click_on_keyboard_button(self):
        self.click_for_android(self.locators.KEYBOARD_BUTTON)

    @allure.step("Clicking on settings button")
    def click_on_settings_button(self):
        self.click_for_android(self.locators.SETTINGS_BUTTON)



