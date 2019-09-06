#coding=utf-8
from alarm import Alarm
from tree import AttributeTree


#归属关系
elements_1 = ["自然界","动物","植物","爬行类","哺乳类","鳄鱼","蜗牛","猪","狗","土狗","拉布拉多"]

relations_1={"自然界":["动物","植物"],"动物":["爬行类","哺乳类"],"爬行类":["鳄鱼","蜗牛"],"哺乳类":["猪","狗"],"狗":["土狗","拉布拉多"]}


#行为关系
elements_2 = ["行为","觅食","攻击","乞讨","捕猎","抓","咬","撕","吞","群挑","单挑"]

relations_2={"行为":["觅食","攻击"],"觅食":["乞讨","捕猎"],"攻击":["抓","咬"],"咬":["撕","吞"],"捕猎":["群挑","单挑"]}





class Animal(Alarm):
    Trees = [AttributeTree("归属",elements_1,relations_1),AttributeTree("行为",elements_2,relations_2)]

class TestAlarm():

    def test_len(self):
        alarm = Animal("爬行类","撕")
        assert  len(alarm) ==2

    def test_dissimilarity(self):
        #测试相似度
        a1 = Animal("爬行类","撕")
        a2 = Animal("爬行类","撕")
        a3 = Animal("爬行类","吞")
        a4 = Animal("动物","抓")
        assert a1.dissimilarity(a2) ==0
        assert a1.dissimilarity(a3) ==2
        k = a1.dissimilarity(a4)
        assert  k == 4

    def test_askey(self):
        #测试键
        a1 = Animal("爬行类", "撕")
        assert a1.askey() =="爬行类-撕"

    def test_equal(self):
        #测试等于
        a1 = Animal("爬行类","撕")
        a2 = Animal("爬行类","撕")
        assert a1 ==a2

    def test_update(self):
        #测试更新
        a2 = Animal("爬行类","撕")
        a3 = Animal("爬行类","咬")
        assert a3 == a2.update(1)