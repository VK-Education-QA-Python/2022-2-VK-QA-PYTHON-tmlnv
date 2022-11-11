import allure
from ui.pages.base_page import BasePage
from ui.basic_locators import CampaignPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class CampaignsPage(BasePage):
    FILE_PATH_BIG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../files/srvvr_cover.png'))
    FILE_PATH_SMALL = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../files/srvvr_logo_cut.jpeg'))

    @allure.step("Choosing VK Product")
    def vk_products_button_click(self, locator):
        vk_products_button = self.delay_check(locator)
        vk_products_button.click()

    @allure.step("Inserting link of vk community")
    def link_input(self, locator, link):
        link_input = self.delay_check(locator)
        link_input.clear()
        link_input.send_keys(link)

    @allure.step("Choosing widescreen block campaign in newsletter for Media Agency")
    def widescreen_block_campaign_choose(self, locator):
        widescreen_block = self.delay_check(locator)
        widescreen_block.click()

    @allure.step("Writing campaign name")
    def write_campaign_name(self, locator, name):
        campaign_name = self.delay_check(locator)
        campaign_name.clear()
        campaign_name.send_keys(name)

    @allure.step("Setting campaign start date")
    def set_start_date(self, locator, date):
        campaign_start = self.delay_check(locator)
        campaign_start.send_keys(date)

    @allure.step("Setting campaign end date")
    def set_end_date(self, locator, date):
        campaign_end = self.delay_check(locator)
        campaign_end.send_keys(date)

    @allure.step("Setting budget per day")
    def set_budget_per_day(self, locator, value):
        budget_per_day = self.delay_check(locator)
        budget_per_day.clear()
        budget_per_day.send_keys(value)

    @allure.step("Setting total budget")
    def set_total_budget(self, locator, value):
        budget_per_day = self.delay_check(locator)
        budget_per_day.clear()
        budget_per_day.send_keys(value)

    @allure.step("Setting add title")
    def set_add_title(self, locator, value):
        add_title_input = self.delay_check(locator)
        add_title_input.clear()
        add_title_input.send_keys(value)

    @allure.step("Setting add text")
    def set_add_text(self, locator, value):
        add_text_input = self.delay_check(locator)
        add_text_input.clear()
        add_text_input.send_keys(value)

    @allure.step("Uploading big image")
    def upload_big_image(self, locator, file):
        upload_big_image = self.delay_check(locator)
        upload_big_image.send_keys(file)

    @allure.step("Uploading small image")
    def upload_small_image(self, locator, file):
        upload_big_image = self.delay_check(locator)
        upload_big_image.send_keys(file)

    @allure.step("Pressing create campaign footer button")
    def create_campaign_footer_button(self, locator):
        create_campaign_footer_button = self.delay_check(locator)
        create_campaign_footer_button.click()

    @allure.step("Checking company was created")
    def check_company_created(self, locator):
        created_company = self.delay_check(locator)
        return created_company

    @allure.step("Deleting created campaign")
    def delete_campaign(self, locator_checkbox, locator_drop_down, locator_delete):
        checkbox_to_delete = self.delay_check(locator_checkbox)
        checkbox_to_delete.click()
        dropdown_to_delete = self.delay_check(locator_drop_down)
        dropdown_to_delete.click()
        delete_button = self.delay_check(locator_delete)
        delete_button.click()
        self.driver.refresh()

    @allure.step("Creating new campaign")
    def create_new_campaign(self, locator):
        create_button = self.delay_check(locator)
        create_button.click()

    def full_create_campaign(self):
        self.create_new_campaign(locator=CampaignPageLocators.CREATE_CAMPAIGN_BUTTON)
        self.vk_products_button_click(locator=CampaignPageLocators.VK_PRODUCTS_BUTTON)
        self.link_input(locator=CampaignPageLocators.LINK_INPUT, link="https://vk.com/sr55r")
        self.widescreen_block_campaign_choose(
            locator=CampaignPageLocators.WIDESCREEN_BLOCK_CAMPAIGN_BUTTON)
        self.write_campaign_name(locator=CampaignPageLocators.CAMPAIGN_NAME_FIRST_INPUT,
                                 name="SRVVR CAMPAIGN")
        self.set_start_date(locator=CampaignPageLocators.CAMPAIGN_DATE_FROM_INPUT, date="15.11.2022")
        self.set_end_date(locator=CampaignPageLocators.CAMPAIGN_DATE_TO_INPUT, date="30.11.2022")
        self.set_budget_per_day(locator=CampaignPageLocators.BUDGET_PER_DAY_INPUT, value="1000")
        self.set_total_budget(locator=CampaignPageLocators.BUDGET_TOTAL_INPUT, value="100000")
        self.set_add_title(locator=CampaignPageLocators.ADD_TITLE_INPUT, value="SRVVR")
        self.set_add_text(locator=CampaignPageLocators.ADD_TEXT_INPUT, value="SUBSCRIBE")
        self.upload_big_image(locator=CampaignPageLocators.UPLOAD_BIG_IMAGE_INPUT,
                              file=self.FILE_PATH_BIG)
        self.upload_small_image(locator=CampaignPageLocators.UPLOAD_SMALL_IMAGE_INPUT,
                                file=self.FILE_PATH_SMALL)
        self.create_campaign_footer_button(
            locator=CampaignPageLocators.CREATE_CAMPAIGN_FOOTER_BUTTON)
        WebDriverWait(self.driver, 40).until(EC.url_to_be("https://target-sandbox.my.com/dashboard#"))

    def full_delete_campaign(self):
        self.delete_campaign(locator_checkbox=CampaignPageLocators.CHECKBOX_ALL_ROWS,
                             locator_drop_down=CampaignPageLocators.ACTIONS_DROP_DOWN,
                             locator_delete=CampaignPageLocators.DELETE_BUTTON
                             )

    def company_created_checking(self):
        return self.check_company_created(locator=CampaignPageLocators.CAMPAIGN_TITLE_IN_TABLE)
