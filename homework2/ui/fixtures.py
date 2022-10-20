import os
import shutil
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.basic_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.audiences_page import AudiencesPage

NAME = 'tmlnv@vk.com'
PASSWORD = 'qwerty1234'


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    headless = config['headless']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if selenoid:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "105.0",
            "selenoid:options": {
                "enableVNC": False,
                "enableVideo": False
            }
        }
        if vnc:
            capabilities["selenoid:options"]["enableVNC"] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("window-size=1920,1080")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager(version='105.0.5195.19').install(),
                                  options=options)
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


def get_driver(browser_name, headless, selenoid, vnc):
    options = Options()
    if selenoid:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "105.0",
            "selenoid:options": {
                "enableVNC": False,
                "enableVideo": False
            }
        }
        if vnc:
            capabilities["selenoid:options"]["enableVNC"] = True
        browser = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser_name == 'chrome':
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("window-size=1920,1080")
        browser = webdriver.Chrome(executable_path=ChromeDriverManager(version='105.0.5195.19').install(),
                                   options=options)
    elif browser_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser_name}"')
    browser.maximize_window()
    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):
    url = config['url']
    browser = get_driver(request.param, headless=request.config.getoption("--headless"),
                         selenoid=request.config.getoption("--selenoid"),
                         vnc=request.config.getoption("--vnc")
                         )
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture(scope='module', autouse=True)
def cookies(request, email=NAME, password=PASSWORD):
    driver_cookies = get_driver("chrome", request.config.getoption("--headless"),
                                selenoid=request.config.getoption("--selenoid"),
                                vnc=request.config.getoption("--vnc")
                                )
    driver_cookies.get("https://target-sandbox.my.com/")
    page_4_cookies = LoginPage(driver_cookies)
    page_4_cookies.click_login(locator=LoginPageLocators.LOGIN_BUTTON)
    page_4_cookies.login(email, password, locator1=LoginPageLocators.EMAIL, locator2=LoginPageLocators.PASSWORD,
                         locator3=LoginPageLocators.LOGIN_FORM_BUTTON)
    cookies = driver_cookies.get_cookies()

    return cookies


@pytest.fixture()
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture()
def campaigns_page(driver):
    return CampaignsPage(driver=driver)


@pytest.fixture()
def audiences_page(driver):
    return AudiencesPage(driver=driver)
