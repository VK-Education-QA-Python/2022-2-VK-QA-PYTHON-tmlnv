import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base import BaseCase
import pytest
from ui.basic_locators import BasePageLocators, CampaignPageLocators, AudiencesPageLocators
import os


@pytest.mark.UI
class TestAddCampaign(BaseCase):
    FILE_PATH_BIG = os.path.abspath(os.path.join(os.path.dirname(__file__), './files/srvvr_cover.png'))
    FILE_PATH_SMALL = os.path.abspath(os.path.join(os.path.dirname(__file__), './files/srvvr_logo_cut.jpeg'))

    @allure.step("Test of advertising campaign")
    def test_creation_of_advertising_campaign(self):
        try:
            self.base_page.create_new_campaign(locator=BasePageLocators.CREATE_CAMPAIGN_BUTTON)
            self.campaigns_page.vk_products_button_click(locator=CampaignPageLocators.VK_PRODUCTS_BUTTON)
            self.campaigns_page.link_input(locator=CampaignPageLocators.LINK_INPUT, link="https://vk.com/sr55r")
            self.campaigns_page.widescreen_block_campaign_choose(
                locator=CampaignPageLocators.WIDESCREEN_BLOCK_CAMPAIGN_BUTTON)
            self.campaigns_page.write_campaign_name(locator=CampaignPageLocators.CAMPAIGN_NAME_FIRST_INPUT,
                                                    name="SRVVR CAMPAIGN")
            self.campaigns_page.set_start_date(locator=CampaignPageLocators.CAMPAIGN_DATE_FROM_INPUT, date="15.11.2022")
            self.campaigns_page.set_end_date(locator=CampaignPageLocators.CAMPAIGN_DATE_TO_INPUT, date="30.11.2022")
            self.campaigns_page.set_budget_per_day(locator=CampaignPageLocators.BUDGET_PER_DAY_INPUT, value="1000")
            self.campaigns_page.set_total_budget(locator=CampaignPageLocators.BUDGET_TOTAL_INPUT, value="100000")
            self.campaigns_page.set_add_title(locator=CampaignPageLocators.ADD_TITLE_INPUT, value="SRVVR")
            self.campaigns_page.set_add_text(locator=CampaignPageLocators.ADD_TEXT_INPUT, value="SUBSCRIBE")
            self.campaigns_page.upload_big_image(locator=CampaignPageLocators.UPLOAD_BIG_IMAGE_INPUT,
                                                 file=self.FILE_PATH_BIG)
            self.campaigns_page.upload_small_image(locator=CampaignPageLocators.UPLOAD_SMALL_IMAGE_INPUT,
                                                   file=self.FILE_PATH_SMALL)
            self.campaigns_page.create_campaign_footer_button(
                locator=CampaignPageLocators.CREATE_CAMPAIGN_FOOTER_BUTTON)
            WebDriverWait(self.driver, 40).until(EC.url_to_be("https://target-sandbox.my.com/dashboard#"))
            assert self.campaigns_page.check_company_created(locator=CampaignPageLocators.CAMPAIGN_TITLE_IN_TABLE)
        finally:
            self.campaigns_page.delete_campaign(locator1=CampaignPageLocators.CHECKBOX_ALL_ROWS,
                                                locator2=CampaignPageLocators.ACTIONS_DROP_DOWN,
                                                locator3=CampaignPageLocators.DELETE_BUTTON
                                                )


