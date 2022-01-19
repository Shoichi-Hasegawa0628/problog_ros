#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from problog.program import PrologString
from problog import get_evaluatable

DATASET_FOLDER = "/root/HSR/catkin_ws/src/problog_ros/data/master_thesis/"
target_name = "sheep_doll"

TXT_DATA = DATASET_FOLDER + "logical_inference.txt"
f = open(TXT_DATA, 'r')
reasoning_data = f.readlines()
Query = "query(exist({}, Y)).\n".format(target_name)
reasoning_data.append(Query)
#print(reasoning_data)
reasoning_data = '\n'.join(reasoning_data)

# 論理推論の実行
p = PrologString(reasoning_data)
# 推論結果の出力
result = get_evaluatable().create_from(p).evaluate()
print(result)

