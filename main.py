# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/8/18 15:25
from Bayes_network import BayesNetwork
from dataset1 import get_ID, method_data


# 将输入的字符串转化为字典
def str_to_dic(_str):
    """
    :param _str: 字符串
    :return: 字典
    """
    _dic = {}
    if ',' in _str:
        for i in _str.split(','):
            _dic[i] = 0
    else:
        _dic[_str] = 0
    return _dic


# 获取需要更新的数据
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
    if isinstance(alpha, list):
        set_data = set()
        for a in alpha:
            temp_data = set(get_ID(a, method_data)['Code'])
            set_data = set_data.union(temp_data)
    else:
        data = get_ID(alpha, method_data)
        set_data = set(data['Code'])                            # 需要检测的所有零部件
    already_check = set_data.intersection(set_update_data)      # 已经检测过的零部件
    rest_data = set_data.difference(set_update_data)            # 还需要检测的零部件
    print(str(alpha) + '需要检测的零部件:' + str(list(set_data)))
    print("其中已经检测过的零部件:" + str(list(already_check)))
    print("需要检测的零部件:" + str(list(rest_data)))
    action = input("检测有故障请输入1，检测无故障请输入0:")
    # rest_data = list(rest_data)
    set_data_pro = {}
    if action == '1' or action == '0':
        for i in range(len(data)):
            set_data_pro[data['Code'].iloc[i]] = data['Rate'].iloc[i]
    else:
        print("输入错误!")
        # return
    return set_data_pro, action


def main(e_y=50, e_x=0.995):
    bayes_network = BayesNetwork()
    model = bayes_network.make_bayes_model()
    print('当前网络节点概率值:')
    result = bayes_network.update_bayes_network(model)
    sum_j = sum(result.values())
    for i, j in result.items():
        result[i] = j / sum_j
        print("%s : %.4f" % (i, j / sum_j))
    update_data = ''
    while True:
        try:
            alphas = input("请输入要进行检测的检测手段序号:")
            if ',' in alphas:
                alpha = alphas.split(',')
            else:
                alpha = alphas
            if alpha == '0':
                print("*"*10)
                print(" 退出成功！")
                print("*"*10)
                break
            update, action = get_update_data(alpha, update_data)
            for i in range(len(update.keys())):
                if i == 0:
                    temp = list(update.keys())[i]
                else:
                    temp = temp + ',' + list(update.keys())[i]
            if update_data and temp:
                update_data = update_data + ',' + temp
            else:
                update_data = update_data + temp

            print("更新后的节点概率:")
            if action == '1':
                for i, j in update.items():
                    update[i] = float(update[i])
                    result[i] = result[i] * (1 + e_y * update[i])
            else:
                for i, j in update.items():
                    update[i] = float(update[i])
                    result[i] = result[i] * (1 - e_x * update[i])

            sum_j = sum(result.values())
            for i, j in result.items():
                result[i] = j / sum_j
            result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

            for i, j in result.items():
                print("%s : %.4f" % (i, j))
            if not result:
                print("所有故障均以排除，如果还没有解决问题则说明故障不在数据库中，请进一步深入检查！")
                print("请输入0退出系统！")
        except Exception as e:
            print("输入错误！\n", e)


"""
对应规则
"""

if __name__ == '__main__':
    main()
