import allure
from ui.pages.base_page import BasePage
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException,\
                                       NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AudiencesPage(BasePage):
    url = "https://target.my.com/segments/segments_list"
    exceptions = (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException,
                  ElementNotInteractableException)

    @allure.step("Setting up the audience page")
    def setup_audience(self, locator1, locator2):
        self.delay_check(locator1)
        audiences_button = self.delay_check(locator2)
        audiences_button.click()

    @allure.step("Adding source to apps and games in social networks segment")
    def add_source_to_audience(self, locator1, locator2, link, locator3, locator4):
        audiences_add = self.delay_check(locator1)
        audiences_add.click()
        link_or_name_input = self.delay_check(locator2)
        link_or_name_input.clear()
        link_or_name_input.send_keys(link)
        select_all_button = self.delay_check(locator3)
        select_all_button.click()
        add_selected_button = self.delay_check(locator4)
        add_selected_button.click()

    @allure.step("Move to segments list")
    def move_to_segments_list(self, locator):
        segments_list = self.delay_check(locator)
        segments_list.click()

    @allure.step("Creating new segment")
    def create_new_segment(self, locator1, locator2, locator3, locator4, name, locator5, locator6, locator_group):
        try:
            create_new_segment_button = self.delay_check(locator1)
            create_new_segment_button.click()
        except self.exceptions:
            create_new_segment_button_exists = self.delay_check(locator6)
            create_new_segment_button_exists.click()
        choose_groups_vk_ok = self.delay_check(locator_group)
        choose_groups_vk_ok.click()
        app_checkbox = self.delay_check(locator2)
        app_checkbox.click()
        submit_button = self.delay_check(locator3)
        submit_button.click()
        segment_name_input = self.delay_check(locator4)
        segment_name_input.clear()
        segment_name_input.send_keys(name)
        create_segment_button = self.delay_check(locator5)
        create_segment_button.click()

    @allure.step("Checking table of segments was created")
    def check_segments_table_exists(self, locator):
        existing_table_locator = self.delay_check(locator)
        return existing_table_locator

    @allure.step("Checking segment was created")
    def check_segment_created(self, locator):
        existing_segment_locator = self.delay_check(locator)
        return existing_segment_locator

    def wait_for_element_to_be_clickable(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    @allure.step("Cleaning up")
    def clean_up(self, locator1, locator2, locator3, locator4, locator5, locator6, locator_search, name,
                 suggester_locator, url_to_be):
        search_by_name = self.delay_check(locator_search)
        search_by_name.clear()
        search_by_name.send_keys(name)
        suggester_li = self.delay_check(suggester_locator)
        suggester_li.click()
        id_checkbox_all_elements = self.delay_check(locator1)
        id_checkbox_all_elements.click()
        actions_drop_down = self.delay_check(locator2)
        actions_drop_down.click()
        self.wait_for_element_to_be_clickable(locator3)
        remove = self.delay_check(locator3)
        remove.click()
        self.driver.refresh()
        self.wait_for_element_to_be_clickable(locator4)
        audiences_add_2 = self.delay_check(locator4)
        audiences_add_2.click()
        WebDriverWait(self.driver, 10).until(EC.url_to_be(url_to_be))
        self.wait_for_element_to_be_clickable(locator5)
        cross_remove = self.delay_check(locator5)
        cross_remove.click()
        self.wait_for_element_to_be_clickable(locator6)
        button_confirm_remove = self.delay_check(locator6)
        button_confirm_remove.click()

    @allure.step("Creating new VK OK group segment")
    def create_new_vk_ok_segment(self, locator1, locator2, locator3, locator4, name, locator5, locator_group, locator6):
        try:
            create_new_segment_button = self.delay_check(locator1)
            create_new_segment_button.click()
        except self.exceptions:
            create_new_segment_button_exists = self.delay_check(locator6)
            create_new_segment_button_exists.click()
        choose_groups_vk_ok = self.delay_check(locator_group)
        choose_groups_vk_ok.click()
        app_checkbox = self.delay_check(locator2)
        app_checkbox.click()
        submit_button = self.delay_check(locator3)
        submit_button.click()
        segment_name_input = self.delay_check(locator4)
        segment_name_input.clear()
        segment_name_input.send_keys(name)
        create_segment_button = self.delay_check(locator5)
        create_segment_button.click()
