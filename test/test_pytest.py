#coding=utf-8



"""
pytest 简单案例
简单高效

参考 https://blog.csdn.net/liuchunming033/article/details/46501653
"""

def add(x):
    return x + 1


def test_add2():
    assert add(1) == 2


def test_add():

    assert add(1) == 5


class TestClass:
    #使用类进行测试
    #方法以test开头
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')

