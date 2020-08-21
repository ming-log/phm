# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/18 15:25
import pymysql

"""判断数据库是否连接成功"""
def judgment_connect():
    try:
        conn = pymysql.connect(
        host='192.168.10.155',
        port=3306,
        password='123456',
        user="crawl",
        database='phm',
        charset='utf8'
        )
        return conn
    except:
        print("数据库连接失败")
        return 0

"""查询所有的节点"""
def select_code(code):
    conn = judgment_connect()
    cursor = conn.cursor()
    sql = 'select * from fault_tree where ID = "%s"' % code
    cursor.execute(sql)
    c = cursor.fetchall()
    conn.commit()
    return c

def select_relation(alpha):
    conn = judgment_connect()
    cursor = conn.cursor()
    sql = 'select ID from fault_information where %s is not null' % alpha
    cursor.execute(sql)
    c = cursor.fetchall()
    conn.commit()
    return c

def select_detail_data(alpha, ID):
    conn = judgment_connect()
    cursor = conn.cursor()
    sql = 'select %s from fault_information where ID = "%s"' % (alpha, ID)
    cursor.execute(sql)
    c = cursor.fetchall()
    conn.commit()
    return c


select_detail_data('alpha1', 'R1')
alpha = 'alpha1'
ID = 'R1'
