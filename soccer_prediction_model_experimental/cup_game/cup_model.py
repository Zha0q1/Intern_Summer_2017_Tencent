'''
import Queue
class TeamRecord :
	__elo = Queue.Queue(maxsize = 10)
	__goal = Queue.Queue(maxsize = 10)
	__count = 0

	def __init__(self):
		__elo = Queue.Queue(maxsize = 10)
		__goal = Queue.Queue(maxsize = 10)
		__count

	def add(self, elo, goal, result) :
		self.__elo.get()
		self.__elo.put(elo)
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

'''







import json

def load_json(file_name):
	with open(file_name) as json_file:
		data = json.load(json_file)
		return data

table = load_json('table.txt')

top50 = []

for team in table[0:50]:
	top50.append(team[1])

all_matches = load_json('matches.txt')
countries_abbr = load_json('countries_abbr.txt')

matches_selected = []

for country in top50:
	#print(country)
	for match in all_matches[country]:
		if match[2] in top50 and match[3] in top50:
			matches_selected.append(match)

def get_last_three_goal_scored_sum(country,month_day,year):
	index = -1
	for match in all_matches[country]:
		#print(country)
		#print(match[0],match[1],month_day,year)
		if match[0] == month_day and match[1] == year:
			index = match[-1]-1
			break
	sum = 0
	if index-3 < 0 :
		return -1
	for i in range(index-3,index):
		match = all_matches[country][i]
		if country == match[2]:
			sum += int(all_matches[country][i][4])
		if country == match[3]:
			sum += int(all_matches[country][i][5])
	return sum

def get_last_three_goal_conceded_sum(country,month_day,year):
	index = -1
	for match in all_matches[country]:
		if match[0] == month_day and match[1] == year:
			index = match[-1]-1
			break
	sum = 0
	if index-3 < 0 :
		return -1
	for i in range(index-3,index):
		match = all_matches[country][i]
		if country == match[2]:
			sum += int(all_matches[country][i][5])
		if country == match[3]:
			sum += int(all_matches[country][i][4])
	return sum

def get_elo_three_ago(country,month_day,year):
	index = -1
	for match in all_matches[country]:
		if match[0] == month_day and match[1] == year:
			index = match[-1]-1
			break
	if index-4 < 0:
		return 9999
	#print(all_matches[country][index-3])
	if country == all_matches[country][index-4][2]:
		return int(all_matches[country][index-4][10])
	if country == all_matches[country][index-4][3]:
		return int(all_matches[country][index-4][11])

def get_elo(country,month_day,year):
	index = -1
	for match in all_matches[country]:
		if match[0] == month_day and match[1] == year:
			index = match[-1]-1
			break
	if index-1 < 0:
		return 9999
	#print(all_matches[country][index-3])
	if country == all_matches[country][index-1][2]:
		return int(all_matches[country][index-1][10])
	if country == all_matches[country][index-1][3]:
		return int(all_matches[country][index-1][11])


def discretized_value(num, vector) :
	pos = 0
	for i in range(len(vector)) :
		if num > vector[i] :
			pos += 1
		else :
			return pos
	return pos

pinpoints1 = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5]
pinpoints2 = [-400,-350,-300,-250,-200,-150,-100,-50,0,50,100,150,200,250,300,350,400]
pinpoints3 = [-100,-90,-80,-70,-60,-50,-40,-30,-20,-10,-0,10,20,30,40,50,60,70,80,90,100]
pinpoints4 = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]

feature_set = []
class_set = []

for match in matches_selected:
	#print(match)
	year = match[1]
	month_day = match[0]
	home_goal = match[4]
	away_goal = match[5]
	home_last_three_goal_scored_sum = get_last_three_goal_scored_sum(match[2],month_day,year)
	home_last_three_goal_conceded_sum = get_last_three_goal_conceded_sum(match[2],month_day,year)
	away_last_three_goal_scored_sum = get_last_three_goal_scored_sum(match[3],month_day,year)
	away_last_three_goal_conceded_sum = get_last_three_goal_conceded_sum(match[3],month_day,year)
	home_elo_three_ago = get_elo_three_ago(match[2],month_day,year)
	away_elo_three_ago = get_elo_three_ago(match[3],month_day,year)
	home_elo = get_elo(match[2],month_day,year)
	away_elo = get_elo(match[3],month_day,year)
	#print(home_elo,home_elo_three_ago,away_elo,away_elo_three_ago)
	if home_last_three_goal_scored_sum < 0:
		continue
	if home_last_three_goal_conceded_sum < 0:
		continue
	if away_last_three_goal_scored_sum < 0:
		continue
	if away_last_three_goal_conceded_sum < 0:
		continue
	if home_elo_three_ago == 9999 or home_elo_three_ago == None:
		continue
	if away_elo_three_ago == 9999 or away_elo_three_ago == None:
		continue
	if home_elo == 9999 or home_elo == None:
		continue
	if away_elo == 9999 or away_elo == None:
		continue
	
	scored_dif = home_last_three_goal_scored_sum - away_last_three_goal_scored_sum
	conceded_dif = home_last_three_goal_conceded_sum - away_last_three_goal_conceded_sum
	elo_dif = home_elo - away_elo
	home_elo_dif =  home_elo - home_elo_three_ago
	away_elo_dif =  away_elo - away_elo_three_ago
	home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)

	

	scored_dif = discretized_value(scored_dif, pinpoints1)
	conceded_dif = discretized_value(conceded_dif, pinpoints1)
	elo_dif = discretized_value(elo_dif, pinpoints2)
	home_elo_dif = discretized_value(home_elo_dif,pinpoints3)
	away_elo_dif = discretized_value(away_elo_dif,pinpoints3)
	#print(home_elo_dif,away_elo_dif)
	feature_set.append([scored_dif,conceded_dif,elo_dif,home_elo_dif,away_elo_dif])

	class_set.append(home_result)



