import server_connection
from tkinter import *
from itertools import chain
from tkinter import ttk, messagebox
from threading import Thread
from datetime import datetime

WIDTH = 1000
HEIGHT = 200
FONT = ("DAVID", 32)


# ToDo: tkinter table - ✓
# ToDo: update button - ✓


def analyze_data(shops: dict):
    return list(chain(*shops.values()))


def open_main_win():
    root = Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.title("Chili prices checker")

    shops = server_connection.get_prices()
    products = analyze_data(shops)
    MainWindow(root, products)
    root.mainloop()


class MainWindow(Frame):
    def __init__(self, master: object, data: list):
        self.get_time = lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        super().__init__(master, width=WIDTH, height=HEIGHT)
        self.data = data
        self.last_sync = StringVar()
        self.last_sync.set("Last update: " + self.get_time())

        if data:
            topics = tuple(data[0].keys())
        else:
            topics = ["None" for _ in range(4)]

        self.tv = ttk.Treeview(self, columns=tuple(range(len(topics))),
                               show="headings", height=50)
        self.topics = topics
        self._create_top()
        self.tv.pack()
        self._create_table()

        self.pack()

    def _create_top(self):
        top = Frame(self, width=WIDTH, height=20)

        self.last_sync_lbl = Label(top, textvariable=self.last_sync)

        self.last_sync_lbl.pack(side='left')

        Label(top, width=int(WIDTH/9.7), text="Welcome - HomiGrotas App")\
            .pack(side='left')

        Button(top, width=WIDTH//80, text="Update",
               command=self.ask_for_update).pack(side='right')

        top.pack(side='top')

    def ask_for_update(self):
        if server_connection.can_update():
            self.data = analyze_data(server_connection.get_prices())
            self._create_table()
            self.last_sync.set("Last update: " + self.get_time())
            messagebox.showinfo("Success", "The table is updated")

    def _create_table(self):
        topics_len = len(self.topics)

        for to_delete in self.tv.get_children():
            self.tv.delete(to_delete)

        for i in range(topics_len):
            self.tv.heading(i, text=self.topics[i])

        for product in self.data:
            self.tv.insert('', 'end', values=tuple(product.values()))
