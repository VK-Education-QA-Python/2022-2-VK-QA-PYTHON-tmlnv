import allure
import pytest
import os
from base import BaseCase
from time import sleep


@pytest.mark.AndroidUI
class TestMarusyaAndroid(BaseCase):

    @allure.step("Testing Russian population search.")
    def test_size_of_russia_search(self):
        self.main_page.click_on_keyboard_button()
        self.search_page.enter_value_in_search_field('Russia')
        self.search_page.hide_keyboard()
        self.search_page.tap_on_search_button()
        country_info = self.search_page.check_country_info()
        assert 'государство' in country_info
        sleep(3)
        self.search_page.swipe_to_population()
        self.search_page.tap_on_size_info()
        sleep(3)
        res = self.search_page.size_info()
        assert 'км' in res

    @allure.step("Testing calculator.")
    def test_calculator(self):
        self.main_page.click_on_keyboard_button()
        self.search_page.enter_value_in_search_field('2*2')
        self.search_page.hide_keyboard()
        self.search_page.tap_on_search_button()
        calc_res = self.search_page.check_calculation_result()
        assert calc_res == '4'

    @allure.step("Testing news source choosing.")
    def test_news_source_choosing(self):
        self.main_page.click_on_settings_button()
        self.settings_page.scroll_to_bottom()
        self.settings_page.tap_on_news_source()
        self.settings_page.choose_mail_ru()
        assert self.settings_page.check_for_selected_source()
        self.settings_page.go_back_to_settings()
        sleep(3)
        self.settings_page.close_settings()
        self.main_page.click_on_keyboard_button()
        self.search_page.enter_value_in_search_field('News')
        self.search_page.hide_keyboard()
        self.search_page.tap_on_search_button()
        sleep(3)
        news = self.search_page.check_news()
        assert 'новости' in news

    @allure.step("Testing about")
    def test_about(self):
        self.main_page.click_on_settings_button()
        self.settings_page.scroll_to_bottom()
        self.settings_page.tap_on_about()
        in_app_ver = self.settings_page.get_app_version()
        apk_version = os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), './app_file')))[0] \
                          .split('_')[1].split('apk')[0][:-1]
        assert apk_version in in_app_ver
        copy_mark = self.settings_page.check_copyright()
        assert 'Mail.ru Group © 1998–2022. Все права защищены.' in copy_mark
