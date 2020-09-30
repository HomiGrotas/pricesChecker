from flask import Flask
from socket import gethostbyname, gethostname
from priceScraper import shops, update_all
from time import time
from threading import Thread

# create Flask app
app = Flask(__name__)
ip_address = gethostbyname(gethostname())
last_sync = time()
update_shops = Thread(target=update_all)

KEYS = [shop.get_shop_name() for shop in shops]
VALUES = [shop.get_products() for shop in shops]


@app.route("/get_prices")
def get_prices():
    """
    :return: all the shop's products
    """
    global KEYS, VALUES

    if not update_shops.is_alive():
        KEYS = [shop.get_shop_name() for shop in shops]
        VALUES = [shop.get_products() for shop in shops]

    return dict(zip(KEYS, VALUES))


@app.route("/update")
def update():
    """
    updates the product prices
    :return:
    """

    global last_sync

    # allows update every 30 seconds
    if time() - last_sync > 30:
        update_shops.start()
        last_sync = time()
        return "updated"
    return str(round(30 - (time() - last_sync)))


if __name__ == "__main__":
    print("host:", ip_address)
    app.run(host=ip_address)
