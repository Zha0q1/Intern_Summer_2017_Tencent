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

def discretized_value(num, vector) :
	pos = 0
	for i in range(len(vector)) :
		if num > vector[i] :
			pos += 1
		else :
			return pos
	return pos

def odds_to_prob(odds):
	return 1/(float(odds)/0.9)

def fix_prob(b365h,b365d,b365a):
	b365h = odds_to_prob(b365h)
	b365d = odds_to_prob(b365d)
	b365a = odds_to_prob(b365a)
	sum = b365h + b365d + b365a
	b365h = int(b365h/sum*100)
	b365d = int(b365d/sum*100)
	b365a = int(b365a/sum*100)
	return b365h,b365d,b365a

def add_game(season_record,row):
	home_name = row[2]
	home_goal = int(row[4])
	away_name = row[3]
	away_goal = int(row[5])
	home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)
	away_result = 2 - home_result
	season_record.update(home_name,True, home_goal,home_result)
	season_record.update(away_name,False, away_goal,away_result)


pinpoints1 = [-11,-8,-5,-2,1,4,7,10]
pinpoints2 = [-7,-5,-3,-1,1,3,5,7]
pinpoints3 = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]

def populate_feature_set(season_record,row,feature_set):
	home_name = row[2]
	away_name = row[3]
	b365h = row[23]
	b365d = row[24]
	b365a = row[25]
	b365h,b365d,b365a = fix_prob(b365h,b365d,b365a)
	point_dif = season_record.get_point(home_name) - season_record.get_point(away_name)
	goal_dif = season_record.get_goal(home_name) - season_record.get_goal(away_name)
	home_away_point_dif = season_record.get_home_point(home_name) \
		- season_record.get_away_point(away_name)
	home_away_goal_dif = season_record.get_home_goal(home_name) \
		- season_record.get_away_goal(away_name)


	point_dif = discretized_value(point_dif,pinpoints1)
	goal_dif = discretized_value(goal_dif,pinpoints1)
	home_away_point_dif = discretized_value(home_away_point_dif,pinpoints2)
	home_away_goal_dif = discretized_value(home_away_goal_dif,pinpoints2)
	b365h = discretized_value(b365h,pinpoints3)
	b365d = discretized_value(b365d,pinpoints3)
	b365a = discretized_value(b365a,pinpoints3)


	feature_set.append([ point_dif,goal_dif,home_away_point_dif,home_away_goal_dif,
		b365h,b365d,b365a ])
	#feature_set.append([ b365h,b365d,b365a ])

def populate_class_set(row,class_set):
	home_goal = row[4]
	away_goal = row[5]
	home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)
	class_set.append(home_result)


import csv

feature_set = []
class_set = []

#280 matches per season
for year in range(2003,2018):
	if year == 2005:# error reading file 2005.csv 
		continue
	print(year)
	season_record = SeasonRecord(year)
	count = -1
	with open(str(year)+".csv") as file:
		reader = csv.reader(file)
		for row in reader:
			if count == -1:
				count += 1
				continue
			rround = int(count/10+1)
			if rround >= 6 and rround <= 33 :
				populate_feature_set(season_record,row,feature_set)
				populate_class_set(row,class_set)
			add_game(season_record,row)
				
			count +=1

print(feature_set)
print(class_set)

def verify_prediction(predictions,actuals,model_name):
	count = 0
	for i in range(len(predictions)):
		if predictions[i] == actuals[i]:
			#print("hit")
			count +=1
		#else:
			#print("miss")
	print("model: " + model_name)
	print("predicted: " + str(len(predictions)))
	print("hit: " + str(count))
	print("ratio: "+ str(count/len(predictions)))




import numpy as np
from sklearn.naive_bayes import *

feature_set1 = []
feature_set2 = []
feature_set3 = []
feature_set4 = []
for vector in feature_set[0:280*12]:
	feature_set1.append(vector[0:2])
	feature_set2.append(vector[2:4])
	feature_set3.append(vector[4:7])
	feature_set4.append(vector)

test_set1 = []
test_set2 = []
test_set3 = []
test_set4 = []
for vector in feature_set[280*12:280*14]:
	test_set1.append(vector[0:2])
	test_set2.append(vector[2:4])
	test_set3.append(vector[4:7])
	test_set4.append(vector)

class_set_sample = class_set[0:280*12]
class_set_test = class_set[280*12:280*14]


# model 1
X = np.array(feature_set1)
y = np.array(class_set_sample)
clf1 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf1.fit(X, y)
predictions1 = clf1.predict(test_set1)
verify_prediction(predictions1,class_set_test,"model 1")

# model 2
X = np.array(feature_set2)
y = np.array(class_set_sample)
clf2 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf2.fit(X, y)
predictions2 = clf2.predict(test_set2)
verify_prediction(predictions2,class_set_test,"model 2")

# model 3
X = np.array(feature_set3)
y = np.array(class_set_sample)
clf3 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf3.fit(X, y)
predictions3 = clf3.predict(test_set3)
verify_prediction(predictions3,class_set_test,"model 3")
import pickle 
f = open('model3.data','wb')  
pickle.dump(clf3, f)
f.close()  

# model 4
X = np.array(feature_set4)
y = np.array(class_set_sample)
clf4 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf4.fit(X, y)
predictions4 = clf4.predict(test_set4)
verify_prediction(predictions4,class_set_test,"model 4")




# model 5.1
X = np.array(feature_set1)
y = np.array(class_set_sample)
clf5_1 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf5_1.fit(X, y)
predictions5_1 = clf5_1.predict(feature_set1)
predictions5_1_2 = clf5_1.predict(test_set1)

# model 5.2
X = np.array(feature_set2)
y = np.array(class_set_sample)
clf5_2 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf5_2.fit(X, y)
predictions5_2 = clf5_2.predict(feature_set2)
predictions5_2_2 = clf5_2.predict(test_set2)

# model 5.3
X = np.array(feature_set3)
y = np.array(class_set_sample)
clf5_3 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf5_3.fit(X, y)
predictions5_3 = clf5_3.predict(feature_set3)
predictions5_3_2 = clf5_3.predict(test_set3)

# model 5
feature_set5 = []
test_set5 = []
for i in range(len(predictions5_1)):
	feature_set5.append([predictions5_1[i],predictions5_2[i],predictions5_3[i]])

for i in range(len(predictions5_1_2)):
	test_set5.append([predictions5_1_2[i],predictions5_2_2[i],predictions5_3_2[i]])


# model 5
X = np.array(feature_set5)
y = np.array(class_set_sample)
clf5 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf5.fit(X, y)
predictions5 = clf5.predict(test_set5)
verify_prediction(predictions5,class_set_test,"model 5")


