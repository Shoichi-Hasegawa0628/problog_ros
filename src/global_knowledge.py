#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 入力された物体名から存在しやすい場所の名前を論理推論するコード

######## 必要なライブラリ (Melodic環境 (Python2系環境)で動作させる場合) ########

## /root/RULO/catkin_ws/srcの中で
# git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc	
# echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
# echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# source ~/.bashrc

## /root/RULO/catkin_ws/srcの中で
# git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
# echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
# source ~/.bashrc

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

class LogicalInference():

  def __init__(self):
    #rospy.Subscriber("/human_command", String, self.word_callback, queue_size=1)
    pass


  def word_callback(self):
    word = rospy.wait_for_message("/human_command", String, timeout=None)

    # 推論モデルの読み込み
    object_name = word.data
    TXT_DATA = DATASET_FOLDER + object_name + ".txt"
    f = open(TXT_DATA, 'r')
    reasoning_data = f.readlines()
    reasoning_data = '\n'.join(reasoning_data)

    # 論理推論の実行
    p = PrologString(reasoning_data)

    # 推論結果の出力
    result = get_evaluatable().create_from(p).evaluate()
    #print (result)
    place_names_probs = {}

    # 推論した場所の単語と確率を辞書型に格納
    pre_prob = list(result.values())  # 場所の確率
    
    count = 0                         # 場所の単語 (場所の単語が最高で7文字なのでこのコードで動作可能)
    for key in result.keys(): 
      key_goal =len(str(key))
      place_name = str(key)[key_goal-8 : key_goal-1]

      if place_name.find(',') is not None:
        place_name = place_name[place_name.find(',') + 1 :]

      place_names_probs[place_name] = pre_prob[count]
      count += 1

    print(place_names_probs)
    return place_names_probs
    

if __name__ == "__main__":
  rospy.init_node('problog_logical_inference')
  l = LogicalInference()
  l.word_callback()
  rospy.spin()
