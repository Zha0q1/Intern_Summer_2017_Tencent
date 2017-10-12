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
		self.__round_count = 0

	def update(self, isHome, goal, result) :
		if self.__index == 5 :
			self.__index = 0
		if self.__index2 == 3 :
			self.__index2 = 0
		self.__point[self.__index] = 3 if result == 0 else (1 if result == 1 else 0)
		self.__goal[self.__index] = goal
		if isHome :
			self.__home_point[self.__index2] = 3 if result == 0 else (1 if result == 1 else 0)
			self.__home_goal[self.__index2] = goal
		else :
			self.__away_point[self.__index2] = 3 if result == 0 else (1 if result == 1 else 0)
			self.__away_goal[self.__index2] = goal
		self.__round_count += 1
		self.__index += 1
		self.__index2 += 1


	def get_point(self) :
		return sum(self.__point)

	def get_goal(self) : 
		return sum(self.__goal)

	def get_home_point(self) :
		return sum(self.__home_point)

	def get_away_point(self) :
		return sum(self.__away_point)

	def get_home_goal(self) :
		return sum(self.__home_goal)

	def get_away_goal(self) :
		return sum(self.__away_goal)
'''
team = GameRecord()
team.update(0,0)
team.update(1,1)
team.update(2,2)
team.update(2,2)
team.update(1,1)
team.update(0,0)
team.update(1,1)
team.update(1,1)
'''

#积分差&总进球差（近五场）
def get_datasets(formatted) :  
	dataset1 = []
	dataset2 = []
	dataset3 = []
	for season in range(2012,2017) :
		teams = {}
		for rround in range(1,26) :
			games = formatted[season-2012][rround-1]
			for game in games: 
				home_id = game[0]
				home_goal = game[1]
				away_id = game[2]
				away_goal = game[3]
				if home_id not in teams.keys():
					teams[home_id] = GameRecord()
				if away_id not in teams.keys():
					teams[away_id] = GameRecord()
				home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)
				away_result = 2 - home_result
				if rround > 5 :
					point_dif = teams[home_id].get_point() - teams[away_id].get_point()
					goal_dif = teams[home_id].get_goal() - teams[away_id].get_goal()
					home_away_point_dif = teams[home_id].get_home_point() \
						 - teams[away_id].get_away_point()
					home_away_goal_dif = teams[home_id].get_home_goal() \
						 - teams[away_id].get_away_goal()
					dataset1.append([point_dif,goal_dif,home_result])
					dataset2.append([point_dif,home_away_point_dif,home_result])
					dataset3.append([goal_dif,home_away_goal_dif,home_result])
				teams[home_id].update(True, home_goal,home_result)
				teams[away_id].update(False, away_goal,away_result)
				
	return dataset1, dataset2, dataset3

def get_testsets(formatted) :
	testset1 = []
	testset2 = []
	testset3 = []
	for season in range(2017,2018) :
		teams = {}
		for rround in range(1,11) :
			games = formatted[season-2012][rround-1]
			for game in games: 
				home_id = game[0]
				home_goal = game[1]
				away_id = game[2]
				away_goal = game[3]
				if home_id not in teams.keys():
					teams[home_id] = GameRecord()
				if away_id not in teams.keys():
					teams[away_id] = GameRecord()
				home_result = 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)
				away_result = 2 - home_result
				if rround > 5 :
					point_dif = teams[home_id].get_point() - teams[away_id].get_point()
					goal_dif = teams[home_id].get_goal() - teams[away_id].get_goal()
					home_away_point_dif = teams[home_id].get_home_point() \
						 - teams[away_id].get_away_point()
					home_away_goal_dif = teams[home_id].get_home_goal() \
						 - teams[away_id].get_away_goal()
					testset1.append([point_dif,goal_dif,home_result])
					testset2.append([point_dif,home_away_point_dif,home_result])
					testset3.append([goal_dif,home_away_goal_dif,home_result])
				teams[home_id].update(True, home_goal,home_result)
				teams[away_id].update(False, away_goal,away_result)
	return testset1, testset2, testset3


			

dataset1, dataset2, dataset3 = get_datasets(formatted)
testset1, testset2, testset3 = get_testsets(formatted)
#print(dataset1)
print(dataset2)
#print(dataset3)
#print(testset1)
#print(testset2)
#print(testset3)






