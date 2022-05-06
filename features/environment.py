
"""
Environment for Behave Testing
"""
from os import getenv
from behave import *
from selenium import webdriver

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))
BASE_URL = getenv('BASE_URL', 'http://localhost:8080')


def before_all(context):
    """ Executed once before all tests """
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized") # open Browser in maximized mode
    options.add_argument("disable-infobars") # disabling infobars
    options.add_argument("--disable-extensions") # disabling extensions
    options.add_argument("--disable-gpu") # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
    options.add_argument("--no-sandbox") # Bypass OS security model
    options.add_argument("--headless")

    context.WAIT_SECONDS = WAIT_SECONDS
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(context.WAIT_SECONDS) # seconds
    context.base_url = BASE_URL

    # context.driver.set_window_size(1200, 600)

    context.base_url = BASE_URL
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini"
    context.config.setup_logging()


def after_all(context):
    """ Executed after all tests """
    context.driver.quit()

def step_impl(context, text_string):
    """ Get the value if a text field """
    element = context.driver.find_element_by_id(element_id)
    assert text_string in element.get_attribute('value')

def step_impl(context, text_string):
    """ Get the value if a text field """
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)

def step_impl(context, text_string):
    """ Type a string into a text field """
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)