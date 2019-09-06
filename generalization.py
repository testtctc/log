#coding=utf-8

# 算法出处
# ## 根因分析初探：一种报警聚类算法在业务系统
# https://tech.meituan.com/2019/02/28/root-clause-analysis.html

# 未来方向  基于分布式计算抽取日志信息
import copy

def abstract_info(alarms:list,mini_size =10 )->list:

    """
    :param alarms:所有告警
    :return:   抽取出来的告警信息
    mini_size: 群的最小尺寸
    """

    #进行一次浅拷贝-->列表仅仅拷贝了元素地址
    T = copy.copy(alarms)
    #最后产生的信息  [(alam,count)]
    messages=[]
    #报警计数器
    counter = {}

    while True:
        # 元素计数器
        element_counter = [dict() for i in range(len(T[0]))]
        #当集合中的元素的个数不足mini_size时，直接退出
        if len(T) < mini_size :
            break

        stand_out =set()
        for item in T:
            #为每个元素计数
            for i in range(len(item)):
                k = item[i]
                c = element_counter[i].setdefault(k,0)
                element_counter[i][k]  = c + 1

            #返回一个原始值
            c1 = counter.setdefault(item,0)
            counter[item] = c1 + 1
            if counter[item] >= mini_size:
                stand_out.add(item)

        #满足条件可以聚类时
        if stand_out:
            for i in stand_out:
                messages.append((i,counter[i]))
            #更新T-->过滤
            T = [i for i in T if i not in stand_out]
        #选择一个属性，更新父类,更新列表T
        discreet = [max(d.values()) for d in element_counter]

        #获取需要更新的属性
        choosen_attr = discreet.index(min(discreet))

        #更新属性
        #继承计数
        counter={}

        #更新集合
        if T:
            T = [item.update(choosen_attr) for item  in T]
        else:
            break

    return messages
