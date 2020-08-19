# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/7/14 9:40

from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
from dataset import get_tree_data


"""生成贝叶斯网络节点"""
def node_pro(pro, code, p_code):
    cpd = TabularCPD(
                variable=code,
                variable_card=2,
                values=[[1, 1 - pro],
                        [0, pro]],
        evidence=[p_code],
        evidence_card=[2]
    )
    return cpd

"""得到所有节点名称"""
def get_all_node_name(code):
    _, pro_data = get_tree_data(code)
    all_node_name = []
    for i in pro_data[1:]:
        all_node_name.append(i[0])
    return all_node_name


"""构建贝叶斯网络模型"""
def set_bayes_model(code):
    node_data, pro_data = get_tree_data(code)
    model = BayesianModel(node_data[1:])
    for i in pro_data[1:]:
        cpd = node_pro(float(i[1].split('%')[0])/100, i[0], code)
        model.add_cpds(cpd)
    root_cpd = TabularCPD(
                variable=code,
                variable_card=2,
                values=[[1 - float(pro_data[0][1].split('%')[0])/100, float(pro_data[0][1].split('%')[0])/100]]
    )

    model.add_cpds(root_cpd)
    return model

"""更新贝叶斯网络"""
def update_bayes_network(model, code, update_element = {}):
    kt_infer = VariableElimination(model)
    all_node_name = get_all_node_name(code)
    sec_problem = set(all_node_name)
    The_updated_element = list(sec_problem.difference(set(update_element.keys())))
    update_prob = {}
    for i in The_updated_element:
        temp = kt_infer.query(
            variables=[i],
            evidence=update_element
        ).values[1]
        update_prob[i] = temp
    sort_re = dict(sorted(update_prob.items(), key=lambda x: x[1], reverse=True))
    for i, j in sort_re.items():
        sum_j = sum(sort_re.values())
        print(i + ':' + str(j/sum_j))
    return sort_re

def str_to_dic(str):
    dic = {}
    if ',' in str:
        for i in str.split(','):
            a, b = i.split('=')
            dic[a.strip()] = int(b.strip())
    else:
        a, b = str.split('=')
        dic[a.strip()] = int(b.strip())
    return dic

def main():
    code = "P20FE85"
    model = set_bayes_model(code)
    print('当前网络节点概率值:')
    update_bayes_network(model, code)
    update_data = ''
    while True:
        try:
            update = input("请输入要更新的节点，以逗号为分割符号：")
            if update == '0':
                break
            print("输入0退出系统！")
            print("-"*20)
            print('更新后:')
            if update_data:
                update_data = update_data + ',' + update
            else:
                update_data = update_data + update
            update_data1 = str_to_dic(update_data)
            result = update_bayes_network(model, code, update_data1)
            if not result:
                print("所有故障均以排除，如果还没有解决问题则说明故障不在数据库中，请进一步深入检查！")
                print("请输入0退出系统！")
        except:
            print("输入错误！")

"""
对应规则
"""

if __name__ == '__main__':
    main()
