#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 入力された物体名から存在しやすい場所の名前を論理推論するコード

# apt-get install python3-pip
# python3 -m pip install problog
# python3 -m pip install pyyaml
# python3 -m pip install rospkg catkin_pkg
###############################################################################

from problog.program import PrologString
from problog import get_evaluatable
import rospy
from std_msgs.msg import String
from __init__ import *
import csv
DATASET_FOLDER = "/root/RULO/catkin_ws/src/problog_ros/data/"

class LogicalInference():

  def __init__(self):
    pass


  def word_callback(self):
    word = rospy.wait_for_message("/human_command", String, timeout=None)

    # 推論モデルの読み込み
    object_name = word.data
    #object_name = "pig_doll"
    TXT_DATA = DATASET_FOLDER + object_name + ".txt"
    f = open(TXT_DATA, 'r')
    reasoning_data = f.readlines()
    reasoning_data = '\n'.join(reasoning_data)

    # 論理推論の実行
    p = PrologString(reasoning_data)

    # 推論結果の出力
    result = get_evaluatable().create_from(p).evaluate()
    print("ProbLog result of reasoning\n")
    print (result)
    print("****************************************************************\n")

    # 推論した場所の単語と確率を辞書型に格納
    pre_prob = list(result.values())  # 場所の確率

    # 場所の単語一覧をロード
    with open('../data/3LDK_01_w_index_1_0.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
        pass
      place_name_list = row

    place_name_probs = [0, 0, 0, 0]
    count = 0                         # 場所の単語 (場所の単語が最高で7文字なのでこのコードで動作可能)
    for key in result.keys(): 
      key_goal =len(str(key))
      place_name = str(key)[key_goal-8 : key_goal-1]

      if place_name.find(',') is not None:
        place_name = place_name[place_name.find(',') + 1 :]

      j = place_name_list.index(place_name)
      place_name_probs[j] = pre_prob[count]
      count += 1

    #print(place_name_probs)
    place_name_probs = [float(i)/sum(place_name_probs) for i in place_name_probs]  #正規化
    #print(sum(place_name_probs))
    return place_name_probs


if __name__ == "__main__":
  rospy.init_node('problog_logical_inference')
  l = LogicalInference()
  l.word_callback()
  #rospy.spin()
