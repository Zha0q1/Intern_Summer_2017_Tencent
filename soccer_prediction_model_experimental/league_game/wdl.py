


#Zhaoqi Zhu
import math
"""
比赛结果--分类
"""
n = 3
class_map = {0:"主胜", 1:"平局", 2:"客胜"}
class_discretization = [0,1]
"""
考虑因素--特征
模型1
	1、积分差 主-客
	2、球差
模型2
	1、主主场积分-客客场积分
	2、主主场积分-客客场积分
模型2
	1、主主场进球-客客场进球
	2、主主场进球-客客场进球
离散修正：左开右闭
"""
discretization_set = [  [[-11,-8,-5,-2,1,4,7,10],[-11,-8,-5,-2,1,4,7,10]] , 

	[[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7]] , 
	[[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7]] , 
	[[0,1],[0,1],[0,1]]  ]


#依据分类标准将数据归类
def discretized_value(num, vector) :
	pos = 0
	for i in range(len(vector)) :
		if num > vector[i] :
			pos += 1
		else :
			return pos
	return pos




#读文件
raw = []
formatted = [[[] for i in range(30)] for j in range(6)]

with open("match.txt") as file :
	for line in file :
		raw.append(line.split("|"))
file.close();

for i in range(2,len(raw)): 
	line = raw[i]
	formatted[int(line[1])-2012][int(line[2])-1].append([int(line[5]),int(line[6]),
		int(line[7]),int(line[8])])
	
#print(formatted[2017-2012][9-1])




class GameRecord :
	__point = [0 for i in range(5)]
	__goal = [0 for i in range(5)]
	__home_point = [0 for i in range(3)]
	__away_point = [0 for i in range(3)]
	__home_goal = [0 for i in range(3)]
	__away_goal = [0 for i in range(3)]
	__index = 0
	__index2 = 0
	__index3 = 0
	__home_count = 0
	__away_count = 0
	__round_count = 0

	def __init__(self):
		self.__point = [0 for i in range(5)]
		self.__goal = [0 for i in range(5)]
		self.__home_point = [0 for i in range(3)]
		self.__away_point = [0 for i in range(3)]
		self.__home_goal = [0 for i in range(3)]
		self.__away_goal = [0 for i in range(3)]
		self.__index = 0
		self.__index2 = 0
		self.__index3 = 0
		self.__home_count = 0
		self.__away_count = 0
		self.__round_count = 0

	def update(self, isHome, goal, result) :
		if self.__index == 5 :
			self.__index = 0
		if self.__index2 == 3 :
			self.__index2 = 0
		if self.__index3 == 3 :
			self.__index3 = 0
		self.__point[self.__index] = 3 if result == 0 else (1 if result == 1 else 0)
		self.__goal[self.__index] = goal
		if isHome :
			self.__home_count += 1
			self.__home_point[self.__index2] = 3 if result == 0 else (1 if result == 1 else 0)
			self.__home_goal[self.__index2] = goal
		else :
			self.__away_count += 1 
			self.__away_point[self.__index3] = 3 if result == 0 else (1 if result == 1 else 0)
			self.__away_goal[self.__index3] = goal
		self.__round_count += 1
		self.__index += 1
		self.__index2 += 1
		self.__index3 += 1


	def get_point(self) :
		return sum(self.__point)

	def get_goal(self) : 
		return sum(self.__goal)

	def get_home_point(self) :
		if self.__home_count < 3 and self.__home_count > 0:
			return sum(self.__home_point)*3/float(self.__home_count)
		return sum(self.__home_point)

	def get_away_point(self) :
		if self.__away_count < 3 and self.__away_count > 0:
			return sum(self.__away_point)*3/float(self.__away_count)
		return sum(self.__away_point)

	def get_home_goal(self) :
		if self.__home_count < 3 and self.__home_count > 0:
			return sum(self.__home_goal)*3/float(self.__home_count)
		return sum(self.__home_goal)

	def get_away_goal(self) :
		if self.__away_count < 3 and self.__away_count > 0:
			return sum(self.__away_goal)*3/float(self.__away_count)
		return sum(self.__away_goal)

