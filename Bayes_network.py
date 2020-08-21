# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/8/18 15:25

from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination
from dataset import get_tree_data, get_ID, get_detail_data


"""生成贝叶斯网络节点"""
def node_pro(pro, code, p_code):
    """
    :param pro: 先验的故障条件概率
    :param code: 当前节点的故障码/故障编号
    :param p_code: 当前节点的父节点的故障码/故障编号
    :return: 相应的贝叶斯网络节点cpd对象
    """
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
    """
    :param code: 根节点故障码/故障编号
    :return: 所有叶节点故障码/故障编号
    """
    _, pro_data = get_tree_data(code)
    all_node_name = []
    for i in pro_data[1:]:
        all_node_name.append(i[0])
    return all_node_name


"""构建贝叶斯网络模型"""
def set_bayes_model(code):
    """
    :param code: 根节点故障码/故障编号
    :return: 利用历史信息构建好的贝叶斯网络模型
    """
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
    """
    :param model: 贝叶斯网络模型
    :param code: 根节点的故障码/故障编号
    :param update_element: 进行故障检测的检测手段编号
    :return:
    """
    kt_infer = VariableElimination(model)
    all_node_name = get_all_node_name(code)
    sec_problem = set(all_node_name)
    The_updated_element = list(sec_problem.difference(set(update_element.keys())))
    update_prob = {}
    for i in The_updated_element:
        temp = kt_infer.query(
            variables=[i],
            evidence=update_element,
            show_progress = False
        ).values[1]
        update_prob[i] = temp
    sort_re = dict(sorted(update_prob.items(), key=lambda x: x[1], reverse=True))
    for i, j in sort_re.items():
        sum_j = sum(sort_re.values())
        print(i + ':' + str(j/sum_j))
    return sort_re

"""将输入的字符串转化为字典"""
def str_to_dic(str):
    """
    :param str: 字符串
    :return: 字典
    """
    dic = {}
    if ',' in str:
        for i in str.split(','):
            dic[i] = 0
    else:
        dic[str] = 0
    return dic

def get_pro(alpha, _list):
    """
    :param alpha: 检测手段的编号
    :param _list: 故障零部件对应的故障码/编号构成的列表
    :return:
    """
    data = {}
    for i in _list:
        pro = get_detail_data(alpha, i)
        data[i] = pro
    return data

"""获取需要更新的数据"""
def get_update_data(alpha, update_data):
    """
    :param alpha: 检测手段编号
    :param update_data: 故障零部件对应的故障码/编号
    :return:
    """
    if ',' in update_data:
        set_update_data = set(update_data.split(','))
    else:
        set_update_data = {}
    print("-" * 20)
    data = get_ID(alpha)
    set_data = set(data)
    already_check = set_data.intersection(set_update_data)
    rest_data = set_data.difference(set_update_data)
    print(alpha + '需要检测的零部件:' + str(list(set_data)))
    print("其中已经检测过的零部件:" + str(list(already_check)))
    print("还需要检测的零部件:" + str(list(rest_data)))
    print("还需要检测的零部件的概率分布:")
    if rest_data:
        set_data_pro = get_pro(alpha, list(rest_data))
        for i, j in set_data_pro.items():
            print(i + ':' + j)
    input("输入回车继续：")
    rest_data = list(rest_data)
    if len(rest_data) >= 1:
        a = rest_data[0]
        for i in rest_data[1:]:
            a = a + ',' + i
    else:
        a = ''
    return a

def main(code = "P20FE85"):
    model = set_bayes_model(code)
    print('当前网络节点概率值:')
    update_bayes_network(model, code)
    update_data = ''
    while True:
        try:
            alpha = input("请输入要进行检测的检测手段序号:")
            if alpha == '0':
                print("*"*10)
                print(" 退出成功！")
                print("*"*10)
                break
            update = get_update_data(alpha, update_data)
            print("*" * 20)
            print("   输入0退出系统！")
            print("*" * 20)
            print("-"*20)
            print('更新后:')
            if update_data and update:
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