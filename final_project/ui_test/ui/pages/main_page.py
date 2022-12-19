from ui.pages.base_page import BasePage
from ui.locators import MainPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException


class MainPage(BasePage):

    def find_logout_button(self):
        if self.delay_check(MainPageLocators.LOGOUT_BUTTON):
            return True
        else:
            return False

    def move_cursor_to_element(self, locator):
        action = ActionChains(self.driver)
        element = self.delay_check(locator)
        action.move_to_element(element)
        action.perform()

    def click_dropdown_elem(self, locator_dropdown_menu, locator_element):
        self.move_cursor_to_element(locator_dropdown_menu)
        self.visibility_check(locator_element)
        self.click(locator_element)

    def click_dropdown_and_switch_to_tab(self, locator_dropdown_menu, locator_element):
        self.click_dropdown_elem(locator_dropdown_menu=locator_dropdown_menu,
                                 locator_element=locator_element)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def click_and_switch_to_tab(self, locator_element):
        self.click(locator_element)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def click_on_tm_ver(self):
        self.click(MainPageLocators.TM_VESRION_NAVBAR)

    def click_home_button(self):
        self.click(MainPageLocators.HOME_BUTTON_NAVBAR)

    def click_python_button(self):
        # self.click(MainPageLocators.PYTHON_BUTTON_NAVBAR)
        self.click_dropdown_and_switch_to_tab(MainPageLocators.PYTHON_BUTTON_NAVBAR,
                                              MainPageLocators.PYTHON_BUTTON_NAVBAR)

    def click_python_history_button(self):
        # self.click_dropdown_elem(locator_dropdown_menu=MainPageLocators.PYTHON_BUTTON_NAVBAR,
        #                          locator_element=MainPageLocators.PYTHON_HISTORY_DROPDOWN_NAVBAR)
        self.click_dropdown_and_switch_to_tab(locator_dropdown_menu=MainPageLocators.PYTHON_BUTTON_NAVBAR,
                                              locator_element=MainPageLocators.PYTHON_HISTORY_DROPDOWN_NAVBAR)

    def click_about_flask_button(self):
        self.click_dropdown_and_switch_to_tab(locator_dropdown_menu=MainPageLocators.PYTHON_BUTTON_NAVBAR,
                                              locator_element=MainPageLocators.ABOUT_FLASK_DROPDOWN_NAVBAR)

    def click_centos7_button(self):
        self.click_dropdown_and_switch_to_tab(locator_dropdown_menu=MainPageLocators.LINUX_BUTTON_NAVBAR,
                                              locator_element=MainPageLocators.DOWNLOAD_CENTOS7_DROPDOWN_NAVBAR)

    def click_wireshark_news_button(self):
        self.click_dropdown_and_switch_to_tab(locator_dropdown_menu=MainPageLocators.NETWORK_BUTTON_NAVBAR,
                                              locator_element=MainPageLocators.WIRESHARK_NEWS_DROPDOWN_NAVBAR)

    def click_wireshark_download_button(self):
        self.click_dropdown_and_switch_to_tab(locator_dropdown_menu=MainPageLocators.NETWORK_BUTTON_NAVBAR,
                                              locator_element=MainPageLocators.WIRESHARK_DOWNLOAD_DROPDOWN_NAVBAR)

    def click_tcdump_examples_button(self):
        self.click_dropdown_and_switch_to_tab(locator_dropdown_menu=MainPageLocators.NETWORK_BUTTON_NAVBAR,
                                              locator_element=MainPageLocators.TCDUMP_EXAMPLES_DROPDOWN_NAVBAR)

    def check_username_credentials(self):
        return self.delay_check(MainPageLocators.LOGGED_AS)

    def check_name_surname_credentials(self):
        return self.delay_check(MainPageLocators.USER)

    def check_vk_id(self):
        return self.delay_check(MainPageLocators.VK_ID)

    def logout(self):
        self.click(MainPageLocators.LOGOUT_BUTTON)

    def click_what_is_an_api(self):
        self.click_and_switch_to_tab(MainPageLocators.WHAT_IS_AN_API)

    def click_future_of_internet(self):
        self.click_and_switch_to_tab(MainPageLocators.FUTURE_OF_INTERNET)

    def click_smtp(self):
        self.click_and_switch_to_tab(MainPageLocators.LETS_TALKS_ABOUT_SMTP)

    def find_fact_about_python(self):
        return self.delay_check(MainPageLocators.FOOTER_TEXT_ABOUT_PYTHON)

    def find_vk_edu_copyright(self):
        return self.delay_check(MainPageLocators.POWERED_BY_VK_EDUCATION)

    def check_header_visible(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(MainPageLocators.HOME_BUTTON_NAVBAR))
            return True
        except TimeoutException:
            return False
