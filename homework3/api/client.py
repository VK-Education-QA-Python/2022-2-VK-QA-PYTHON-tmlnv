import requests
import allure
import os


class ApiClientException(Exception):
    ...


class ApiClient:
    FILE_PATH_BIG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../files/srvvr_cover.png'))
    FILE_PATH_SMALL = os.path.abspath(os.path.join(os.path.dirname(__file__), '../files/srvvr_logo_cut.jpeg'))

    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url

        self.login = login
        self.password = password

        self.session = requests.Session()

        self.cookies_values = {}

        self.id_of_added_source_vk_group = 0
        self.id_of_added_source_poker = 0
        self.id_of_added_segment_poker = 0
        self.id_of_added_segment_vk_study = 0
        self.id_of_created_campaign = 0
        self.id_of_poker_game = 0
        self.id_of_vk_study_group = 0
        self.id_of_pic_big = 0
        self.id_of_pic_small = 0

    @allure.step("Getting cookies: ssdc, mc, sdc.")
    def get_tokens(self):
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
        auth_request = self.session.post(url='https://auth-ac.my.com/auth', headers=headers, data=data)
        res = {r.url: r.cookies.get_dict() for r in auth_request.history}
        ssdc_token = res['https://auth-ac.my.com/auth']['ssdc']
        mc_token = res['https://auth-ac.my.com/auth']['mc']
        sdc_token = auth_request.history[4].headers['set-cookie'].split(';')[0].split('=')[-1]
        self.cookies_values.update({'ssdc': ssdc_token, 'mc': mc_token, 'sdc': sdc_token})

    def get_cookies(self):
        return '; '.join([f'{k}={v}' for k, v in self.cookies_values.items()])

    @allure.step("Getting csrftoken cookie.")
    def get_csrf_token(self):
        csrf_request = self.session.get(url='https://target-sandbox.my.com/csrf/')
        csrftoken = csrf_request.headers['set-cookie'].split(';')[0].split('=')[-1]
        self.cookies_values['csrftoken'] = csrftoken

    def auth(self):
        self.get_tokens()  # first
        self.get_csrf_token()
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
        headers['Cookie'] = self.get_cookies()
        auth = self.session.post(url='https://auth-ac.my.com/auth', headers=headers, data=data)
        return auth

    @allure.step("Getting id of pocker game source.")
    def get_pocker_game_source_id(self):
        # link = 'https://vk.com/logic_poker'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        id_of_poker_game = self.session.get(
            url='https://target-sandbox.my.com/api/v1/vk_apps.json?q=https%3A%2F%2Fvk.com%2Flogic_poker',
            headers=headers
        )
        self.id_of_poker_game = id_of_poker_game.json()[0]['id']
        return id_of_poker_game.json()

    @allure.step("Getting id of VK Study group source.")
    def get_vk_study_group_source_id(self):
        # link = 'https://vk.com/vkedu'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        id_of_vk_study_group = self.session.get(
            url='https://target-sandbox.my.com/api/v2/vk_groups.json?_q=https%3A%2F%2Fvk.com%2Fvkedu',
            headers=headers
        )
        self.id_of_vk_study_group = id_of_vk_study_group.json()['items'][0]['id']
        return id_of_vk_study_group.json()

    @allure.step("Deleting poker game from sources list.")
    def delete_poker_source(self):
        headers = {'Cookie': self.get_cookies(),
                   'X-CSRFToken': self.cookies_values['csrftoken']}

        poker_deleted = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/vk_apps/{self.id_of_added_source_poker}.json',
            headers=headers)
        return poker_deleted

    @allure.step("Deleting VK Study group from sources list.")
    def delete_vk_group(self):
        headers = {'Cookie': self.get_cookies(),
                   'X-CSRFToken': self.cookies_values['csrftoken']}
        deleted_vk_group = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/vk_groups/{self.id_of_added_source_vk_group}.json',
            headers=headers)
        return deleted_vk_group

    @allure.step("Adding poker game to sources list.")
    def add_new_apps_and_games_source(self):
        data = '{"object_id": ' + f'{self.id_of_poker_game}' + '}'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        added_source = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/vk_apps.json',
            headers=headers,
            data=data
        )
        self.id_of_added_source_poker = added_source.json()['id']
        return added_source.json()

    @allure.step("Adding VK Study group to sources list.")
    def add_new_vk_group_source(self):
        data = '{"items":[{"object_id":' + f'{self.id_of_vk_study_group}' + '}]}'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        added_source = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/vk_groups/bulk.json',
            headers=headers,
            data=data
        )
        self.id_of_added_source_vk_group = added_source.json()['items'][0]['id']
        return added_source.json()

    @allure.step("Adding new audience segment based on poker game source.")
    def add_new_segment_poker(self):
        data = '{"name":"Poker segment",\
        "pass_condition":1,\
        "relations":[{"object_type":"remarketing_vk_app","params":{"source_id":7475511,"type":"positive"}}],\
        "logicType":"or"}'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        added_segment = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/segments.json',
            headers=headers,
            data=data
        )
        self.id_of_added_segment_poker = added_segment.json()['id']
        return added_segment

    @allure.step("Deleting audience segment based on poker game source.")
    def delete_segment_poker(self):
        headers = {'Cookie': self.get_cookies(),
                   'X-CSRFToken': self.cookies_values['csrftoken']}
        deleted_segment_poker = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/segments/{self.id_of_added_segment_poker}.json',
            headers=headers)
        return deleted_segment_poker

    @allure.step("Adding new audience segment based on VK Study group source.")
    def add_new_segment_vk_study(self):
        data = '{"name":"VK Study Audience",\
                 "pass_condition":1,\
                 "relations":[{"object_type":"remarketing_vk_group",\
                               "params":{"source_id":153502007,"type":"positive"}}],\
                 "logicType":"or"}'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        added_segment = self.session.post(
            url='https://target-sandbox.my.com/api/v2/remarketing/segments.json',
            headers=headers,
            data=data
        )
        self.id_of_added_segment_vk_study = added_segment.json()['id']
        return added_segment

    @allure.step("Deleting audience segment based on VK Study group source.")
    def delete_segment_vk_study(self):
        headers = {'Cookie': self.get_cookies(),
                   'X-CSRFToken': self.cookies_values['csrftoken']}
        deleted_segment_poker = self.session.delete(
            url=f'https://target-sandbox.my.com/api/v2/remarketing/segments/{self.id_of_added_segment_vk_study}.json',
            headers=headers)
        return deleted_segment_poker

    @allure.step("Creating new campaign.")
    def create_new_campaign(self):
        data = '{\
        "name":"SRVVR API TEST CAMPAIGN",\
        "read_only":false,\
        "conversion_funnel_id":null,\
        "objective":"general_ttm",\
        "targetings":{"split_audience":[1,2,3,4,5,6,7,8,9,10],\
        "sex":["male","female"],\
        "age":{"age_list":[0,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75],"expand":true},\
        "geo":{"regions":[188]},\
        "interests_soc_dem":[],\
        "birthday":null,\
        "segments":[],\
        "interests":[],\
        "fulltime":{"flags":["use_holidays_moving","cross_timezone"],\
                    "mon":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],\
                    "tue":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],\
                    "wed":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],\
                    "thu":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],\
                    "fri":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],\
                    "sat":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],\
                    "sun":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]},\
        "pads":[13697,38276]},\
        "age_restrictions":null,\
        "date_start":"2022-11-15",\
        "date_end":"2022-11-30",\
        "autobidding_mode":"max_shows",\
        "uniq_shows_period":"day",\
        "uniq_shows_limit":null,\
        "banner_uniq_shows_limit":null,\
        "budget_limit_day":"1000",\
        "budget_limit":"100000",\
        "mixing":"recommended",\
        "utm":null,\
        "enable_utm":true,\
        "price":"40",\
        "max_price":"0",\
        "package_id":438,\
        "banners":[{"urls":{"primary":{"id":696667}},\
                    "textblocks":{"title_25":{"text":"SRVVR"},\
                                  "text_90":{"text":"FOLLOW"},\
                                  "cta_sites_full":{"text":"visitSite"}},\
                                  "content":{"image_1080x607":{"id":' + f'{self.id_of_pic_big}' + \
                                  '},"icon_256x256":{"id":'+f'{self.id_of_pic_small}'+'}},"name":""}]}'
        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken'],
        }
        added_campaign = self.session.post(
            url='https://target-sandbox.my.com/api/v2/campaigns.json',
            headers=headers,
            data=data
        )
        self.id_of_created_campaign = added_campaign.json()['id']
        return added_campaign

    @allure.step("Deleting campaign.")
    def delete_campaign(self):
        data = '[{"id":' + f'{self.id_of_created_campaign}' + ',"status":"deleted"}]'
        headers = {'Cookie': self.get_cookies(),
                   'X-CSRFToken': self.cookies_values['csrftoken']}
        deleted_campaign = self.session.post(
            url='https://target-sandbox.my.com/api/v2/campaigns/mass_action.json',
            headers=headers,
            data=data
        )
        return deleted_campaign

    @allure.step("Uploading 1080x607 image.")
    def big_pic_upload(self):
        with open(f"{self.FILE_PATH_BIG}", "rb") as image:
            f = image.read()
            binary_file = bytearray(f)
        file = {'file': ('srvvr_cover.png', binary_file)}

        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken']
        }
        uploaded_big_pic = self.session.post(
            url='https://target-sandbox.my.com/api/v2/content/static.json',
            headers=headers,
            files=file
        )
        self.id_of_pic_big = uploaded_big_pic.json()['id']
        return uploaded_big_pic.json()

    @allure.step("Uploading 256x256 image.")
    def small_pic_upload(self):
        with open(f"{self.FILE_PATH_SMALL}", "rb") as image:
            f = image.read()
            binary_file = bytearray(f)
        file = {'file': ('srvvr_logo_cut.jpeg', binary_file)}

        headers = {
            'Cookie': self.get_cookies(),
            'X-CSRFToken': self.cookies_values['csrftoken']
        }
        uploaded_small_pic = self.session.post(
            url='https://target-sandbox.my.com/api/v2/content/static.json',
            headers=headers,
            files=file
        )
        self.id_of_pic_small = uploaded_small_pic.json()['id']
        return uploaded_small_pic.json()
