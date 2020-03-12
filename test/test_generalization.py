#coding=utf-8

from alarm import Alarm
from tree import AttributeTree
from generalization import abstract_info

#归属关系
elements_1 = ["自然界","动物","植物","爬行类","哺乳类","鳄鱼","蜗牛","猪","狗","土狗","拉布拉多"]

relations_1={"自然界":["动物","植物"],"动物":["爬行类","哺乳类"],"爬行类":["鳄鱼","蜗牛"],"哺乳类":["猪","狗"],"狗":["土狗","拉布拉多"]}


#行为关系
elements_2 = ["行为","觅食","攻击","乞讨","捕猎","抓","咬","撕","吞","群挑","单挑"]

relations_2={"行为":["觅食","攻击"],"觅食":["乞讨","捕猎"],"攻击":["抓","咬"],"咬":["撕","吞"],"捕猎":["群挑","单挑"]}


class Animal(Alarm):
    Trees = [AttributeTree("归属",elements_1,relations_1,"自然界"),AttributeTree("行为",elements_2,relations_2,"行为")]



class TestAbstraction():
    #测试信息抽取
    def test_abstract_info(self):
        alarm_set = [Animal("爬行类","撕"),Animal("爬行类","撕"),Animal("爬行类","撕"),Animal("爬行类","撕"),Animal("爬行类","撕")]
        print(abstract_info(alarm_set,mini_size=3))  #nimal("爬行类","撕")

    def test_abstract_info2(self):

        alarm_set = [Animal("爬行类","咬"),Animal("爬行类","撕"),Animal("爬行类","撕"),Animal("爬行类","撕"),Animal("爬行类","撕")]
        print(abstract_info(alarm_set,mini_size=4))  #.[(Animal(爬行类,撕), 4)]
        print(abstract_info(alarm_set, mini_size=5))   #[(Animal(爬行类,咬), 5)]