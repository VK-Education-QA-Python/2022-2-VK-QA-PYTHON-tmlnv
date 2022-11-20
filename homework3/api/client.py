import requests
import allure
import json


class ApiClientException(Exception):
    ...


class ApiClient:

    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url

        self.login = login
        self.password = password

        self.session = requests.Session()

        self.headers = {}

    @allure.step("Getting cookies: ssdc, mc, sdc.")
    def first_login(self):
        headers = {
            'Origin': "https://target-sandbox.my.com",
            'Referer': 'https://target-sandbox.my.com/'
        }
        data = {
            'email': self.login,
            'password': self.password,
            'continue': 'https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self.session.post(url='https://auth-ac.my.com/auth', headers=headers, data=data)

    @allure.step("Getting csrftoken cookie.")
    def get_csrf_token(self):
        csrf_request = self.session.get(url='https://target-sandbox.my.com/csrf/')
        csrftoken = csrf_request.headers['set-cookie'].split(';')[0].split('=')[-1]
        self.session.cookies.set('csrftoken', csrftoken)
        self.headers['X-CSRFToken'] = csrftoken

    def auth(self):
        self.first_login()
        self.get_csrf_token()
        data = {
            'email': self.login,
            'password': self.password,
            'continue': 'https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        auth = self.session.post(url='https://auth-ac.my.com/auth', data=data)
        return auth

    @allure.step("Getting id of pocker game source.")
    def get_pocker_game_source_id(self):
        # link = 'https://vk.com/logic_poker'
        poker_game = self.session.get(
            url='https://target-sandbox.my.com/api/v1/vk_apps.json?q=https%3A%2F%2Fvk.com%2Flogic_poker',
            headers=self.headers
        )
        id_of_poker_game = poker_game.json()[0]['id']
        return id_of_poker_game

    @allure.step("Getting id of VK Study group source.")
    def get_vk_study_group_source_id(self):
        # link = 'https://vk.com/vkedu'
        vk_study_group = self.session.get(
            url='https://target-sandbox.my.com/api/v2/vk_groups.json?_q=https%3A%2F%2Fvk.com%2Fvkedu',
            headers=self.headers
        )
        id_of_vk_study_group = vk_study_group.json()['items'][0]['id']
        return id_of_vk_study_group

    @allure.step("Deleting source poker from sources list.")
    def delete_source_poker(self, source_id):
        deleted_source = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/vk_apps/{source_id}.json',
            headers=self.headers
        )
        return deleted_source

    @allure.step("Deleting source VK group from sources list.")
    def delete_source_vk_group(self, source_id):
        deleted_source = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/vk_groups/{source_id}.json',
            headers=self.headers
        )
        return deleted_source

    @allure.step("Adding poker game to sources list.")
    def add_new_apps_and_games_source(self, id_of_poker_game):
        data = '{"object_id": ' + f'{id_of_poker_game}' + '}'
        added_source = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/vk_apps.json',
            headers=self.headers,
            data=data
        )
        id_of_added_source_poker = added_source.json()['id']
        return id_of_added_source_poker

    @allure.step("Adding VK Study group to sources list.")
    def add_new_vk_group_source(self, id_of_vk_study_group):
        data = '{"items":[{"object_id":' + f'{id_of_vk_study_group}' + '}]}'
        added_source = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/vk_groups/bulk.json',
            headers=self.headers,
            data=data
        )
        id_of_added_source_vk_group = added_source.json()['items'][0]['id']
        return id_of_added_source_vk_group

    @allure.step("Adding new segment based on source.")
    def add_new_segment(self, file_path, id_of_source):
        with open(f'{file_path}', 'r') as file:
            jsn_data = json.loads(file.read())
            jsn_data['relations'][0]['params']['source_id'] = id_of_source
            data = json.dumps(jsn_data)
        added_segment = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/segments.json',
            headers=self.headers,
            data=data
        )
        added_segment_id = added_segment.json()['id']
        return added_segment, added_segment_id

    @allure.step("Deleting created audience segment.")
    def delete_segment(self, segment_to_delete):
        deleted_segment = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/segments/{segment_to_delete}.json',
            headers=self.headers
        )
        return deleted_segment

    @allure.step("Creating new campaign.")
    def create_new_campaign(self, file_path_campaign, id_big_pic, id_small_pic, id_primary):
        with open(f'{file_path_campaign}', 'r') as file:
            jsn_data = json.loads(file.read())
            jsn_data['banners'][0]['urls']['primary']['id'] = id_primary
            jsn_data['banners'][0]['content']['image_1080x607']['id'] = id_big_pic
            jsn_data['banners'][0]['content']['icon_256x256']['id'] = id_small_pic
            data = json.dumps(jsn_data)
        added_campaign = self.session.post(
            url='https://target-sandbox.my.com/api/v2/campaigns.json',
            headers=self.headers,
            data=data
        )
        id_of_created_campaign = added_campaign.json()['id']
        return added_campaign, id_of_created_campaign

    @allure.step("Deleting campaign.")
    def delete_campaign(self, id_campaign):
        deleted_campaign = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/campaigns/{id_campaign}.json',
            headers=self.headers,
        )
        return deleted_campaign

    @allure.step("Uploading 1080x607 image.")
    def big_pic_upload(self, file_path_big):
        with open(f"{file_path_big}", "rb") as image:
            f = image.read()
            binary_file = bytearray(f)
        file = {'file': ('srvvr_cover.png', binary_file)}
        uploaded_big_pic = self.session.post(
            url='https://target-sandbox.my.com/api/v2/content/static.json',
            headers=self.headers,
            files=file
        )
        id_big_pic = uploaded_big_pic.json()['id']
        return id_big_pic

    @allure.step("Uploading 256x256 image.")
    def small_pic_upload(self, file_path_small):
        with open(f"{file_path_small}", "rb") as image:
            f = image.read()
            binary_file = bytearray(f)
        file = {'file': ('srvvr_logo_cut.jpeg', binary_file)}
        uploaded_small_pic = self.session.post(
            url='https://target-sandbox.my.com/api/v2/content/static.json',
            headers=self.headers,
            files=file
        )
        id_pic_small = uploaded_small_pic.json()['id']
        return id_pic_small

    @allure.step("Getting primary id.")
    def get_primary_id_banner(self):
        primary_id = self.session.get(
            url='https://target-sandbox.my.com/api/v2/campaign_objective/general_ttm/urls.json',
            headers=self.headers
        )
        id_primary = primary_id.json()['items'][0]['id']
        return id_primary

    @allure.step("Checking campaign.")
    def check_campaign(self, campaign_id):
        check_ = self.session.get(
            url=f'https://target-sandbox.my.com/api/v2/campaigns/{campaign_id}.json?fields=id,name,status',
            headers=self.headers
        )
        return check_.json()

    @allure.step("Cheking segment.")
    def check_segment(self, segment_id):
        check_ = self.session.get(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/segments/{segment_id}.json?fields=id,name,created',
            headers=self.headers
        )
        return check_.json()
