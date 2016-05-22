#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# main.py
# 编写人：路泽亚
# 本文件主要是界面部分

import Tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from record import DBHandle

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class LoginWindow:

    def __init__(self, db):
        self.db = db
        self.login = Tk.Tk()
        self.listbox = Tk.Listbox(self.login)
        self.login_button = Tk.Button(self.login,
                                      text="进入",
                                      command=self.loginCallback)
        self.create_button = Tk.Button(self.login, text="创建")

        self.login.wm_title("选择")

        for i in db.listUser():
            self.listbox.insert(0, i)
        self.listbox.grid(row=0, column=0, rowspan=2, columnspan=1)
        self.login_button.grid(row=0, column=1)
        self.create_button.grid(row=1, column=1)
        return None

    def loginCallback(self):
        print self.listbox.get(self.listbox.curselection())
        return None

    def run(self):
        return self.login.mainloop()


db = DBHandle("weight.db")
login = LoginWindow(db)
login.run()
