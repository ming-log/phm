# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/26 9:05
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination

from dataset import get_tree_data


# 贝叶斯网络类
class BayesNetwork:
    def __init__(self, code):
        """
        :param code: 根节点故障码
        """
        self.code = code

    # 生成贝叶斯网络节点
    def node_pro(self, pro, p_code):
        """
        :param pro: 先验的故障条件概率
        :param code: 当前节点的故障码/故障编号
        :param p_code: 当前节点的父节点的故障码/故障编号
        :return: 相应的贝叶斯网络叶节点cpd对象
        """
        cpd = TabularCPD(
                    variable=p_code,
                    variable_card=2,
                    values=[[1, 1 - pro],
                            [0, pro]],
                    evidence=[self.code],
                    evidence_card=[2]
                    )
        return cpd

    # 得到所有节点名称
    def get_all_node_name(self):
        """
        :param code: 根节点故障码/故障编号
        :return: 所有叶节点故障码/故障编号
        """
        _, pro_data = get_tree_data(self.code)
        all_node_name = []
        for i in pro_data[1:]:
            all_node_name.append(i[0])
        return all_node_name

    # 构建贝叶斯网络模型
    def make_bayes_model(self):
        """
        :param code: 根节点故障码/故障编号
        :return: 利用历史信息构建好的贝叶斯网络模型
        """
        node_data, pro_data = get_tree_data(self.code)
        model = BayesianModel(node_data[1:])
        for i in pro_data[1:]:
            cpd = self.node_pro(float(i[1].split('%')[0])/100, i[0])
            model.add_cpds(cpd)   # 将各子节点加入贝叶斯网络
        # 根节点
        root_cpd = TabularCPD(
                            variable=self.code,
                            variable_card=2,
                            values=[[1 - float(pro_data[0][1].split('%')[0])/100,
                                     float(pro_data[0][1].split('%')[0])/100]]
                            )
        model.add_cpds(root_cpd)  # 将根节点加入贝叶斯网络
        return model

    # 更新贝叶斯网络
    def update_bayes_network(self, model, update_element={}):
        """
        :param model: 贝叶斯网络模型
        :param code: 根节点的故障码/故障编号
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
