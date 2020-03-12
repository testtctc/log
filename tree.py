#coding=utf-8

import numpy as np
import pandas as pd
import logging
from queue import Queue

class AttributeTree():

    """
    属性树
    """

    def __init__(self,name,elements,relations,root=None):
        """
        elements :list 所有节点的集合
        relations :dict  节点之间的关系
        one_array:numpy.array 辅助
        """
        self.name = name
        self.elements  = elements
        self.one_array = np.array(elements)
        self.relations = relations
        self.dataframe = self._create_dataframe()
        self.root = root
        self.priority= None
        self.sort()

    def sort(self):
        """使用队列进行排序--宽度优先"""
        sort ={}
        sort[self.root] = 1
        id = 0
        queue = Queue()
        queue.put(self.root)
        while not queue.empty():
            element = queue.get()
            id = id + 1
            sort[element] = id
            if element in self.relations:
                for c in self.relations[element]:
                    queue.put(c)

        print(sort)
        self.priority=sort

    def max_key(self,keys):
        """寻找最大键"""
        keys= list(keys)
        max= keys[0]
        max_priority=self.priority[max]
        for key in keys:
            if self.priority[key] > max_priority:
                max=key
                max_priority = self.priority[key]
        return max

    def _create_dataframe(self):
        """构建矩阵 dataframe"""
        arr = np.zeros((len(self.elements), len(self.elements)))
        for p in self.relations:
            for c in self.relations[p]:
                arr[self.elements.index(p), self.elements.index(c)] = 1
        return pd.DataFrame(arr, index=self.elements, columns=self.elements)

    def search_children(self,p:str,c:str,dis=1)->int:
        #直系距离
        #寻找并返回距离
        #优点 简单
        #缺点 内存消耗较大
        """
        p：父节点
        c:子节点
        dis:距离
        """
        if p ==c:
            return 0
        if p not in self.relations:
            return -1
        elif c in self.relations[p]:
            return dis
        else:
            return max(self.search_children(child,c,dis+1) for child in self.relations[p])

    def search_children3(self,p:str, c:str, dis=1)->int:
        # 直系距离
        # 寻找并返回距离
        #优点数据量大时，利用矩阵进行搜索效率高
        """
        p：父节点
        c:子节点
        dis:距离
        """
        #两者相等时，直接返回
        if  p ==c:
            return 0
        if self.dataframe.loc[p,c] == 1:
            return dis
        # bool index
        childrens = self.dataframe.loc[p] == 1

        if np.sum(childrens) == 0:
            return -1
        elif np.sum(self.dataframe[childrens][c]) > 0:
            return dis + 1
        else:
            #
            bottom =  self.dataframe[childrens].sum(axis=0) > 0
            #没有孙节点
            if np.sum(bottom) ==0:
                return -1
            else :
                #可能多个节点都指向同一个c,此时路径取最小值
                out = [self.search_children3(p1, c,dis + 2) for p1 in one_array[bottom]]
                filter = [ x for x  in out if x > 0]
                #均找不到
                if len(filter) ==0:
                    return -1
                else :
                    return min(filter)

    def distance(self,e1: str, e2: str, use_dict =True, level=1) -> int:
        """
        :param e1:元素
        :param e2: 元素
        :param use_dict: 使用基于字典的方式计算节点之间的距离
        :return: 两个元素之间的距离
        """

        # 确保搜索的元素存在
        assert e1 in self.elements
        assert e2 in self.elements

        dis_func =  self.search_children if use_dict else self.search_children3
        dis = max(dis_func(e1, e2),dis_func(e2,e1))
        if dis != -1:
            return dis
        else:
            level = 0
            # 获取父节点
            parents = self.find_parents(e1)
            while True:
                level += 1
                # 距离得分
                dis_score = []
                # 祖先
                ancestor = []
                for p in parents:
                    ancestor.extend(self.find_parents(p))
                    dis = dis_func(p, e2)
                    if dis != -1:
                        dis_score.append(dis)

                if  len(dis_score) > 0 and  max(dis_score) >= 0:
                    return level + min([x for x in dis_score if x >= 0])
                elif ancestor:
                    parents = set(ancestor)  # 去重

    def find_parents(self,node:str) ->list :
        return list(self.one_array[self.dataframe[node] ==1])

    def to_parent(self,node:str)->str:
        #找到父类并返回其中之一
        parents = self.find_parents(node)
        if parents:
            return parents[0]
        else:
            logging.warning("已经是根节点，无法找到父类: " + node)
            return node


if __name__ == "__main__":
    from relations.just_test import elements, one_array, relations

    att_tree =AttributeTree("test",elements,relations,"a")
    print(att_tree.dataframe)
    assert att_tree.distance("a","e") ==2 #work

    assert att_tree.distance("c", "e",use_dict=False)==3
    assert att_tree.distance("c", "d",use_dict=False)==3
    assert att_tree.distance("d", "e",use_dict=False) ==2

    assert att_tree.distance("c", "e")==3
    assert att_tree.distance("c", "d")==3
    assert att_tree.distance("d", "e") ==2
    assert att_tree.distance("f", "e") == 3
    assert att_tree.distance("k", "e") == 4
    assert att_tree.distance("k", "c") == 5


