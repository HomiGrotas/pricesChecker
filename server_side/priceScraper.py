from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from json import dumps, load
from glob import glob
import hiperMorHandler
import RamiLaviHandler


def create_driver():
    """
    :return: chrome webdriver
    """
    return webdriver.Chrome("chromedriver.exe")


shops = []
driver = create_driver()


#   ToDo: read json files - ✓
#   ToDo: create classes with the json data - ✓
#   ToDo: run selenium with xpath - ✓
#   ToDo: make check with check_pattern - ✓
#   ToDo: get additional data (company, amount) - ✓
#   ToDo: add product (price, name, company) to Shop list - ✓
#   ToDo: api - dict (keys: shops, values: products) - ✓


def close_driver():
    """
    :does: closes driver
    """
    driver.quit()


class Shop:
    """
    class of RamiLavi shop.
    use to get the chili price of the shop
    """

    def __init__(self, url: str, xpath_patterns: dict, shop_name: str,
                 handler: str, look_for: str = "צילי מתוק"):

        self._url = url
        self._xpath = xpath_patterns
        self._shop_name = shop_name
        self._look_for = look_for
        self._handler = eval(handler)
        self._products = []
        self.update()  # updates products list

    def update(self):
        """
        updates the chili price
        :return: None
        """
        self._products = []
        if driver.current_url != self._url:
            driver.get(self._url)  # enter the page

        self._load_xpath()

    def _check_name(self, ind: int):
        """
        :param ind: index of the element
        :return: is the name in the index fits to the requirements
        :rtype: tuple (bool, str)
        """

        try:
            xpath = self._handler.get_xpath_pattern(
                self._xpath['name'], 'name', ind
            )

            name = WebDriverWait(driver, 7).\
                until(ec.presence_of_element_located(
                 (By.XPATH, xpath)
                 ), "Couldn't load name of product in " + self._shop_name)

        except TimeoutException:
            raise

        return check_pattern(name.text, self._look_for), name.text

    def _get_price(self, ind: int):
        """
        :param ind: index of product (1-)
        :return: gets product price
        :rtype: str
        """
        xpath = self._handler.get_xpath_pattern(
            self._xpath['price'], 'price', ind
        )

        price = WebDriverWait(driver, 7).\
            until(ec.presence_of_element_located(
                  (By.XPATH, xpath)))

        return price.text

    def _get_company(self, ind: int):
        """
        :param ind: index of product (1-)
        :return: if there is a company name and its name
        :rtype: tuple
        """
        xpath = self._handler.get_xpath_pattern(
            self._xpath['company'], 'company', ind
        )

        company = WebDriverWait(driver, 7). \
            until(ec.presence_of_element_located(
             (By.XPATH, xpath)))

        company = company.text
        has_company = True

        if any(char.isdigit() for char in company):
            has_company = False

        return has_company, company

    def _get_amount(self, ind: int):
        """
        :param ind: index of product (1-)
        :return: the size of the product (grams, mml, etc.)
        :rtype: str
        """
        xpath = self._handler.get_xpath_pattern(
            self._xpath['amount'], 'amount', ind
        )

        amount = WebDriverWait(driver, 7). \
            until(ec.presence_of_element_located(
             (By.XPATH, xpath)))

        return amount.text.replace("|", "", 1)

    def _load_xpath(self):
        """
        looping through all the products and searching for
        the look_for variable pattern
        :return: None
        """
        if self.get_shop_name() == "hiperMor":
            hiperMorHandler.close_proms(driver)

        product_amount = self._handler.get_amount_of_products(driver)

        for i in range(1, product_amount + 1):
            fits, name = self._check_name(i)
            if fits:
                price = self._get_price(i)
                has_company, company = self._get_company(i)

                if has_company:
                    amount = self._get_amount(i)
                else:
                    amount = company
                    company = "Unknown"

                self._products.append(
                    Product(self._shop_name, price, company, amount, name)
                )

    def get_data(self):
        """
        :return: RamiLavi chili price
        """
        return self.product

    def get_shop_name(self):
        return self._shop_name

    def get_products(self):
        return [product.get_info_dict() for product in self._products]

    def __str__(self):
        return "Shop name: " + self._shop_name + \
               "\nUrl: " + self._url + \
               "\nXpath patterns: " + dumps(self._xpath) + \
               "\nLook for: " + self._look_for

    def __repr__(self):
        return {
                    "Shop name": self._shop_name,
                    "Url": self._url,
                    "Xpath patterns": self._xpath,
                    "Look for": self._look_for
                }


class Product:
    """
    product of a shop
    """

    def __init__(self, shop_name: str, price: str, company: str,
                 amount: str, name: str):

        self._shop_name = shop_name.strip()
        self._price = price.strip()
        self._company = company.strip()
        self._amount = amount.strip()
        self._name = name.strip()

    def get_info_dict(self):
        """
        :return:description of the product
        :rtype: dict
        """
        return {
                    "name": self._name,
                    "shop_name": self._shop_name,
                    "price": self._price,
                    "company": self._company,
                    "amount": self._amount
                }


def create_classes():
    """
    creates Shop classes with the json data
    :return: None
    """
    data = read_json_files()
    for shop_data in data:
        key = list(shop_data.keys())[0]
        xpath_keys = ["name", "price", "company", "amount"]

        url = shop_data[key]["url"]
        xpath_patterns = \
            dict(zip(xpath_keys,
                     [shop_data[key][xpath_key] for xpath_key in xpath_keys]))

        look_for = shop_data[key]["look_for"]
        handler = shop_data[key]["handler"]

        shops.append(Shop(url, xpath_patterns, key, handler, look_for))


def read_json_files():
    """
    reads json files
    :return: the data in the json files (list)
    """

    json_files = glob("*.json")
    to_rtr = []

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = load(file)
            to_rtr.append({json_file.replace('.json', ''): data})

    return to_rtr


def check_pattern(word: str, pattern: str):
    word = ''.join([char for char in word
                    if 'א' <= char <= 'ת' or char == " "])
    return pattern in word


def update_all():
    for shop in shops:
        for p in shop._products:
            print(p.get_info_dict())
        shop.update()

    print("---finished updating---")


create_classes()