class SeasonRecord :
	__season_id = 0
	__teams = {}
	__current_round = 0

	def __init__(self, season_id) : 
		self.season_id = season_id
		self.__teams = {}
		self.__current_round

	def update_round(self, round) :
		self.__current_round = round

	def get_current_round(self):
		return self.__current_round

	def add_team(self, team_id) :
		self.__teams[team_id] = GameRecord()

	def update(self, team_id, isHome, goal, result) :
		if team_id not in self.__teams.keys():
			self.add_team(team_id)
		self.__teams[team_id].update(isHome,goal,result)

	def get_point(self, team_id) :
		return self.__teams[team_id].get_point()

	def get_goal(self, team_id) : 
		return self.__teams[team_id].get_goal()

	def get_home_point(self, team_id) :
		return self.__teams[team_id].get_home_point()

	def get_away_point(self, team_id) :
		return self.__teams[team_id].get_away_point()

	def get_home_goal(self, team_id) :
		return self.__teams[team_id].get_home_goal()

	def get_away_goal(self, team_id) :
		return self.__teams[team_id].get_away_goal()






season_records = {}


#生成五个模型所需数据
def get_datasets(formatted) :  
	dataset1 = []
	dataset2 = []
	dataset3 = []
	dataset4 = []
	dataset5 = []
	for season_id in range(2012,2017) :
		season_records[season_id] = SeasonRecord(season_id)
		season_record = season_records[season_id]
		for rround in range(1,26) :
			games = formatted[season_id-2012][rround-1]
			for game in games: 
				home_id = game[0]
				home_goal = game[1]
				away_id = game[2]
				away_goal = game[3]
				home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)
				away_result = 2 - home_result
				if rround > 6 :
					goal_dif_this_match = home_goal - away_goal
					goal_dif_class = discretized_value(goal_dif_this_match,class_discretization) 
					point_dif = season_record.get_point(home_id) - season_record.get_point(away_id)
					goal_dif = season_record.get_goal(home_id) - season_record.get_goal(away_id)
					home_away_point_dif = season_record.get_home_point(home_id) \
						 - season_record.get_away_point(away_id)
					home_away_goal_dif = season_record.get_home_goal(home_id) \
						 - season_record.get_away_goal(away_id)
					dataset1.append([point_dif,goal_dif,home_result])
					dataset2.append([home_away_point_dif,home_away_goal_dif,home_result])
					dataset3.append([point_dif,home_away_point_dif,home_result])
					dataset4.append([goal_dif,home_away_goal_dif,home_result])
					dataset5.append([point_dif,home_away_point_dif,goal_dif,home_away_goal_dif,home_result])
				season_record.update(home_id,True, home_goal,home_result)
				season_record.update(away_id,False, away_goal,away_result)
			season_record.update_round(rround)
	
	return dataset1, dataset2, dataset3, dataset4, dataset5
#五个测试集
def get_testsets(formatted) :
	testset1 = []
	testset2 = []
	testset3 = []
	testset4 = []
	testset5 = []
	for season_id in range(2017,2018) :
		season_records[season_id] = SeasonRecord(season_id)
		season_record = season_records[season_id]
		for rround in range(1,11) :
			games = formatted[season_id-2012][rround-1]
			for game in games: 
				home_id = game[0]
				home_goal = game[1]
				away_id = game[2]
				away_goal = game[3]
				home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)
				away_result = 2 - home_result
				if rround > 5 :
					goal_dif_this_match = home_goal - away_goal
					goal_dif_class = discretized_value(goal_dif_this_match,class_discretization) 
					point_dif = season_record.get_point(home_id) - season_record.get_point(away_id)
					goal_dif = season_record.get_goal(home_id) - season_record.get_goal(away_id)
					home_away_point_dif = season_record.get_home_point(home_id) \
						 - season_record.get_away_point(away_id)
					home_away_goal_dif = season_record.get_home_goal(home_id) \
						 - season_record.get_away_goal(away_id)
					testset1.append([point_dif,goal_dif,home_result])
					testset2.append([home_away_point_dif,home_away_goal_dif,home_result])
					testset3.append([point_dif,home_away_point_dif,home_result])
					testset4.append([goal_dif,home_away_goal_dif,home_result])
					testset5.append([point_dif,home_away_point_dif,goal_dif,home_away_goal_dif,home_result])
				season_record.update(home_id,True, home_goal,home_result)
				season_record.update(away_id,False, away_goal,away_result)
			season_record.update_round(rround)

	return testset1, testset2, testset3, testset4, testset5



			

