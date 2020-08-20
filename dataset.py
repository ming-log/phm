# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/18 15:25

from database import select_code, select_relation

def get_tree_data(code):
    tree_data = select_code(code)
    node_data = []
    pro_data = []
    for i in tree_data:
        node_temp = (i[0], i[1])
        pro_temp = (i[1], i[3])
        node_data.append(node_temp)
        pro_data.append(pro_temp)
    return node_data, pro_data

def get_ID(alpha):
    result = select_relation(alpha)
    data = []
    for i in result:
        data.append(i[0])
    return data

















