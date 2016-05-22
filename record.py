#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# record.py
# 编写人：路泽亚
# 本文件主要与数据库sqlite3进行交互
# 两个表user,user_weight(对应与具体用户名)
# user (name, waist腰围, height身高)
# user_weight (date, time, weight)

import os
import sqlite3
from datetime import datetime, timedelta

# user表记录用户名
sql_user = """
CREATE TABLE user (
name text,
waist real,
height real,
PRIMARY KEY (name)
);
"""

# 表名为对应的用户名加上table
# 表名的形式无法使用sqlite3自带的?,只能操作字符串
sql_weight = """
CREATE TABLE {} (
date text,
time text,
weight real,
PRIMARY KEY (date, time)
);
"""

# 创建表索引
sql_weight_index = """
CREATE INDEX {0}_idx ON {0}(date);
"""

# 创建用户项
sql_createUser = """
INSERT INTO user VALUES(?, ?, ?);
"""

# 列出用户
sql_listUser = """
SELECT name FROM user;
"""

# 插入日期，时间，体重
# 日期与时间分开是为了分析时方便
sql_insertUserWeight = """
INSERT INTO {} VALUES(?, ?, ?);
"""

# 查找用户的体重信息，一天之内
sql_listUserWeightToday = """
SELECT time, weight FROM {} WHERE date = ?;
"""

# 查找用户的体重信息，每天的
sql_listUserWeightEveryday = """
SELECT date, avg(weight) FROM {} GROUP BY date;
"""

# 查询指定天的平均体重
sql_queryUserWeight = """
SELECT date, avg(weight) FROM {} WHERE date = ? GROUP BY date;
"""


class DBHandle:

    def __init__(self, dbname):
        "dbname为数据库文件路径"
        self.dbname = dbname
        self.isExistDB = False

        if os.path.exists(dbname):
            self.isExistDB = True

        self.conn = sqlite3.connect(self.dbname)

        if self.isExistDB is False:
            self.createDB()
        return None

    def __del__(self):
        self.conn.close()
        return None

    def createDB(self):
        "创建数据库并创建user表"
        sc = self.conn.cursor()
        sc.execute(sql_user)
        self.conn.commit()
        return None

    def createUser(self, name, waist=0, height=0):
        "创建用户，同时会创建用户的体重记录表"
        sc = self.conn.cursor()
        sc.execute(sql_createUser, (name, waist, height))
        sc.execute(sql_weight.format(name))
        sc.execute(sql_weight_index.format(name))
        self.conn.commit()
        return None

    def listUser(self):
        "列出所有用户, 返回用户名的列表（用户不会太多，所以直接查找全部）"
        sc = self.conn.cursor()
        sc.execute(sql_listUser)
        self.conn.commit()
        return [i[0] for i in sc.fetchall()]

    def insertUserWeight(self, name, weight):
        "插入用户体重，时间实时生成.weight数字， name字符串"
        # 生成时间
        now = datetime.now()
        date = str(now.strftime("%x"))
        time = str(now.strftime("%X"))

        sc = self.conn.cursor()
        sc.execute(sql_insertUserWeight.format(name), (date, time, weight))
        self.conn.commit()
        return None

    def listUserWeightToday(self,
                            name,
                            date=str(datetime.now().strftime("%x"))):
        """
        返回元组的列表(默认当天)，没有查找到返回空表。
        元组第一项为当天时间，第二项为体重
        因为一天中也不可能次数太多，所以fetchall，这里性能受限于查找的速度
        """
        sc = self.conn.cursor()
        sc.execute(sql_listUserWeightToday.format(name), (date,))
        self.conn.commit()
        return sc.fetchall()

    def listUserWeightEveryday(self, name):
        """
        返回生成器，每一项为一个元组
        元组第一项为日期，第二项为当日平均体重
        这个数据可能会很多，所以需要优化
        """
        sc = self.conn.cursor()
        sc.execute(sql_listUserWeightEveryday.format(name))
        while True:
            res = sc.fetchone()
            if res is None:
                break
            yield res
        return

    def listUserWeightWeek(self,
                           name,
                           date=str(datetime.now().strftime("%x"))):
        """
        列出指定用户本周的所有数据。返回值同listUserWeightToday类似。
        可能不足7天，也可能没有数据（空表）
        """
        # 找到本周开始的一天
        date = datetime.strptime(date, "%x")
        week_today = date.isoweekday()
        start = date - timedelta(week_today)

        # 没法用sql直接做，只能查询七次每次加一天
        one = timedelta(1)
        sc = self.conn.cursor()
        week_weight = []
        for i in range(7):
            start += one
            print str(start.strftime("%x"))
            sc.execute(sql_queryUserWeight.format(name),
                       (str(start.strftime("%x")), ))
            self.conn.commit()
            data = sc.fetchone()
            if data is not None:
                week_weight.append(data)
                print data

        return week_weight

    def insertTestData(self, name, date, time, weight):
        "测试数据的使用"
        sc = self.conn.cursor()
        sc.execute(sql_insertUserWeight.format(name), (date, time, weight))
        self.conn.commit()
        return None


def record_main():
    db = DBHandle("weight.db")
    # db.createUser("lzy")
    db.insertUserWeight("lzy", 49)
    import time;time.sleep(1)
    db.insertUserWeight("lzy", 47)

    for i in db.listUserWeightEveryday("lzy"):
        print i

        print db.listUserWeightWeek("lzy")
        del db
    return None

# 测试使用
if __name__ == "__main__":
    record_main()
