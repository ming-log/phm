# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/8/24 15:10
import pandas as pd


class RelationSheet:
    def __init__(self):
        self.data1 = pd.read_excel("./F-R.xlsx", sheet_name=0, index_col="序号")          # 将序号这列作为行标签
        self.data2 = pd.read_excel("./F-R.xlsx", sheet_name=1)
        self.data3 = pd.read_excel("./F-R.xlsx", sheet_name=2, skiprows=1)                # 省略第一行数据
        self.data4 = pd.read_excel("./F-R.xlsx", sheet_name=4)

    def get_first_part(self, part):
        temp = self.data2 == part
        for i, j in temp.items():
            if any(j):
                return i

    def select(self, code):
        select_data = self.data3[self.data3["故障码"] == code]
        correspond = self.data4["对应关系"][self.data4["故障码"] == code].values[0]  # 对应关系
        for i, j in select_data.items():
            if i == "故障码":
                print(i, ":", j.values[0])
                print("对应关系:", correspond)
            elif i == "故障描述":
                print(i, ":", j.values[0])
                print("故障模式:")
            elif not pd.isnull(j.values):
                print("\t", "-" * 50)
                first_part = self.get_first_part(i)
                print("\t", "故障一级部件:", first_part)
                print("\t", i, ":")
                if '\n' in j.values[0]:
                    for k in j.values[0].split("\n"):
                        print("\t", k)
                else:
                    print("\t", j.values[0])


if __name__ == '__main__':
    relation_sheet = RelationSheet()
    while True:
        print("\t", "-" * 50)
        fault_code = input("故障码:")
        if fault_code == '0':
            print()
            print("\t\t\t**************")
            print("\t\t\t*退 出 系 统 !*")
            print("\t\t\t**************")
            break
        try:
            relation_sheet.select(fault_code)
        except Exception as e:
            print("\t\t\tError:", e)
