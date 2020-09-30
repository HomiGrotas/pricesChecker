from requests import get, ConnectionError
from socket import gethostname, gethostbyname
from json import loads, dumps
from time import sleep
from tkinter import messagebox

ip_address = gethostbyname(gethostname())


def get_prices():
    """
    :return: new information of the products
    :rtype: dict
    """
    try:
        file = get(f"http://{ip_address}:5000/get_prices")
    except ConnectionError as e:
        messagebox.showerror(title=type(e).__name__, message=e)
        return {}
    return file.json()


def can_update():
    """
    :return: update is available
    :rtype: bool
    """
    ans = False
    try:
        response = get(f"http://{ip_address}:5000/update").text
        if response != "updated":  # if can't update
            response = response if response != '0' else '1'

            if messagebox.askretrycancel(  # if user wants to try again
                    title="Can't update",
                    message=f"You can update every 30 seconds\n"
                            f"time left: {response} seconds."):
                ans = can_update()
        else:
            ans = True  # you can update

    except ConnectionError as e:
        messagebox.showerror(title=type(e).__name__, message=e)
    return ans
