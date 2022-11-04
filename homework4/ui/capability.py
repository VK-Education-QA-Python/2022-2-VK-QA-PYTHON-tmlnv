import os


def capability_select(device_os):
    if device_os == 'android':
        capability = {"platformName": "Android",
                      "platformVersion": "11.0",
                      "automationName": "Appium",
                      "appPackage": "ru.mail.search.electroscope",
                      "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
                      "app": os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                          '../app_file/marussia_1.70.0.apk')
                                             ),
                      'autoGrantPermissions': 'true',
                      "orientation": "PORTRAIT"
                      }
    else:
        raise ValueError("Incorrect device os type")
    return capability
