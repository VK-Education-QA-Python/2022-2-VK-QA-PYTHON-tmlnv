from appium.webdriver.common.mobileby import MobileBy


class BasePageANDROIDLocators:
    pass


class MainPageANDROIDLocators(BasePageANDROIDLocators):
    KEYBOARD_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    SETTINGS_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')


class SearchPageANDROIDLocators(BasePageANDROIDLocators):
    SEARCH_FIELD = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    SEND_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/text_input_send')
    RUSSIA_INFO = (MobileBy.ID,
                   'ru.mail.search.electroscope:id/item_dialog_fact_card_content_text')
    RUSSIAN_POPULATION = (MobileBy.XPATH, '//android.view.ViewGroup[4]/android.widget.TextView')
    POPULATION_SEARCH_RESULT = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    CALCULATION_RESULT = (
        MobileBy.XPATH,
        '//androidx.recyclerview.widget.RecyclerView/android.widget.TextView[2]'
    )
    TURNING_ON_NEWS_LOCATOR = (
        MobileBy.XPATH,
        '//android.widget.LinearLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.widget.TextView')


class SettingsPageANDROIDLocators(BasePageANDROIDLocators):
    NEWS_SOURCE = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    MAIL_RU_SOURCE = (
        MobileBy.XPATH,
        '//android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]')
    SELECTED_SOURCE = (MobileBy.ID, 'ru.mail.search.electroscope:id/news_sources_item_selected')
    GO_BACK_BUTTON = (MobileBy.CLASS_NAME, 'android.widget.ImageButton')
    CLOSE_MENU_CROSS = (
        MobileBy.XPATH,
        '//android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.ImageButton')
    ABOUT = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_about')
    APP_VERSION = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_version')
    COPYRIGHT = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_copyright')
