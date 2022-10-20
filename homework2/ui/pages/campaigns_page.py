import allure
from ui.pages.base_page import BasePage


class CampaignsPage(BasePage):
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
    def delete_campaign(self, locator1, locator2, locator3):
        checkbox_to_delete = self.delay_check(locator1)
        checkbox_to_delete.click()
        dropdown_to_delete = self.delay_check(locator2)
        dropdown_to_delete.click()
        delete_button = self.delay_check(locator3)
        delete_button.click()
        self.driver.refresh()
