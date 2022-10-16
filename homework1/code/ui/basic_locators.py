from selenium.webdriver.common.by import By

LOGIN_BUTTON = (By.CSS_SELECTOR, "[class*='responseHead-module-button']")
EMAIL = (By.NAME, 'email')
PASSWORD = (By.NAME, 'password')
LOGIN_FORM_BUTTON = (By.CSS_SELECTOR, "[class*='authForm-module-button']")
STARTING_PAGE_DASH = (By.CSS_SELECTOR, "[href='/dashboard']")
LOGOUT_BUTTON_2 = (By.CSS_SELECTOR, "[href='/logout']")
LOGOUT_BUTTON = (By.CSS_SELECTOR, "[class*='right-module-rightButton']")
FULL_NAME = (By.CSS_SELECTOR, 'input[type="text"]')
SAVE_BUTTON = (By.CLASS_NAME, "button__text")
PROFILE_BUTTON = (By.CSS_SELECTOR, "[data-gtm-id='pageview_profile']")
AUDIENCE_BUTTON = (By.CSS_SELECTOR, "[href='/segments']")
AUDIENCE_SEGMENTS = (By.CLASS_NAME, "left-nav__group__label")
BILLING_BUTTON = (By.CSS_SELECTOR, "[href='/billing']")
BILLING_PAYER = (By.CLASS_NAME, "deposit__payment-form__title")
ERROR_INVALID_LOGIN_OR_PASSWORD = (By.CLASS_NAME, 'js_form_msg')
LOGOUT_MENU = (By.CSS_SELECTOR, "[class*='rightMenu-module-visibleRightMenu']")
CREATE_CAMPAIGN_BUTTON = (By.CSS_SELECTOR, "[data-test='button']:first-child")


