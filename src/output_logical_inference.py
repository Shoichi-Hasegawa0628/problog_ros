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
import os
from std_msgs.msg import String
from __init__ import *
import csv
DATASET_FOLDER = "/root/HSR/catkin_ws/src/problog_ros/data/irex2022/"

class LogicalInference():

  def __init__(self):
    pass


  def word_callback(self, target_name):
    # word = rospy.wait_for_message("/human_command", String, timeout=None)

    # 推論モデルの読み込み
    # object_name = word.data
    object_name = target_name
    TXT_DATA = DATASET_FOLDER + "logical_inference.txt"
    f = open(TXT_DATA, 'r')
    reasoning_data = f.readlines()
    Query = "query(exist({}, Y)).\n".format(object_name)
    reasoning_data.append(Query)
    reasoning_data = '\n'.join(reasoning_data)

    # 論理推論の実行
    p = PrologString(reasoning_data)

    # 推論結果の出力
    result = get_evaluatable().create_from(p).evaluate()
    # print("ProbLog result of reasoning\n")
    # print (result)
    # print("****************************************************************\n")

    # 推論した場所の単語と確率を辞書型に格納
    pre_prob = list(result.values())  # 場所の確率

    # 場所の単語一覧をロード
    with open(DATASET_FOLDER + 'W_list.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
        pass
      place_name_list = row

    place_name_probs = [0, 0, 0]
    #print(place_name_list)
    count = 0                         # 場所の単語 (場所の単語が最高で7文字なのでこのコードで動作可能)
    ct = 1
    for key in result.keys():
      #print(str(key))
      key_goal =len(str(key))
      #place_name = str(key)[key_goal - 7: key_goal - 1]
      if ct == 1:
        place_name = str(key)[key_goal-7 : key_goal-1]
        #print(place_name)
      elif ct == 2:
        place_name = str(key)[key_goal - 8: key_goal - 1]
        #print(place_name)
      else:
        place_name = str(key)[key_goal - 8: key_goal - 1]
        #print(place_name)
      # else:
      #   place_name = str(key)[key_goal - 9: key_goal - 1]
      # print(place_name)
      # ct += 1

      if place_name.find(',') is not None:
        place_name = place_name[place_name.find(',') + 1 :]

      j = place_name_list.index(place_name)
      place_name_probs[j] = pre_prob[count]
      count += 1
      ct += 1

    #print(place_name_probs)
    place_name_probs = [float(i)/sum(place_name_probs) for i in place_name_probs]  #正規化
    # print(sum(place_name_probs))
    #print(place_name_probs)
    self.save_data(place_name_probs, place_name_list, object_name)
    return place_name_probs


  def save_data(self, prob, place_name_list, object_name):
    # 推論結果をtxtでまとめて保存
    FilePath = "/root/HSR/catkin_ws/src/spco2_boo_problog/data/" + str(object_name)
    if not os.path.exists(FilePath):
      os.makedirs(FilePath)
    with open(FilePath + "/logical_inference_result.txt", "w") as f:
      f.write("Result of inference:\n")
      f.write("{} = {}\n".format(place_name_list, prob))
      f.close()


if __name__ == "__main__":
  rospy.init_node('problog_logical_inference')
  l = LogicalInference()
  #l.word_callback()
  #rospy.spin()
