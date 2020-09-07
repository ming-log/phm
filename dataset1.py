# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/7 13:19
# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/8/18 15:25
import json

import pandas as pd


json_file = "data.json"     # 需要导入的json文件


def read_json(json_file):
    # f = open("data.json", encoding='utf-8')
    f = open(json_file, encoding='utf-8')
    data = json.load(f)
    tree_data = data['FtaTree']
    tree_data_root = tree_data['Root']
    root_code = tree_data_root['Code']
    root_pro = tree_data_root['IRate']

    tree_data_leaf = tree_data['Leaf']
    tree_data_leaf = pd.DataFrame(tree_data_leaf)
    tree = list(zip(tree_data_leaf['PCode'], tree_data_leaf['Code']))
    pro = list(zip(tree_data_leaf['Code'], tree_data_leaf['CRate']))

    method_data = data['Method']
    method_data = pd.DataFrame(method_data)
    return root_code, root_pro, tree, pro, method_data



root_code, root_pro, tree, pro, method_data = read_json(json_file)


# 获取检测手段对应的节点相关数据
def get_id(alpha, method_data):
    all_data = pd.DataFrame(method_data['RelatedLeaf'][method_data['MethodCode'] == alpha].iloc[0])
    return all_data


get_ID = get_id
