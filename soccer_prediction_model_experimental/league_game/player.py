import urllib2
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}


for page in range(0,100):
	offset = page * 80
	req = urllib2.Request(
    	url = 'https://sofifa.com/players?hl=en-US&offset='+str(offset),
    	headers = headers
	)
	result = urllib2.urlopen(req).read()
	file_object = open('sofifa_'+str(offset+1)+'_to_'str(offset+80)'.html', 'w')
	file_object.write(result)
	file_object.close( )


from bs4 import BeautifulSoup

soup = BeautifulSoup(open("sofifa_index.html"),"html.parser")

players = {}

tables = soup.findAll('table', class_ = "table table-hover persist-area")  
tab = tables[0]  

for tr in tab.findAll('tr'): 
	name = ""
	#print("-------\nnext player\n-------")
	player = {}
	for td in tr.findAll('td'): 
		if td.get('id') == None:


			for img in td.findAll('img'):
				if 'players' in img.get("data-src"):
					player["img"] = img.get("data-src").encode("utf-8")
			for span in td.findAll('span'):
				if span.get("title") != None: #nationality
					player["na"] = span.get('title').encode("utf-8")
					#print(span.get("title"))
				if 'pos' in span.get('class'):
					if 'pos' not in  player.keys():
						player['pos'] = [span.getText().encode("utf-8")]
					else:
						player['pos'].append(span.getText().encode("utf-8"))
			for a in td.findAll('a'): 
				if a.get("title") != None: #full name
					player["full_name"] = a.get("title").encode("utf-8")
					player["name"] = a.getText().encode("utf-8")
					name = a.getText().encode("utf-8")
				if 'team' in a.get('href'):
					player['team'] = a.getText().encode("utf-8")
					#print(a.getText())
					#print("!????")
					#print(a.get('title'))
					#print(a.get("title"))


		#print(td)
		#print(td.getText().replace("\n",""))
		else:
			#print(td.get('id'))
			content = td.getText().replace("\n","").replace("\r","")
			player[td.get("id").encode("utf-8")] = content.encode("utf-8")  
		#if content == "":
			#continue
			#print(content)
		'''
		if name == "":
			name = td.getText()
			print(name)
			players[name] = []
		players[name].append(td.getText())
		'''
	if name != "":
		players[name] = player



print(players.keys())
print(players["Cristiano Ronaldo"])