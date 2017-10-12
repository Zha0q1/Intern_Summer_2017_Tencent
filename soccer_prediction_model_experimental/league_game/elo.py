import urllib2
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
req = urllib2.Request(
    url = 'http://www.eloratings.net/world.html',
    headers = headers
)
result = urllib2.urlopen(req).read()
file_object = open('index.html', 'w')
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

with open("index.html") as file :
	read_flag = False

	for line in file :
		if (not read_flag) and "Ratings and Statistics as of" in line:
			read_flag = True
			date = line[line.find("of")+3:].replace("</td></tr>","").replace(" ","_").replace("\n","")
		else:
			if line.startswith("<tr><td>"):
				process_line(line)

import json

in_json = json.dumps(countries)
file_object = open('contries.txt', 'w')
file_object.write(in_json)
file_object.close()

in_json = json.dumps(countries_abbr)
file_object = open('contries_abbr.txt', 'w')
file_object.write(in_json)
file_object.close()

in_json = json.dumps(table)
file_object = open('table_'+date+'.txt', 'w')
file_object.write(in_json)
file_object.close()










cutoff = 20

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
for country in countries[0:cutoff]:
	print("processing "+country)
	req = urllib2.Request(
		url = 'http://www.eloratings.net/' + countries_abbr[country] + '.htm',
		headers = headers
	)
	result = urllib2.urlopen(req).read()
	file_object = open(country+'.html', 'w')
	file_object.write(result)
	file_object.close( )

matches = {}
for country in countries[0:cutoff]:
	raw = []
	with open(country+".html") as file :
		for line in file :
			if line.startswith("<tr class=\"nh\">"):

				raw.append(line.replace("<br>",",").replace("<tr class=\"nh\"><td>","")\
					.replace("</td><td>",",").replace("</td></tr>\n","").split(","))
	file.close();
	matches[country] = raw



in_json = json.dumps(matches)
file_object = open('matches_'+date+'.txt', 'w')
file_object.write(in_json)
file_object.close( )