@pytest.mark.UI
class TestAudiencesCreation(BaseCase):
    NAME = "POKER VK GAME"

    @allure.step("Test of audiences creation")
    def test_creation_of_audience_segment(self):
        try:
            self.audiences_page.setup_audience(locator1=BasePageLocators.CREATE_CAMPAIGN_BUTTON,
                                               locator2=BasePageLocators.AUDIENCE_BUTTON)
            self.audiences_page.add_source_to_audience(locator1=AudiencesPageLocators.APPS_AND_GAMES_IN_SOCIAL_NETWORKS,
                                                       locator2=AudiencesPageLocators.LINK_OR_NAME_INPUT,
                                                       link="https://vk.com/logic_poker",
                                                       locator3=AudiencesPageLocators.SELECT_ALL_BUTTON,
                                                       locator4=AudiencesPageLocators.ADD_SELECTED_BUTTON
                                                       )
            self.audiences_page.move_to_segments_list(locator=AudiencesPageLocators.SEGMENTS_LIST)
            self.audiences_page.create_new_segment(
                locator1=AudiencesPageLocators.CREATE_NEW_SEGMENT_BUTTON,
                locator2=AudiencesPageLocators.APP_CHECKBOX,
                locator3=AudiencesPageLocators.SUBMIT_BUTTON,
                locator4=AudiencesPageLocators.SEGMENT_NAME_INPUT,
                name=self.NAME,
                locator5=AudiencesPageLocators.CREATE_SEGMENT_BUTTON,
                locator6=AudiencesPageLocators.CREATE_SEGMENT_BUTTON_IF_SEGMENT_EXISTS,
                locator_group=AudiencesPageLocators.ADDING_SEGMENTS_GAMES
            )
            self.audiences_page.check_segments_table_exists(locator=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS)
            self.driver.refresh()
            assert self.audiences_page.check_segment_created(locator=AudiencesPageLocators.SEGMENT_IN_SEGMENTS_LIST)
        finally:
            self.audiences_page.clean_up(locator1=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS,
                                         locator2=AudiencesPageLocators.ACTIONS_DROP_DOWN,
                                         locator3=AudiencesPageLocators.REMOVE,
                                         locator4=AudiencesPageLocators.APPS_AND_GAMES_IN_SOCIAL_NETWORKS,
                                         locator5=AudiencesPageLocators.CROSS_REMOVE,
                                         locator6=AudiencesPageLocators.BUTTON_CONFIRM_REMOVE,
                                         locator_search=AudiencesPageLocators.SEARCH_BY_NAME,
                                         name=self.NAME,
                                         suggester_locator=AudiencesPageLocators.LI_SUGGESTER_MODULE_TO_DELETE,
                                         url_to_be="https://target-sandbox.my.com/segments/apps_games_list"
                                         )


@pytest.mark.UI
class TestVKStudyAudience(BaseCase):
    NAME = "VK STUDY GROUP"

    @allure.step("Test of VK Study audience segmentation")
    def test_vk_study_audience(self):
        try:
            self.audiences_page.setup_audience(locator1=BasePageLocators.CREATE_CAMPAIGN_BUTTON,
                                               locator2=BasePageLocators.AUDIENCE_BUTTON)
            self.audiences_page.add_source_to_audience(locator1=AudiencesPageLocators.GROUPS_OK_AND_VK,
                                                       locator2=AudiencesPageLocators.LINK_OR_NAME_INPUT,
                                                       link="https://vk.com/vkedu",
                                                       locator3=AudiencesPageLocators.SELECT_ALL_BUTTON,
                                                       locator4=AudiencesPageLocators.ADD_SELECTED_BUTTON
                                                       )
            self.audiences_page.move_to_segments_list(locator=AudiencesPageLocators.SEGMENTS_LIST)
            self.audiences_page.create_new_segment(
                locator1=AudiencesPageLocators.CREATE_NEW_SEGMENT_BUTTON,
                locator2=AudiencesPageLocators.APP_CHECKBOX,
                locator3=AudiencesPageLocators.SUBMIT_BUTTON,
                locator4=AudiencesPageLocators.SEGMENT_NAME_INPUT,
                name=self.NAME,
                locator5=AudiencesPageLocators.CREATE_SEGMENT_BUTTON,
                locator_group=AudiencesPageLocators.ADDING_SEGMENTS_GROUPS_OK_AND_VK,
                locator6=AudiencesPageLocators.CREATE_SEGMENT_BUTTON_IF_SEGMENT_EXISTS
            )
            self.audiences_page.check_segments_table_exists(locator=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS)
            self.driver.refresh()
            assert self.audiences_page.check_segment_created(
                locator=AudiencesPageLocators.SEGMENT_VK_GROUP_IN_SEGMENTS_LIST)
        finally:
            self.audiences_page.clean_up(locator1=AudiencesPageLocators.ID_CHECKBOX_ALL_ELEMENTS,
                                         locator2=AudiencesPageLocators.ACTIONS_DROP_DOWN,
                                         locator3=AudiencesPageLocators.REMOVE,
                                         locator4=AudiencesPageLocators.GROUPS_OK_AND_VK,
                                         locator5=AudiencesPageLocators.CROSS_REMOVE,
                                         locator6=AudiencesPageLocators.BUTTON_CONFIRM_REMOVE,
                                         locator_search=AudiencesPageLocators.SEARCH_BY_NAME,
                                         name=self.NAME,
                                         suggester_locator=AudiencesPageLocators.LI_SUGGESTER_MODULE_TO_DELETE,
                                         url_to_be="https://target-sandbox.my.com/segments/groups_list"
                                         )
