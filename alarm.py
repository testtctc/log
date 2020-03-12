#coding=utf-8

from tree import AttributeTree
from relations.just_test import elements,relations


"""
说明：所有的子类都必须继承父类Alarm，并填写属性树的列表 Trees

其中：Alarm_Test 仅仅用于示范，并无其他作用

"""

class Alarm():
    """
    告警
    """
    #类属性，公用，节约内存
    Trees = []  #属性树的集合,用于计算距离

    def __init__(self,*attr):
        #最好是写死,避免属性不一致
        self._attrs =attr

        if not self.Trees:
            raise NotImplemented("必须先实现告警属性树")


    def dissimilarity(self,other)->int:
        # 两个告警之间的非相似度-->距离

        if not isinstance(other,self.__class__):
            raise ValueError("必须是相同告警类型")

        if len(self) != len(other):
            raise ValueError("属性长度必须一致，否则无法比较")

        combo = zip(self._attrs,other._attrs,self.Trees)
        dis = []
        for (a1,a2,tree) in combo:
            dis.append(tree.distance(a1,a2))
        return sum(dis)

    def update(self,attr_index:int):
        #更新部分元素之后，返回新对象
        parent = self.Trees[attr_index].to_parent(self._attrs[attr_index])
        attrs = [self._attrs[i] if i !=attr_index else parent for i in range(len(self))]

        return self.__class__(*attrs)


    def __eq__(self, other):
        """对比两个元素是否相等"""
        #根据距离也可以直接得出，但计算成本高
        if not isinstance(other,self.__class__):
            raise  ValueError("必须是相同告警类型")
        combo = zip(self._attrs, other._attrs)
        for (a1,a2) in combo:
            if a1 != a2:
                return False
        return True

    def __len__(self):
        #告警的长度
        return len(self._attrs)

    def __iter__(self):
        return self._attrs

    def __getitem__(self, index):
        return self._attrs[index]

    def __repr__(self):
        attrs_str = ",".join([str(i) for i in self._attrs])
        return self.__class__.__name__ + "("  + attrs_str + ")"

    def askey(self):
        return "-".join( i for i in self._attrs)

    def __hash__(self):
        return hash( "".join( i for i in self._attrs))

class Alarm_Test(Alarm):
    """示范"""
    Trees =[AttributeTree("测试属性",elements,relations)]
