import allure
from base import BaseCase
import pytest


@pytest.mark.UI
class TestAddCampaign(BaseCase):

    @pytest.fixture()
    def create_and_delete_campaign(self):
        self.campaigns_page.full_create_campaign()
        yield
        self.campaigns_page.full_delete_campaign()

    @allure.step("Test of advertising campaign")
    def test_creation_of_advertising_campaign(self, create_and_delete_campaign):
        assert self.campaigns_page.company_created_checking()


@pytest.mark.UI
class TestAudiencesCreation(BaseCase):

    @pytest.fixture()
    def create_and_delete_audience(self):
        self.audiences_page.full_create_audience()
        yield
        self.audiences_page.full_clean_up()

    @allure.step("Test of audiences creation")
    def test_creation_of_audience_segment(self, create_and_delete_audience):
        assert self.audiences_page.segment_created_check()


@pytest.mark.UI
class TestVKStudyAudience(BaseCase):

    @pytest.fixture()
    def create_and_delete_vk_study_audience(self):
        self.audiences_page.full_create_vk_study_audience()
        yield
        self.audiences_page.full_clean_up_vk_study()

    @allure.step("Test of VK Study audience segmentation")
    def test_vk_study_audience(self, create_and_delete_vk_study_audience):
        assert self.audiences_page.vk_study_segment_created_check()
