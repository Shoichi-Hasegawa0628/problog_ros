#ProbLogのライブラリ
from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable

#事前知識
p = PrologString("""
0.3::exist(bottle,balcony).
0.6::exist(bottle,entrance).
0.2::exist(bottle,dining).
0.6::exist(cup,living).
0.8::exist(cup,living).
query(exist(bottle,X)).
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
target_place = max_key[key_start+1 : key_goal-1]
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
