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

    #属性树
    Trees = T[0].Trees

    while True:
        # 报警计数器
        counter = {}
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
                c = element_counter[i].get(k,0)
                element_counter[i][k]  = c + 1

            #返回一个原始值
            c1 = counter.get(item,0)
            counter[item] = c1 + 1

        for m  in counter:
            if counter[m] >= mini_size:
                stand_out.add(m)

        #满足条件可以聚类时
        if stand_out:
            for i in stand_out:
                messages.append((i,counter[i]))
            #更新T-->过滤
            T = [i for i in T if i not in stand_out]

        if T:
            # 选择一个属性，更新父类,更新列表T
            # 找到最大优先级，然后更新值

            #collector:（key,count） ->str,int
            collector=[]
            choosen_attr=None
            #最下计数
            min=None
            for i in range(len(element_counter)):
                k = Trees[i].max_key(element_counter[i].keys())
                #i =  (Trees[i].one_array == k).argmax()
                collector.append((k,element_counter[i][k]))
                if (min is None)  or ( element_counter[i][k] < min) :
                    min = element_counter[i][k]
                    choosen_attr = i

            #获取需要更新的属性
            update_key = collector[choosen_attr][0]

            #更新集合
            T = [item.update(choosen_attr) if item[choosen_attr] ==update_key else item for item in T ]
        else:
            break

    return messages
