#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# main.py
# 编写人：路泽亚
# 本文件主要是界面部分

import os
import re
import Tkinter as Tk
from tkMessageBox import showwarning

from record import DBHandle
from wm import WM


class LoginWindow:

    def __init__(self, db):
        self.db = db
        self.root = Tk.Tk()
        self.listbox = Tk.Listbox(self.root)
        self.login_button = Tk.Button(self.root,
                                      text="进入",
                                      command=self.loginCallback)
        self.create_button = Tk.Button(self.root,
                                       text="创建",
                                       command=self.createCallback)

        self.root.wm_title("选择")

        for i in db.listUser():
            self.listbox.insert(Tk.END, i)

        self.listbox.selection_set(0)
        self.listbox.grid(row=0, column=0, rowspan=2, columnspan=1)
        self.login_button.grid(row=0, column=1)
        self.create_button.grid(row=1, column=1)
        return

    def loginCallback(self):
        "进入主界面"
        try:
            username = self.listbox.get(self.listbox.curselection())
        except Tk.TclError:
            showwarning("", "没有选中")

        wm = WM(username, self.db)
        self.root.destroy()
        main = MainWindow(self.db, wm, username)
        main.run()
        return

    def createCallback(self):
        cu = CreateUserWindow(self.db, self.listbox)
        cu.run()
        return

    def run(self):
        return self.root.mainloop()


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
        return

    def createCallback(self):
        "直接在listbox中添加项，就代表刷新了。TODO:改变刷新方式"
        try:
            username = self.entry.get()
            if username == "":
                showwarning("", "请输入!")
                return
            db.createUser(username)
            self.root.destroy()
            self.listbox.insert(Tk.END, username)
        except Exception:
            showwarning("", "用户重名!")
            pass
        return

    def cancelCallback(self):
        return self.root.destroy()

    def run(self):
        return self.root.mainloop()


class MainWindow:

    def __init__(self, db, wm, name):
        self.db = db
        self.wm = wm
        self.name = name
        self.root = Tk.Tk()
        self.today = Tk.Button(self.root,
                               text="今日图像",
                               command=self.todayCallback)
        self.everyday = Tk.Button(self.root,
                                  text="全部",
                                  command=self.everydayCallback)
        self.record = Tk.Button(self.root,
                                text="记录",
                                command=self.recordCallback)
        self.today.grid(row=0, column=0)
        self.everyday.grid(row=0, column=1)
        self.record.grid(row=0, column=2)
        self.root.wm_title(self.name)
        return

    def todayCallback(self):
        if self.wm.monitorToday() is False:
            showwarning("", "今日没有体重数据!")
        return

    def everydayCallback(self):
        if self.wm.monitorEveryday() is False:
            showwarning("", "没有任何体重数据")
        return

    def recordCallback(self):
        record = RecordWindow(self.db, self.name)
        return record.run()

    def run(self):
        return self.root.mainloop()


class RecordWindow:

    def __init__(self, db, name):
        self.name = name
        self.db = db
        self.root = Tk.Tk()
        self.label = Tk.Label(self.root, text="本次体重: ")
        self.entry = Tk.Entry(self.root)
        self.record_button = Tk.Button(self.root,
                                       text="记录",
                                       command=self.recordCallback)
        self.cancel_button = Tk.Button(self.root,
                                       text="取消",
                                       command=self.cancelCallback)
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.cancel_button.grid(row=1, column=0)
        self.record_button.grid(row=1, column=1)
        self.root.wm_title(self.name)
        return

    def recordCallback(self):
        weight = self.entry.get()
        if weight == "":
            showwarning("", "请输入！")
            return
        m = re.match("^[0-9][0-9.]*$", weight)
        if m is not None:
            self.db.insertUserWeight(self.name, weight)
            return self.root.destroy()
        showwarning("", "请重新输入！")
        return

    def cancelCallback(self):
        return self.root.destroy()

    def run(self):
        return self.root.mainloop()


# 程序运行流程与所需变量
database = "~/.record/record.db"

if __name__ == '__main__':
    database = os.path.expanduser(os.path.dirname(database))
    dbdir = os.path.dirname(database)
    if not os.path.exists(dbdir):
        os.mkdir(dbdir)
    db = DBHandle(database)
    login = LoginWindow(db)
    login.run()
