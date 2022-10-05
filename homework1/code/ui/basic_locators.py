from selenium.webdriver.common.by import By

LOGIN_BUTTON = (By.CSS_SELECTOR, '.responseHead-module-button-2yl51i')
EMAIL = (By.NAME, 'email')
PASSWORD = (By.NAME, 'password')
LOGIN_FORM_BUTTON = (By.CLASS_NAME, 'authForm-module-button-1u2DYF')
STARTING_PAGE_DASH = (By.CSS_SELECTOR, "[href='/dashboard']")
LOGOUT_BUTTON_2 = (By.CSS_SELECTOR, "[href='/logout']")
LOGOUT_BUTTON = (By.CLASS_NAME, "right-module-rightButton-3e-duF")
FULL_NAME = (By.CSS_SELECTOR, 'input[type="text"]')
SAVE_BUTTON = (By.CLASS_NAME, "button__text")
PROFILE_BUTTON = (By.CSS_SELECTOR, "[data-gtm-id='pageview_profile']")
AUDIENCE_BUTTON = (By.CSS_SELECTOR, "[href='/segments']")
AUDIENCE_SEGMENTS = (By.CLASS_NAME, "left-nav__group__label")
BILLING_BUTTON = (By.CSS_SELECTOR, "[href='/billing']")
BILLING_PAYER = (By.CLASS_NAME, "deposit__payment-form__title")


