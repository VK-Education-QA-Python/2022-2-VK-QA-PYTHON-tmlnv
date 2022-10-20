from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_BUTTON = (By.CSS_SELECTOR, '.responseHead-module-button-2yl51i')
    EMAIL = (By.NAME, 'email')
    PASSWORD = (By.NAME, 'password')
    LOGIN_FORM_BUTTON = (By.CLASS_NAME, 'authForm-module-button-1u2DYF')


class BasePageLocators:
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
    CREATE_CAMPAIGN_BUTTON = (By.CSS_SELECTOR, "[data-test='button']:first-child")


class CampaignPageLocators:
    VK_PRODUCTS_BUTTON = (By.CSS_SELECTOR, "._general_ttm")
    LINK_INPUT = (By.CSS_SELECTOR, "[placeholder='Enter the link']")
    WIDESCREEN_BLOCK_CAMPAIGN_BUTTON = (By.CSS_SELECTOR, ".pac-id-438")
    CAMPAIGN_NAME_FIRST_INPUT = (By.CSS_SELECTOR, ".base-settings__campaign-name-wrap input[maxlength='255']")
    CAMPAIGN_DATE_FROM_INPUT = (By.CSS_SELECTOR, ".js-max-price-block .date-setting__date-from input")
    CAMPAIGN_DATE_TO_INPUT = (By.CSS_SELECTOR, ".js-max-price-block .date-setting__date-to input")
    BUDGET_PER_DAY_INPUT = (By.CSS_SELECTOR, "[data-test='budget-per_day']")
    BUDGET_TOTAL_INPUT = (By.CSS_SELECTOR, "[data-test='budget-total']")
    ADD_TITLE_INPUT = (By.CSS_SELECTOR, "[data-name='title_25']")
    ADD_TEXT_INPUT = (By.CSS_SELECTOR, "[data-name='text_90']")
    UPLOAD_BIG_IMAGE_INPUT = (
        By.CSS_SELECTOR,
        "[class*='bannerForm-module-fieldsWrapForInline'] [class*='bannerForm-module-roleInline']:first-child input"
    )
    UPLOAD_SMALL_IMAGE_INPUT = (
        By.CSS_SELECTOR,
        "[class*='bannerForm-module-fieldsWrapForInline'] [class*='bannerForm-module-roleInline']:last-child input"
    )
    CREATE_CAMPAIGN_FOOTER_BUTTON = (By.CSS_SELECTOR, ".footer__button [data-class-name='Submit']")
    CAMPAIGN_TITLE_IN_TABLE = (
        By.CSS_SELECTOR,
        "[class*='main-module-CellFirst'] [data-entity-type='campaign'] a[title='SRVVR CAMPAIGN']"
    )
    CHECKBOX_ALL_ROWS = (By.CSS_SELECTOR, "[class*='header-module-noWrap'] [type='checkbox']")
    ACTIONS_DROP_DOWN = (By.CSS_SELECTOR, "[class*='tableControls-module-selectItem']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "li[title='Delete']")


class AudiencesPageLocators:
    APPS_AND_GAMES_IN_SOCIAL_NETWORKS = (By.CSS_SELECTOR, "[href='/segments/apps_games_list']")
    LINK_OR_NAME_INPUT = (By.CSS_SELECTOR, "input[class*='multiSelectSuggester']")
    SELECT_ALL_BUTTON = (By.CSS_SELECTOR, "[data-test='select_all']")
    ADD_SELECTED_BUTTON = (By.CSS_SELECTOR, "[data-test='add_selected_items_button']")
    SEGMENTS_LIST = (By.CSS_SELECTOR, "[href='/segments/segments_list']")
    CREATE_NEW_SEGMENT_BUTTON = (By.CSS_SELECTOR, "[href='/segments/segments_list/new/']")
    APP_CHECKBOX = (By.CSS_SELECTOR, ".js-sources .adding-segments-source:last-child .adding-segments-source__checkbox")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".adding-segments-modal__footer .button_submit")
    SEGMENT_NAME_INPUT = (By.CSS_SELECTOR, ".input_create-segment-form .input__inp")
    CREATE_SEGMENT_BUTTON = (By.CSS_SELECTOR, ".create-segment-form__btn-wrap  button")
    SEGMENT_IN_SEGMENTS_LIST = (By.CSS_SELECTOR, "[title='POKER VK GAME']")
    ID_CHECKBOX_ALL_ELEMENTS = (By.CSS_SELECTOR, "[class*='header-module-noWrap'] input[type='checkbox']")
    ACTIONS_DROP_DOWN = (By.CSS_SELECTOR, "[class*='segmentsTable-module-selectItem']")
    REMOVE = (By.CSS_SELECTOR, "[data-id='remove']")
    CROSS_REMOVE = (By.CSS_SELECTOR, "[data-class-name='RemoveView']")
    BUTTON_CONFIRM_REMOVE = (By.CSS_SELECTOR, ".button_confirm-remove")
    GROUPS_OK_AND_VK = (By.CSS_SELECTOR, "[href='/segments/groups_list']")
    ADDING_SEGMENTS_GROUPS_OK_AND_VK = (By.CSS_SELECTOR, ".adding-segments-item:nth-child(10)")
    SEGMENT_VK_GROUP_IN_SEGMENTS_LIST = (By.CSS_SELECTOR, "[title='VK STUDY GROUP']")
    SEARCH_BY_NAME = (By.CSS_SELECTOR, '[placeholder = "Search by name or id..."]')
    CREATE_SEGMENT_BUTTON_IF_SEGMENT_EXISTS = (By.CSS_SELECTOR, ".button_submit")
    ADDING_SEGMENTS_GAMES = (By.CSS_SELECTOR, ".adding-segments-item:nth-child(8)")
    LI_SUGGESTER_MODULE_TO_DELETE = (By.CSS_SELECTOR, "li[class*='suggester-module-option']")
    POKER_ROW_LOCATOR = (By.CSS_SELECTOR, "[href='https://vk.com/logic_poker']")
