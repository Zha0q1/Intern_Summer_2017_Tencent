import urllib2
import json
import threading
import datetime
import sys
import os
import random
import shutil  
import time

def get_index(start_time):
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
	    url = 'http://www.eloratings.net/world.html',
	    headers = headers_set[random.randint(0,len(headers_set)-1)]
	)
	try:
		result = urllib2.urlopen(req).read()
	except:
		if (datetime.datetime.now()-start_time).seconds > 180:
			print('timeout for index, exiting')
			quit()
		else:
			return get_index(start_time)
	else:
		file_object = open('temp/index.html', 'w')
		file_object.write(result)
		file_object.close( )

		countries = []
		countries_abbr = {}
		table = []

		def process_line(line):
			line = line.replace("<tr><td>","").replace("</td><td>",",").replace("</td>","")
			line = line.split(",")
			rank = int(line[0])
			country = line[1][line[1].find("\">")+2:line[1].find("</a>")]
			abbr = line[1][line[1].find("=\"")+2:line[1].find(".htm")]
			rating = int(line[2])
			countries.append(country)
			countries_abbr[country] = abbr
			table.append([rank,country,rating])

		date = ""

		with open("temp/index.html") as file :
			read_flag = False

			for line in file :
				if (not read_flag) and "Ratings and Statistics as of" in line:
					read_flag = True
					date = line[line.find("of")+3:].replace("</td></tr>","").replace(" ","_").replace("\n","")
				else:
					if line.startswith("<tr><td>"):
						process_line(line)
		return countries,countries_abbr,date

def download_page(country,countries_abbr,start_time):
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
	    url = 'http://www.eloratings.net/' + countries_abbr[country] + '.htm',
	    headers = headers_set[random.randint(0,len(headers_set)-1)]
	)
	try:
		result = urllib2.urlopen(req).read()
	except:
		if (datetime.datetime.now()-start_time).seconds > 180:
			print('timeout for ' + country)
			return 
		else:
			download_page(country,countries_abbr,start_time)
	else:
		file_object = open('temp/'+country+'.html', 'w')
		file_object.write(result)
		file_object.close( )

if len(sys.argv) < 3:
	#getting all matches a week from now
	start_str = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d")
	end_str = time.strftime("%Y-%m-%d")
else:
	start_str = sys.argv[1]
	end_str = sys.argv[2]

print("getting matches from "+start_str + " to "+end_str+" -- " + time.strftime("%Y-%m-%d %H:%M:%S"))

if not os.path.exists('temp'):
	os.makedirs('temp')
countries,countries_abbr,date = get_index(datetime.datetime.now())

cutoff = len(countries)
threads = []

for country in countries[0:cutoff]:
	start_time = datetime.datetime.now()
	t = threading.Thread(target=download_page,args=(country,countries_abbr,start_time,))
	threads.append(t)

for t in threads:
	t.start()

for t in threads:
	t.join()

months = ["January","February","March","April","May","June",
	"July","August","September","October","November","December"] 

def parse_date(str):
	str = str.split(" ")
	if len(str)<3:
		year = int(str[1])
		month = 1
		day = 1
	else:
		year = int(str[2])
		month = 0
		day = int(str[1])
		for i in range(12):
			if str[0] == months[i]:
				month = i+1
	return year,month,day

def in_range(date_str,start_str,end_str):
	year,month,day = parse_date(date_str)
	start_str = start_str.split("-")
	end_str = end_str.split("-")
	year_s = int(start_str[0])
	month_s = int(start_str[1])
	day_s = int(start_str[2])
	year_e = int(end_str[0])
	month_e = int(end_str[1])
	day_e = int(end_str[2])
	date = datetime.date(year,month,day)
	date_s = datetime.date(year_s,month_s,day_s)
	date_e = datetime.date(year_e,month_e,day_e)
	if date_s<=date and date_e>=date :
		return True
	else:
		return False


matches = {}
for country in countries[0:cutoff]:
	raw = []
	count = 1
	try:
		with open("temp/"+country+".html") as file :
			for line in file :
				if line.startswith("<tr class=\"nh\">"):
					line = line.replace("<br>",",").replace("<tr class=\"nh\"><td>","")\
						.replace("</td><td>",",").replace("</td></tr>\n","").split(",")
					
					if len(line)== 15:
						line.insert(0,"January 1")
					date_str = line[0]+" "+line[1]
					line.append(count)
					if in_range(date_str,start_str,end_str):
						raw.append(line)
					count +=1
		file.close();
		matches[country] = raw
	except:
		print('error reading temp/'+country+".html")
shutil.rmtree('temp') 

in_json = json.dumps(matches)
file_object = open('matches_'+end_str+'.txt', 'w')
file_object.write(in_json)
file_object.close( )

print("done -- " + time.strftime("%Y-%m-%d %H:%M:%S"))
