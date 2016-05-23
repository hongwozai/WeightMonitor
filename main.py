#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# main.py
# 编写人：路泽亚
# 本文件主要是界面部分

import Tkinter as Tk
import tkMessageBox
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
        self.create_button = Tk.Button(self.login,
                                       text="创建",
                                       command=self.createCallback)

        self.login.wm_title("选择")

        for i in db.listUser():
            self.listbox.insert(Tk.END, i)

        self.listbox.selection_set(0)
        self.listbox.grid(row=0, column=0, rowspan=2, columnspan=1)
        self.login_button.grid(row=0, column=1)
        self.create_button.grid(row=1, column=1)
        return None

    def loginCallback(self):
        try:
            print self.listbox.get(self.listbox.curselection())
        except Tk.TclError:
            tkMessageBox.showinfo("", "没有选中")
            pass
        return None

    def createCallback(self):
        cu = CreateUserWindow(self.db, self.listbox)
        cu.run()
        return None

    def run(self):
        return self.login.mainloop()


class CreateUserWindow:

    def __init__(self, db, listbox):
        self.db = db
        self.listbox = listbox
        self.root = Tk.Tk()
        self.label_name = Tk.Label(self.root, text="名称: ")
        self.entry = Tk.Entry(self.root)
        self.cancel_button = Tk.Button(self.root,
                                       text="取消",
                                       command=self.cancelCallback)
        self.create_button = Tk.Button(self.root,
                                       text="创建",
                                       command=self.createCallback)

        self.root.wm_title("创建")
        self.label_name.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.cancel_button.grid(row=1, column=0)
        self.create_button.grid(row=1, column=1)
        return None

    def createCallback(self):
        try:
            username = self.entry.get()
            db.createUser(username)
            self.root.destroy()
            self.listbox.insert(Tk.END, username)
        except Exception:
            pass
        return None

    def cancelCallback(self):
        return self.root.destroy()

    def run(self):
        return self.root.mainloop()


class TodayWindow:

    def __init__(self, db):
        return None


db = DBHandle("weight.db")
if not db.isExistDB:
    db.createUser("lzy")
login = LoginWindow(db)
login.run()