dataset1, dataset2, dataset3, dataset4, dataset5 = get_datasets(formatted)
testset1, testset2, testset3, testset4, testset5 = get_testsets(formatted)



#训练！返回格式 [[[]]] 第一层：分类 第二层：特征 第三层：特征的归类 
#probabilities[-1] 为一维list，存放分类的概率
def train(dataset, discretization) :
	counts = [[[0]*(len(vector)+1) for vector in discretization] for j in \
		range(n)] # counts for conditional p's
	counts.append([0]*n) 
	#计数统计
	for vector in dataset :
		counts[-1][vector[-1]] += 1
		for i in range(len(vector)-1) :
			num = discretized_value(vector[i], discretization[i])
			counts[vector[-1]][i][num] += 1
	probabilities = []
	#转换成概率，使用Laplace校准
	for i in range(len(counts)-1) :
		probabilities.append([])
		for j in range(len(counts[i])) :
			probabilities[-1].append([])
			for num in counts[i][j]:
				probabilities[-1][-1].append((num+1)/(counts[-1][i]+len(discretization[j])+1))
	probabilities.append([])
	for num in counts[-1] :
		probabilities[-1].append(num/len(dataset))
	return probabilities
#根据probabilities对input进行分类
def classifier(input, probabilities, discretization) :
	calc_probabilities = []
	for i in range(len(probabilities)-1) :
		p = probabilities[-1][i]
		for j in range(len(probabilities[i])) :
			p *= probabilities[i][j][discretized_value(input[j],discretization[j])]
		calc_probabilities.append(p)
	return calc_probabilities
#返回所计算出概率中最大者对应类别
def determine_class(calc_probabilities) :
	maximum = max(enumerate(calc_probabilities),key=lambda x: x[1])[0]
	return maximum
def determine_report(calc_probabilities) :
	report = ""
	sum = 0
	for p in calc_probabilities: 
		sum += p
	for i in range(len(calc_probabilities)) : 
		report += (class_map[i] + ": " + str(int(calc_probabilities[i]/sum*100)) + "% ")
	return report

def level1(dataset_set):
	probabilities_set = []
	for i in range(len(dataset_set)) : 
		dataset = dataset_set[i]
		probabilities_set.append(train(dataset, discretization_set[i]))
	return probabilities_set

def generate_dataset_from_level1(dataset_set, probabilities_set):
	dataset_level2 = [[] for i in range(len(dataset_set[0])) ]
	for i in range(len(dataset_set)) : 
		dataset = dataset_set[i]
		for j in range(len(dataset)) :
			vector = dataset[j]
			calc_p = classifier(vector[0:len(vector)-1],probabilities_set[i],discretization_set[i])
			dataset_level2[j].append(determine_class(calc_p))
	for i in range(len(dataset_set[0])):
		dataset_level2[i].append(dataset_set[0][i][-1])
	return dataset_level2

def level2(dataset_level2):
	return train(dataset_level2,discretization_set[-1])

def generate_input_from_level1(inputset, probabilities_set) : 
	input_level2 = []
	for i in range(len(inputset)): 
		calc_p = classifier(inputset[i],probabilities_set[i],discretization_set[i])
		input_level2.append(determine_class(calc_p))
	return input_level2

def generate_testset_from_level1(testtset_set, probabilities_set): 
	testset_level2 = []
	for j in range(len(testtset_set[0])) : 
		inputset_level1 = []
		for i in range(len(testtset_set)) :
			inputset_level1.append(testset_set[i][j][0:len(testset_set[i][j])-1])
		test_input_level2 = generate_input_from_level1(inputset_level1,probabilities_set)
		test_input_level2.append(testset_set[0][j][-1])
		testset_level2.append(test_input_level2)
	return testset_level2

