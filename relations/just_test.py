#coding=utf-8


#小案例，用于测试
#枚举所有元素


import numpy  as np

elements = ["a","b","c","d","e","f","k"]
one_array = np.array(elements)
#定义父子关系
relations ={"a":["b","c"],"b":["d","e"],"d":["f"],"f":["k"]}