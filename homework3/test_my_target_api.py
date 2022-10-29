import allure
import pytest

from base import ApiBase


@pytest.mark.API
class TestApi(ApiBase):
    @allure.step("Testing creation of campaign.")
    def test_creation_of_campaign(self):
        try:
            self.api_client.big_pic_upload()
            self.api_client.small_pic_upload()
            new_created_campaign = self.api_client.create_new_campaign()
            assert new_created_campaign.status_code == 200
            assert 'id' in new_created_campaign.json()
        finally:
            self.api_client.delete_campaign()

    @allure.step("Testing creation of and audience segment based on Poker VK game.")
    def test_creation_of_audience_segment(self):
        try:
            self.api_client.get_pocker_game_source_id()
            self.api_client.add_new_apps_and_games_source()
            new_created_segment_poker = self.api_client.add_new_segment_poker()
            assert new_created_segment_poker.status_code == 200
            assert 'id' in new_created_segment_poker.json()
        finally:
            self.api_client.delete_segment_poker()
            self.api_client.delete_poker_source()

    @allure.step("Testing creation of an audience segment based on VK Study group source.")
    def test_creation_of_audience_vk_study_group(self):
        try:
            self.api_client.get_vk_study_group_source_id()
            self.api_client.add_new_vk_group_source()
            new_created_segment_poker = self.api_client.add_new_segment_vk_study()
            assert new_created_segment_poker.status_code == 200
            assert 'id' in new_created_segment_poker.json()
        finally:
            self.api_client.delete_segment_vk_study()
            self.api_client.delete_vk_group()
