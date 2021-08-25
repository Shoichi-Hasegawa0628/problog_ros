# -*- coding: utf-8 -*-
#ProbLogのライブラリ
from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable

#事前知識
#a = " \"\"\"  a  \"\"\"  " #これをtextファイルか何かで推論モデルを読み込むことができれば、できそう？
#print(a)

p = PrologString("""
place(living).
place(bedroom).
place(kitchen).
place(toilet).

food(orange).
food(apple).

doll(rabbit_doll). 			               
doll(bear_doll).   			                               
doll(monkey_doll).			                               

0.4 :: exist(rabbit_doll, living).                         
0.3 :: exist(rabbit_doll, bedroom).	                        
0.15 :: exist(rabbit_doll, kitchen).	                   
0.15 :: exist(rabbit_doll,toilet ).	                        

same_group(X, rabbit_doll) :- doll(X).
0.5 :: exist(X, rabbit_doll, Y) :- same_group(X, rabbit_doll), exist(rabbit_doll, Y).

query(exist(bear_doll, rabbit_doll, Y)).         
""")


#推論結果の出力
result = get_evaluatable().create_from(p).evaluate()
print (result)
max_value = max(result.values())
print(max_value)


max_key = str(max(result, key=result.get))
print(max_key)
key_start = max_key.find(',')
key_goal = len(max_key)
target_place = max_key[key_start+13 : key_goal-1]
print(target_place)

"""
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
