# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/26 9:05
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination

import dataset1


# 贝叶斯网络类
class BayesNetwork:
    def __init__(self):
        """
        :param code: 根节点故障码
        """
        self.root_code = dataset1.root_code
        self.root_pro = dataset1.root_pro
        self.tree = dataset1.tree
        self.pro = dataset1.pro
        self.method_data = dataset1.method_data

    # 生成贝叶斯网络节点
    def node_pro(self, pro, p_code):
        """
        :param pro: 先验的故障条件概率
        :param p_code: 当前节点的父节点的故障码/故障编号
        :return: 相应的贝叶斯网络叶节点cpd对象
        """
        cpd = TabularCPD(
                    variable=p_code,
                    variable_card=2,
                    values=[[1, 1 - pro],
                            [0, pro]],
                    evidence=[self.root_code],
                    evidence_card=[2]
                    )
        return cpd

    # 得到所有节点名称
    def get_all_node_name(self):
        """
        :return: 所有叶节点故障码/故障编号
        """
        all_node_name = []
        for i in self.pro:
            all_node_name.append(i[0])
        return all_node_name

    # 构建贝叶斯网络模型
    def make_bayes_model(self):
        """
        :return: 利用历史信息构建好的贝叶斯网络模型
        """
        model = BayesianModel(self.tree)
        for i in self.pro:
            cpd = self.node_pro(float(i[1]), i[0])
            model.add_cpds(cpd)   # 将各子节点加入贝叶斯网络
        # 根节点
        root_cpd = TabularCPD(
                            variable=self.root_code,
                            variable_card=2,
                            values=[[1 - float(self.root_pro),
                                     float(self.root_pro)]]
                            )
        model.add_cpds(root_cpd)  # 将根节点加入贝叶斯网络
        return model

    # 更新贝叶斯网络
    def update_bayes_network(self, model, update_element={}):
        """
        :param model: 贝叶斯网络模型
        :param update_element: 进行故障检测的检测手段编号
        :return:更新后的网络节点信息
        """
        kt_infer = VariableElimination(model)
        all_node_name = self.get_all_node_name()
        sec_problem = set(all_node_name)                    # 得到所有叶节点名称
        the_updated_element = list(sec_problem.difference(set(update_element.keys())))
        update_prob = {}
        for i in the_updated_element:
            temp = kt_infer.query(
                variables=[i],
                evidence=update_element,
                show_progress=False
            ).values[1]
            update_prob[i] = temp
        sort_re = dict(sorted(update_prob.items(), key=lambda x: x[1], reverse=True))
        return sort_re