def mass_predict(testset, probabilities,discretization):
	hit = 0
	for input in testset: 
		calc_p = classifier(input[0:len(input)-1],probabilities,discretization)
		cclass = determine_class(calc_p)
		print(cclass)
		if input[-1] == cclass :
			hit += 1
	return float(hit)/float(len(testset))


dataset_set = [dataset1,dataset3,dataset4]
probabilities_set = level1(dataset_set)
dataset_level2 = generate_dataset_from_level1(dataset_set,probabilities_set)
probabilities_level2 = level2(dataset_level2)

testset_set = [testset1,testset3,testset4]
testset_level2 = generate_testset_from_level1(testset_set,probabilities_set)


ratio = mass_predict(testset_level2,probabilities_level2,discretization_set[-1])
print("2-level model")
print(ratio)

print("model 1")
ratio = mass_predict(testset1,probabilities_set[0],discretization_set[0])
print(ratio)
print("model 2")
ratio = mass_predict(testset2,probabilities_set[1],discretization_set[1])
print(ratio)
print("model 3")
ratio = mass_predict(testset2,probabilities_set[2],discretization_set[2])
print(ratio)

probabilities_new = train(dataset5,[[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7],[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7]])
ratio = mass_predict(testset5,probabilities_new,[[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7],[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7]])
print("1level model")
print(ratio)


input_guoan = [[5,1],[5,3],[1,2]]
print(generate_input_from_level1(input_guoan,probabilities_set))
calc_p = classifier(generate_input_from_level1(input_guoan,probabilities_set),probabilities_level2,discretization_set[-1])
print(calc_p)
print(determine_report(calc_p))

calc_p = classifier([5,3,1,2],probabilities_new,[[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7],[-11,-8,-5,-2,1,4,7,10],[-7,-5,-3,-1,1,3,5,7]])
print(determine_report(calc_p))

import json
data = {"teamInfo": {"homeName": "上海上港","homeId": 7697,"awayName": "北京国安","awayId": 1378},
	"result_odds":{"w":0.65,"d":0.19,"l":0.15},
	"goal_dif_odds":{"-3":0,"-2":0.02,"-1":0.14,"0":0.20,"+1":0.38,"+2":0.08,"+3":0.15},
	"point":{"shanggang":23,"guoan":15},
	"goal":{"shanggang":23,"guoan":15},
	"point_last_five":{"shanggang":13,"guoan":8},
	"goal_last_five":{"shanggang":11,"guoan":10},
	"home_point_last_three":{"shanggang":9,"guoan":2},
	"home_goal_last_three":{"shanggang":8,"guoan":4},
	"away_point_last_three":{"shanggang":7,"guoan":6},
	"away_goal_last_three":{"shanggang":5,"guoan":6}
	}
in_json = json.dumps(data)
print(in_json)





#probabilities = train(ddataset,[[-9,-6,-3,0,3,6,9],[-9,-6,-3,0,3,6,9]])
#print(mass_predict(probabilities,ttestset))
#print("shanggang vs guoan")
#calc_p = classifier([1,0],probabilities,[[-9,-6,-3,0,3,6,9],[-9,-6,-3,0,3,6,9]])
#print(determine_report(calc_p))

'''
#测试一下
dataset_set = []
dataset_set.append(generate_dataset())
dataset_set.append(generate_dataset())

probabilities_set = level1(dataset_set)

dataset2 = generate_dataset_from_level1(dataset_set,probabilities_set)

probabilities2 = level2(dataset2)

#print(probabilities)
#print(calc_p)
#print(cclass)
#print(dataset2)
input_set = [[-5,-5],[-5,-5]]

input2 = translate_level1_input_to_level2(input_set,probabilities_set)
print(input2)

calc_p = classifier(input2,probabilities2,discretization_set[-1])
print(determine_report(calc_p))

calc_p2 = classifier([-5,-5],probabilities_set[0],discretization_set[0])
print(determine_report(calc_p2))
'''


		
	