def verify_prediction(predictions,actuals,model_name):
	count = 0
	for i in range(len(predictions)):
		#print(predictions[i])
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
for vector in feature_set[0:16000]:
	feature_set1.append(vector[0:2])
	feature_set2.append(vector[2:5])
	feature_set3.append(vector)

test_set1 = []
test_set2 = []
test_set3 = []
for vector in feature_set[16000:]:
	test_set1.append(vector[0:2])
	test_set2.append(vector[2:5])
	test_set3.append(vector)

class_set_sample = class_set[0:16000]
class_set_test = class_set[16000:]


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
print(clf3.predict_proba([test_set3[-1]]))

# model 4.1
X = np.array(feature_set1)
y = np.array(class_set_sample)
clf4_1 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf4_1.fit(X, y)
predictions4_1 = clf4_1.predict(feature_set1)
predictions4_1_2 = clf4_1.predict(test_set1)

# model 4.2
X = np.array(feature_set2)
y = np.array(class_set_sample)
clf4_2 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf4_2.fit(X, y)
predictions4_2 = clf4_2.predict(feature_set2)
predictions4_2_2 = clf4_2.predict(test_set2)

# model 4
feature_set4 = []
test_set4 = []
for i in range(len(predictions4_1)):
	feature_set4.append([predictions4_1[i],predictions4_2[i]])

for i in range(len(predictions4_1_2)):
	test_set4.append([predictions4_1_2[i],predictions4_2_2[i]])


# model 4
X = np.array(feature_set4)
y = np.array(class_set_sample)
clf4 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf4.fit(X, y)
predictions4 = clf4.predict(test_set4)
verify_prediction(predictions4,class_set_test,"model 4")
print(clf4.predict_proba([[0,0]]))

# model 5.1
X = np.array(feature_set1)
y = np.array(class_set_sample)
clf5_1 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf5_1.fit(X, y)
predictions5_1 = clf5_1.predict_proba(feature_set1)
predictions5_1_2 = clf5_1.predict_proba(test_set1)

# model 5.2
X = np.array(feature_set2)
y = np.array(class_set_sample)
clf5_2 = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=False)
clf5_2.fit(X, y)
predictions5_2 = clf5_2.predict_proba(feature_set2)
predictions5_2_2 = clf5_2.predict_proba(test_set2)

# model 5
feature_set5 = []
test_set5 = []
for i in range(len(predictions5_1)):
	features = []
	for j in range(len(predictions5_1[0])):
		features.append(discretized_value(predictions5_1[i][j]*100,pinpoints4))
	for j in range(len(predictions5_2[0])):
		features.append(discretized_value(predictions5_2[i][j]*100,pinpoints4))
	feature_set5.append(features)

for i in range(len(predictions5_1_2)):
	features = []
	for j in range(len(predictions5_1_2[0])):
		features.append(discretized_value(predictions5_1_2[i][j]*100,pinpoints4))
	for j in range(len(predictions5_2_2[0])):
		features.append(discretized_value(predictions5_2_2[i][j]*100,pinpoints4))
	test_set5.append(features)



# model 5
X = np.array(feature_set5)
y = np.array(class_set_sample)
clf5 = GaussianNB()
clf5.fit(X, y)
predictions5 = clf5.predict(test_set5)
verify_prediction(predictions5,class_set_test,"model 5")
print(clf5.predict_proba([[7, 6, 5, 9, 7, 3]]))

import pickle 
import numpy as np
from sklearn.naive_bayes import *

clf100 = pickle.load(open("model3.data","rb"))

def odds_to_prob(odds):
	return 1/(float(odds)/0.9)

def fix_prob(b365h,b365d,b365a):
	b365h = odds_to_prob(b365h)
	b365d = odds_to_prob(b365d)
	b365a = odds_to_prob(b365a)
	sum = b365h + b365d + b365a
	b365h = b365h/sum
	b365d = b365d/sum
	b365a = b365a/sum
	return [b365h,b365d,b365a]

def model_predict_single(feature_set,clf,odds):
	proba1 = clf.predict_proba(feature_set)[0]
	print("model:")
	print(proba1)
	odds_prab = fix_prob(odds[0],odds[1],odds[2])
	print("odds:")
	print(odds_prab)
	proba = proba1+odds_prab
	proba /= sum(proba)
	print('overall:')
	print(proba)

odds = [1.25,5.5,12]

feature_set_m3 = [
	discretized_value(7-2,pinpoints1),
	discretized_value(4-2,pinpoints1),
	discretized_value(1683-1574,pinpoints2),
	discretized_value(1683-1652,pinpoints3),
	discretized_value(1574-1583,pinpoints4),
	]

#model_predict_single(feature_set_m3,clf3,odds)

feature_set_m4 = [ 
	clf4_1.predict([discretized_value(7-2,pinpoints1),discretized_value(4-2,pinpoints1)]) ,
	clf4_2.predict([discretized_value(1683-1574,pinpoints2),discretized_value(1683-1652,pinpoints3),discretized_value(1574-1583,pinpoints4)])
	]

#model_predict_single([0,0],clf4,odds)
