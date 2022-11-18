import os

import allure
import pytest
import json

from base import ApiBase


@pytest.mark.API
class TestApi(ApiBase):

    @pytest.fixture()
    def file_path_big(self, repo_root):
        return os.path.join(repo_root, 'files', 'srvvr_cover.png')

    @pytest.fixture()
    def file_path_small(self, repo_root):
        return os.path.join(repo_root, 'files', 'srvvr_logo_cut.jpeg')

    @pytest.fixture()
    def file_path_poker_segment(self, repo_root):
        return os.path.join(repo_root, 'json_data', 'poker_segment.json')

    @pytest.fixture()
    def file_path_vk_study_segment(self, repo_root):
        return os.path.join(repo_root, 'json_data', 'vk_study_segment.json')

    @pytest.fixture()
    def file_path_campaign(self, repo_root):
        return os.path.join(repo_root, 'json_data', 'campaign.json')

    @allure.step("Testing creation of campaign.")
    def test_creation_of_campaign(self, file_path_big, file_path_small, file_path_campaign):
        id_big_pic = self.api_client.big_pic_upload(file_path_big)
        id_small_pic = self.api_client.small_pic_upload(file_path_small)
        id_primary = self.api_client.get_primary_id_banner()
        new_created_campaign, id_of_created_campaign = self.api_client.create_new_campaign(
            file_path_campaign, id_big_pic, id_small_pic, id_primary
        )
        assert new_created_campaign.status_code == 200
        with open(f'{file_path_campaign}', 'r') as file:
            jsn_data = json.loads(file.read())
        assert jsn_data['name'] in self.api_client.check_campaign(id_of_created_campaign).values()
        self.api_client.delete_campaign(id_of_created_campaign)

    @allure.step("Testing creation of and audience segment based on Poker VK game.")
    def test_creation_of_audience_segment(self, file_path_poker_segment):
        id_of_poker_game = self.api_client.get_pocker_game_source_id()
        id_of_poker_game_source = self.api_client.add_new_apps_and_games_source(id_of_poker_game)
        new_created_segment_poker, id_new_created_segment_poker = self.api_client.add_new_segment(
            file_path_poker_segment, id_of_poker_game)
        assert new_created_segment_poker.status_code == 200
        with open(f'{file_path_poker_segment}', 'r') as file:
            jsn_data = json.loads(file.read())
        assert jsn_data['name'] in self.api_client.check_segment(id_new_created_segment_poker).values()
        self.api_client.delete_segment(id_new_created_segment_poker)
        self.api_client.delete_source(id_of_poker_game_source)

    @allure.step("Testing creation of an audience segment based on VK Study group source.")
    def test_creation_of_audience_vk_study_group(self, file_path_vk_study_segment):
        id_of_vk_study_group = self.api_client.get_vk_study_group_source_id()
        id_of_vk_group_source = self.api_client.add_new_vk_group_source(id_of_vk_study_group)
        new_created_segment_vk_study, id_new_created_segment_vk_study = self.api_client.add_new_segment(
            file_path_vk_study_segment, id_of_vk_study_group)
        assert new_created_segment_vk_study.status_code == 200
        with open(f'{file_path_vk_study_segment}', 'r') as file:
            jsn_data = json.loads(file.read())
        assert jsn_data['name'] in self.api_client.check_segment(id_new_created_segment_vk_study).values()
        self.api_client.delete_segment(id_new_created_segment_vk_study)
        self.api_client.delete_source(id_of_vk_group_source)
