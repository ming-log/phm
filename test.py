# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/18 15:26
import json
import pandas as pd


f = open("data.json", encoding='utf-8')
data = json.load(f)
tree_data = data['FtaTree']
tree_data_root = tree_data['Root']
tree_data_leaf = tree_data['Leaf']
tree_data_leaf = pd.DataFrame(tree_data_leaf)
tree = list(zip(tree_data_leaf['PCode'], tree_data_leaf['Code']))
pro = list(zip(tree_data_leaf['Code'], tree_data_leaf['CRate']))

method_data = data['Method']
method_data = pd.DataFrame(method_data)
