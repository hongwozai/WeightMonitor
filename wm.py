#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# wm.py
# 编写人： 路泽亚
# 本文件主要为启动界面,命令行参数
# 体脂率，腰围

import time
import matplotlib.pyplot as plt
import numpy as np
from record import DBHandle
from datetime import datetime


# 时间比较函数
def CompareTime(t, other):
    "两个时间都是字符串形式"
    t = datetime.strptime(t, "%H:%M:%S")
    o = datetime.strptime(other, "%H:%M:%S")
    if t < o:
        return -1
    elif t == o:
        return 0
    else:
        return 1


# 日期比较函数
def CompareDate(d, other):
    "两个日期都是字符串形式"
    d = datetime.strptime(d, "%Y-%m-%d")
    o = datetime.strptime(other, "%Y-%m-%d")
    if d > o:
        return -1
    elif d == o:
        return 0
    else:
        return 1


# WegithMonitor
class WM:

    def __init__(self, name, db):
        "name是用户名称，db是已经打开的数据库"
        self.name = name
        self.db = db
        return None

    def monitorEveryday(self):
        # 获得计算数据
        l = self.db.listUserWeightEveryday(self.name)
        d = []
        w = []
        for i in sorted(l, cmp=CompareDate, key=lambda x: x[0]):
            d.append(i[0])
            w.append(i[1])
        d.reverse()
        w.reverse()
        day = d
        if d == []:
            return False

        # 基准
        total = len(d)
        start = time.mktime(time.strptime(d[0], "%Y-%m-%d"))
        end = time.mktime(time.strptime(d[total - 1], "%Y-%m-%d"))
        sw = int(w[0]) - 20
        ew = int(w[0]) + 20

        d = [time.mktime(time.strptime(i, "%Y-%m-%d")) - start for i in d]
        # 画图
        plt.figure(figsize=(12, 6))
        plt.plot(d, w, "*-")

        # 设置坐标刻度
        day = [i[5:] for i in day]
        ax = plt.gca()
        ax.set_xticks(np.linspace(0,
                                  end - start,
                                  total))
        ax.set_xticklabels(day)
        # ax.set_xticklabels([str(i) for i in range(int(start_time), 25)])
        ax.set_yticks(np.linspace(sw, ew, 11))

        # 配置信息
        plt.grid()
        plt.xlabel("time")
        plt.ylabel("weight")
        plt.show()
        return True

    def monitorToday(self):
        l = self.db.listUserWeightToday(self.name)
        if l == []:
            return False
        l.sort(cmp=CompareTime, key=lambda x: x[0])

        # 获得基准（体重是今日第一次量的上下加10，时间是从6点到24点）
        start_time = "06"
        start = time.mktime(time.strptime("{}:00:00".format(start_time),
                                          "%H:%M:%S"))
        end = time.mktime(time.strptime("23:59:59", "%H:%M:%S"))
        sw = int(l[0][1]) - 10
        ew = int(l[0][1]) + 10

        # 计算x,y数据
        t = [time.mktime(time.strptime(i[0], "%H:%M:%S")) - start for i in l]
        w = [i[1] for i in l]

        # 画图
        plt.figure(figsize=(12, 6))
        plt.plot(t, w, "*-")

        # 设置坐标刻度
        ax = plt.gca()
        ax.set_xticks(np.linspace(int(start_time),
                                  end - start,
                                  25 - int(start_time)))
        ax.set_xticklabels([str(i) for i in range(int(start_time), 25)])
        ax.set_yticks(np.linspace(sw, ew, 11))

        # 配置信息
        plt.grid()
        plt.xlabel("time")
        plt.ylabel("weight")
        plt.show()
        return True


# 测试使用
def wm_main():
    db = DBHandle("weight.db")
    if not db.isExistDB:
        db.createUser("lzy")
        # 生成今日的数据
        db.insertTestData("lzy", "2016-05-26", "12:06:05", 84.1)
        db.insertTestData("lzy", "2016-05-27", "12:06:05", 84.1)
        db.insertTestData("lzy", "2016-05-22", "07:06:05", 85.5)
        db.insertTestData("lzy", "2016-05-22", "08:06:05", 84.3)
        db.insertTestData("lzy", "2016-05-22", "09:06:05", 83.2)
        db.insertTestData("lzy", "2016-05-22", "10:06:05", 82.67)
        db.insertTestData("lzy", "2016-05-23", "11:06:05", 86.8)
        db.insertTestData("lzy", "2016-05-24", "12:06:05", 84.1)
        db.insertTestData("lzy", "2016-05-25", "12:06:05", 88.1)
        db.insertTestData("lzy", "2016-05-28", "12:06:05", 82.1)

    wm = WM("lzy", db)
    # wm.monitorToday()
    wm.monitorEveryday()
    return None

if __name__ == "__main__":
    wm_main()
