from ui.pages.base_page import BasePage
from ui.locators.locators_android import SettingsPageANDROIDLocators
import allure


class SettingsPage(BasePage):

    def scroll_to_bottom(self):
        pass

    def tap_on_news_source(self):
        pass

    def choose_mail_ru(self):
        pass

    def check_for_selected_source(self):
        pass

    def go_back_to_settings(self):
        pass

    def close_settings(self):
        pass

    def tap_on_about(self):
        pass

    def get_app_version(self):
        pass

    def check_copyright(self):
        pass


class SettingsPageANDROID(SettingsPage):
    locators = SettingsPageANDROIDLocators()

    @allure.step("Scrolling to news source setting.")
    def scroll_to_bottom(self):
        self.swipe_up()
        self.swipe_up()
        self.swipe_up()

    @allure.step("Tapping on news source setting.")
    def tap_on_news_source(self):
        self.click_for_android(self.locators.NEWS_SOURCE)

    @allure.step("Choosing Mail ru as news source.")
    def choose_mail_ru(self):
        self.click_for_android(self.locators.MAIL_RU_SOURCE)

    @allure.step('Checking for selected source.')
    def check_for_selected_source(self):
        return self.find(self.locators.SELECTED_SOURCE)

    @allure.step("Doing back to settings menu.")
    def go_back_to_settings(self):
        self.click_for_android(self.locators.GO_BACK_BUTTON)

    @allure.step("Closing settings.")
    def close_settings(self):
        self.click_for_android(self.locators.CLOSE_MENU_CROSS)

    @allure.step("Tapping on About.")
    def tap_on_about(self):
        self.click_for_android(self.locators.ABOUT)

    @allure.step("Getting app version.")
    def get_app_version(self):
        ver = self.find(self.locators.APP_VERSION)
        return ver.text

    @allure.step("Checking copyright mark exists.")
    def check_copyright(self):
        mark = self.find(self.locators.COPYRIGHT)
        return mark.text
