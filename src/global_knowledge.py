#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 入力された物体名から存在しやすい場所の名前を論理推論するコード

## 必要なライブラリ (Melodic環境 (Python2系環境)で動作させる場合)
# apt-get install python3-pip
# python3 -m pip install problog
# python3 -m pip install pyyaml
# python3 -m pip install rospkg catkin_pkg


from problog.program import PrologString
from problog import get_evaluatable
import rospy
from std_msgs.msg import String
from __init__ import *

class LogicalInference():

  def __init__(self):
    rospy.Subscriber("/human_command", String, self.word_callback, queue_size=1)

  def word_callback(self, word):
    # 推論モデルの読み込み
    object_name = word.data
    #print(object_name)
    #print(type(object_name))
    #object_name = str(object_name)
    #rospy.loginfo("object_name: ", object_name)
    #object_name = "penguin_doll"
    TXT_DATA = DATASET_FOLDER + object_name + ".txt"
    #print(TXT_DATA)
    f = open(TXT_DATA, 'r')
    reasoning_data = f.readlines()
    reasoning_data = '\n'.join(reasoning_data)

    # 論理推論の実行
    p = PrologString(reasoning_data)

    # 推論結果の出力
    
    result = get_evaluatable().create_from(p).evaluate()
    print (result)
    pre_prob = list(result.values())
    print(pre_prob)
    
    #return result

    """
    max_value = max(result.values())
    print(max_value)
    max_key = str(max(result, key=result.get))
    print(max_key)
    key_start = max_key.find(',')
    key_goal = len(max_key)
    target_place = max_key[key_start+14 : key_goal-1]
    print(target_place)

    
    #対象の場所の語彙をtxtファイルへ書き出し
    path_w = "/root/HSR/catkin_ws/src/SpCoNavi/SIGVerse/planning/myfile.txt"
    f = open(path_w, 'w')
    f.write(target_place)
    f.close()

    #txtファイルの読み込み、変数へ代入
    with open(path_w) as f:
      target = f.read()
      print(target)

    #場所の語彙と対応する数字への置換
    list = {'entrance':0, 'living':1, 'dining':2, 'kitchen':3}
    target_instance = list[target]
    print(target_instance)
    """

if __name__ == "__main__":
  rospy.init_node('problog_logical_inference')
  LogicalInference()
  rospy.spin()
