import allure
from ui.pages.base_page import BasePage
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
    NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui.basic_locators import BasePageLocators, CampaignPageLocators, AudiencesPageLocators


class AudiencesPage(BasePage):
    url = "https://target.my.com/segments/segments_list"
    exceptions = (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException,
                  ElementNotInteractableException)
    NAME = "POKER VK GAME"
    NAME_VK = "VK STUDY GROUP"

    @allure.step("Setting up the audience page")
    def setup_audience(self, locator_create_campaign, locator_audience_button):
        self.delay_check(locator_create_campaign)
        audiences_button = self.delay_check(locator_audience_button)
        audiences_button.click()

    @allure.step("Adding source to apps and games in social networks segment")
    def add_source_to_audience(self, locator_apps_games, locator_input, link, locator_select_all, locator_add_selected):
        audiences_add = self.delay_check(locator_apps_games)
        audiences_add.click()
        link_or_name_input = self.delay_check(locator_input)
        link_or_name_input.clear()
        link_or_name_input.send_keys(link)
        select_all_button = self.delay_check(locator_select_all)
        select_all_button.click()
        add_selected_button = self.delay_check(locator_add_selected)
        add_selected_button.click()

    @allure.step("Move to segments list")
    def move_to_segments_list(self, locator):
        segments_list = self.delay_check(locator)
        segments_list.click()

    @allure.step("Creating new segment")
    def create_new_segment(self, locator_create_segement, locator_app_checkbox, locator_submit_button,
                           locator_segment_name, name, locator_create_segment, locator_create_button_alternative,
                           locator_group):
        try:
            create_new_segment_button = self.delay_check(locator_create_segement)
            create_new_segment_button.click()
        except self.exceptions:
            create_new_segment_button_exists = self.delay_check(locator_create_button_alternative)
            create_new_segment_button_exists.click()
        choose_groups_vk_ok = self.delay_check(locator_group)
        choose_groups_vk_ok.click()
        app_checkbox = self.delay_check(locator_app_checkbox)
        app_checkbox.click()
        submit_button = self.delay_check(locator_submit_button)
        submit_button.click()
        segment_name_input = self.delay_check(locator_segment_name)
        segment_name_input.clear()
        segment_name_input.send_keys(name)
        create_segment_button = self.delay_check(locator_create_segment)
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
    def clean_up(self, locator_checkbox_all, locator_drop_down, locator_remove, locator_apps_games,
                 locator_cross_remove, locator_confirm_remove, locator_search, name,
                 suggester_locator, url_to_be):
        search_by_name = self.delay_check(locator_search)
        search_by_name.clear()
        search_by_name.send_keys(name)
        suggester_li = self.delay_check(suggester_locator)
        suggester_li.click()
        id_checkbox_all_elements = self.delay_check(locator_checkbox_all)
        id_checkbox_all_elements.click()
        actions_drop_down = self.delay_check(locator_drop_down)
        actions_drop_down.click()
        self.wait_for_element_to_be_clickable(locator_remove)
        remove = self.delay_check(locator_remove)
        remove.click()
        self.driver.refresh()
        self.wait_for_element_to_be_clickable(locator_apps_games)
        audiences_add_2 = self.delay_check(locator_apps_games)
        audiences_add_2.click()
        WebDriverWait(self.driver, 10).until(EC.url_to_be(url_to_be))
        self.wait_for_element_to_be_clickable(locator_cross_remove)
        cross_remove = self.delay_check(locator_cross_remove)
        cross_remove.click()
        self.wait_for_element_to_be_clickable(locator_confirm_remove)
        button_confirm_remove = self.delay_check(locator_confirm_remove)
        button_confirm_remove.click()

    def full_create_audience(self):
        self.setup_audience(locator_create_campaign=CampaignPageLocators.CREATE_CAMPAIGN_BUTTON,
                            locator_audience_button=BasePageLocators.AUDIENCE_BUTTON)
        self.add_source_to_audience(
            locator_apps_games=AudiencesPageLocators.APPS_AND_GAMES_IN_SOCIAL_NETWORKS,
            locator_input=AudiencesPageLocators.LINK_OR_NAME_INPUT,
            link="https://vk.com/logic_poker",
            locator_select_all=AudiencesPageLocators.SELECT_ALL_BUTTON,
            locator_add_selected=AudiencesPageLocators.ADD_SELECTED_BUTTON
        )
        self.move_to_segments_list(locator=AudiencesPageLocators.SEGMENTS_LIST)
        self.create_new_segment(
            locator_create_segement=AudiencesPageLocators.CREATE_NEW_SEGMENT_BUTTON,
            locator_app_checkbox=AudiencesPageLocators.APP_CHECKBOX,
            locator_submit_button=AudiencesPageLocators.SUBMIT_BUTTON,
            locator_segment_name=AudiencesPageLocators.SEGMENT_NAME_INPUT,
            name=self.NAME,
            locator_create_segment=AudiencesPageLocators.CREATE_SEGMENT_BUTTON,
            locator_create_button_alternative=AudiencesPageLocators.CREATE_SEGMENT_BUTTON_IF_SEGMENT_EXISTS,
            locator_group=AudiencesPageLocators.ADDING_SEGMENTS_GAMES
        )
        self.check_segments_table_exists(locator=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS)
        self.driver.refresh()

    def full_clean_up(self):
        self.clean_up(locator_checkbox_all=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS,
                      locator_drop_down=AudiencesPageLocators.ACTIONS_DROP_DOWN,
                      locator_remove=AudiencesPageLocators.REMOVE,
                      locator_apps_games=AudiencesPageLocators.APPS_AND_GAMES_IN_SOCIAL_NETWORKS,
                      locator_cross_remove=AudiencesPageLocators.CROSS_REMOVE,
                      locator_confirm_remove=AudiencesPageLocators.BUTTON_CONFIRM_REMOVE,
                      locator_search=AudiencesPageLocators.SEARCH_BY_NAME,
                      name=self.NAME,
                      suggester_locator=AudiencesPageLocators.LI_SUGGESTER_MODULE_TO_DELETE,
                      url_to_be="https://target-sandbox.my.com/segments/apps_games_list"
                      )

    def segment_created_check(self):
        return self.check_segment_created(locator=AudiencesPageLocators.SEGMENT_IN_SEGMENTS_LIST)

    def full_create_vk_study_audience(self):
        self.setup_audience(locator_create_campaign=CampaignPageLocators.CREATE_CAMPAIGN_BUTTON,
                            locator_audience_button=BasePageLocators.AUDIENCE_BUTTON)
        self.add_source_to_audience(locator_apps_games=AudiencesPageLocators.GROUPS_OK_AND_VK,
                                    locator_input=AudiencesPageLocators.LINK_OR_NAME_INPUT,
                                    link="https://vk.com/vkedu",
                                    locator_select_all=AudiencesPageLocators.SELECT_ALL_BUTTON,
                                    locator_add_selected=AudiencesPageLocators.ADD_SELECTED_BUTTON
                                    )
        self.move_to_segments_list(locator=AudiencesPageLocators.SEGMENTS_LIST)
        self.create_new_segment(
            locator_create_segement=AudiencesPageLocators.CREATE_NEW_SEGMENT_BUTTON,
            locator_app_checkbox=AudiencesPageLocators.APP_CHECKBOX,
            locator_submit_button=AudiencesPageLocators.SUBMIT_BUTTON,
            locator_segment_name=AudiencesPageLocators.SEGMENT_NAME_INPUT,
            name=self.NAME_VK,
            locator_create_segment=AudiencesPageLocators.CREATE_SEGMENT_BUTTON,
            locator_group=AudiencesPageLocators.ADDING_SEGMENTS_GROUPS_OK_AND_VK,
            locator_create_button_alternative=AudiencesPageLocators.CREATE_SEGMENT_BUTTON_IF_SEGMENT_EXISTS
        )
        self.check_segments_table_exists(locator=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS)
        self.driver.refresh()

    def full_clean_up_vk_study(self):
        self.clean_up(locator_checkbox_all=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS,
                      locator_drop_down=AudiencesPageLocators.ACTIONS_DROP_DOWN,
                      locator_remove=AudiencesPageLocators.REMOVE,
                      locator_apps_games=AudiencesPageLocators.GROUPS_OK_AND_VK,
                      locator_cross_remove=AudiencesPageLocators.CROSS_REMOVE,
                      locator_confirm_remove=AudiencesPageLocators.BUTTON_CONFIRM_REMOVE,
                      locator_search=AudiencesPageLocators.SEARCH_BY_NAME,
                      name=self.NAME_VK,
                      suggester_locator=AudiencesPageLocators.LI_SUGGESTER_MODULE_TO_DELETE,
                      url_to_be="https://target-sandbox.my.com/segments/groups_list"
                      )

    def vk_study_segment_created_check(self):
        return self.check_segment_created(locator=AudiencesPageLocators.SEGMENT_VK_GROUP_IN_SEGMENTS_LIST)
