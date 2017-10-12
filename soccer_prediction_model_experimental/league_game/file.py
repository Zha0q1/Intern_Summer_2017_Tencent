raw = []
team_point = {}
train_start = 30
train_end = 60
dataset = []


with open("match.txt") as file :
	for line in file :
		raw.append(line.split("|"))
file.close()
for i in range(2,len(raw)) :
	home_id = int(raw[i][3])
	home_goal = int(raw[i][4])
	away_id = int(raw[i][5])
	away_goal = int(raw[i][6])
	if home_id not in team_point.keys():
		team_point[home_id] = [0,0,0] # total home away
	if away_id not in team_point.keys():
		team_point[away_id] = [0,0,0]
	team_point[home_id][0] += 3 if home_goal>away_goal else (1 if home_goal==away_goal else 0)
	team_point[home_id][1] += 3 if home_goal>away_goal else (1 if home_goal==away_goal else 0)
	team_point[away_id][0] += 0 if home_goal>away_goal else (1 if home_goal==away_goal else 3)
	team_point[away_id][2] += 0 if home_goal>away_goal else (1 if home_goal==away_goal else 3)
	if i >= train_start and i < train_end :
		dataset.append([team_point[home_id][0]-team_point[away_id][0] 
			, team_point[home_id][1]-team_point[away_id][2]
			, 0 if home_goal>away_goal else (1 if home_goal==away_goal else 2)])


print(dataset)

