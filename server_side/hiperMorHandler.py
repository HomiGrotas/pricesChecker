from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep


def close_proms(driver):
    try:
        button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div"
                                              "[2]/form/div[3]/span/button")

        button.click()
    except Exception:
        pass

    try:
        button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/"
                                                  "div[2]/form/div[2]/div[2]/button")

        button.click()
    except Exception:
        pass

    sleep(1)

    try:
        button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/"
                                              "div[2]/button/img")
        button.click()
    except Exception:
        pass

    try:
        button = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]"
                                              "/span/img")
        button.click()

    except Exception:
        pass


def get_xpath_pattern(pattern, pattern_name, ind):
    assert ind < 11, "Limit is 10"

    def name_pattern():
        if ind < 6:
            rtr = 5 if ind % 2 == 0 else 6
        else:
            rtr = 6 if ind % 2 == 0 else 5
        return rtr

    def price_pattern():
        if ind < 6:
            rtr = 6 if ind % 2 == 0 else 7
        else:
            rtr = 7 if ind % 2 == 0 else 6
        return rtr

    def company_pattern():
        if ind < 6:
            rtr = 3 if ind % 2 == 0 else 4
        else:
            rtr = 4 if ind % 2 == 0 else 3
        return rtr

    def amount_pattern():
        if ind < 6:
            rtr = 3 if ind % 2 == 0 else 4
        else:
            rtr = 4 if ind % 2 == 0 else 3
        return rtr

    patterns = \
        {
            'name': name_pattern,
            'price': price_pattern,
            'company': company_pattern,
            'amount': amount_pattern,
        }

    f = patterns[pattern_name]()
    return pattern.format(ind=ind, ind2=f)


def get_amount_of_products(driver, limit=10):
    length = len(WebDriverWait(driver, 7)
                 .until(ec.presence_of_all_elements_located(
                    (By.CLASS_NAME, "name")),
        "can't get amount of products - HiperMor"))

    if length > limit:
        length = limit

    return length
