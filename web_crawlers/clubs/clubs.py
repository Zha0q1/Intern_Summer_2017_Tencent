import json
import datetime
import urllib2
import random
import csv
import os
import time

def get_and_parse_data(start_time):
	today = datetime.date.today()
	url = 'http://api.clubelo.com/'+today.isoformat()
	
	headers_set = []
	headers1 = {
    	'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}
	headers2 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/51.0.2704.63 Safari/537.36'
	}
	headers3 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
	}
	headers_set.append(headers1)
	headers_set.append(headers2)
	headers_set.append(headers3)

	req = urllib2.Request(
	    url = url,
	    headers = headers_set[random.randint(0,len(headers_set)-1)]
	)
	try:
		result = urllib2.urlopen(req).read()
	except:
		if (datetime.datetime.now()-start_time).seconds > 180:
			print('timeout, exiting')
			quit()
		else:
			return get_and_parse_data(start_time)
	else:
		result = urllib2.urlopen(req).read()
		file_object = open('club_'+today.isoformat()+'.csv', 'w')
		file_object.write(result)
		file_object.close( )

		clubs = []
		
		with open('club_'+today.isoformat()+'.csv') as file:
			reader = csv.reader(file)
			for row in reader:
				if not row:
					continue
				if row[0] != 'Rank':
					rank = 'None' if (row[0]=='None') else int(row[0])
					level = int(row[3])
					elo = float(row[4])
					clubs.append([rank,row[1],row[2],level,elo,row[5],row[6]])
		os.remove('club_'+today.isoformat()+'.csv')
		return today.isoformat(),clubs

print("getting clubs elo --- "+time.strftime("%Y-%m-%d %H:%M:%S"))

date,clubs = get_and_parse_data(datetime.datetime.now())

in_json = json.dumps(clubs)
file_object = open('clubs_'+date+'.txt', 'w')
file_object.write(in_json)
file_object.close( )

print("done --- "+time.strftime("%Y-%m-%d %H:%M:%S"))
