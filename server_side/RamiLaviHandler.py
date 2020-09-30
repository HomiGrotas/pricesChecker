from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_xpath_pattern(pattern, _, ind):
    return pattern.format(ind=ind)


def get_amount_of_products(driver, limit=10):
    length = len(WebDriverWait(driver, 7)
                 .until(ec.presence_of_all_elements_located(
                  (By.CLASS_NAME, "product-title")),
        "can't get amount of products - RamiLavi"))

    if length > limit:
        length = limit

    return length
