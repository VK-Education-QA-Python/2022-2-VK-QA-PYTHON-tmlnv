import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption('--headless', action='store_true', help="Run driver in headless mode (no browser page visible).")


@pytest.fixture()
def config(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    url = "https://target-sandbox.my.com/"
    return {"browser": browser, "url": url, "headless": headless}


@pytest.fixture(scope='function')
def driver(config):

    browser = config["browser"]
    url = config["url"]
    headless = config['headless']
    match browser:
        case 'chrome':
            options = Options()
            if headless:
                options.add_argument('--headless')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("window-size=1920,1080")
            driver = webdriver.Chrome(executable_path=ChromeDriverManager(version='105.0.5195.19').install(),
                                      options=options)
        case _:
            raise RuntimeError(f'Unsupported browser, we do this homework only for Chrome: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()
