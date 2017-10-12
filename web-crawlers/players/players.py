import urllib2
import random
import os,signal,sys
import threading
import json
import shutil  
import time
import datetime

def get_and_parse_page(page,start_time):
	offset = page * 80
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

	print("processing offset "+str(offset))
	req = urllib2.Request(
    	url = 'https://sofifa.com/players?hl=en-US&offset='+str(offset),
    	headers = headers_set[random.randint(0,len(headers_set)-1)]
	)
	try:
		result = urllib2.urlopen(req).read()
	except:
		if (datetime.datetime.now()-start_time).seconds > 180:
			print('timeout for offset '+str(offset)+', skiping it')
			sem.release()
			return
		else:
			print('redownloading '+str(offset))
			get_and_parse_page(page,start_time)
			return
	else:
		
		file_name = 'temp/sofifa_'+str(offset+1)+'_to_'+str(offset+80)+'.html'
		file_object = open(file_name, 'w')
		file_object.write(result)
		file_object.close( )

		from bs4 import BeautifulSoup

		soup = BeautifulSoup(open(file_name),"html.parser")

		players = {}
		players_rank = {}
		players_id = {}

		tables = soup.findAll('table', class_ = "table table-hover persist-area")  
		tab = tables[0] 

		rank = offset

		for tr in tab.findAll('tr'): 
			name = ""
			sofifa_id = ''
			#print("-------\nnext player\n-------")
			player = {}
			for td in tr.findAll('td'): 
				if td.get('id') == None:


					for img in td.findAll('img'):
						if 'players' in img.get("data-src"):
							player['sofifa_id'] = img.get("id").encode("utf-8")
							player["img"] = img.get("data-src").encode("utf-8")
							sofifa_id = img.get("id").encode("utf-8")
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
					for div in td.findAll('div'):
						if div.get("class") == [u'subtitle', u'text-clip', u'rtl']:
							player['contract'] = div.getText()



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
				rank += 1
				player["rank"] = rank
				players_rank[rank] = player
				players[name] = player
				players_id[sofifa_id] = player

		'''
		in_json = json.dumps(players)
		file_object = open('temp/players_'+str(offset+1)+'_to_'+str(offset+80)+'.txt', 'w')
		file_object.write(in_json)
		file_object.close()

		in_json = json.dumps(players_rank)
		file_object = open('temp/players_rank_'+str(offset+1)+'_to_'+str(offset+80)+'.txt', 'w')
		file_object.write(in_json)
		file_object.close()
		'''
		in_json = json.dumps(players_id)
		file_object = open('temp/players_rank_'+str(offset+1)+'_to_'+str(offset+80)+'.txt', 'w')
		file_object.write(in_json)
		file_object.close()

		print("finished processing offset "+str(offset))
		sem.release()

class Watcher():  

	def __init__(self):  
		self.child = os.fork()  
		if self.child == 0:  
			return  
		else:  
			self.watch()  
  
	def watch(self):  
		try:  
			os.wait()  
		except KeyboardInterrupt:  
			self.kill()  
		sys.exit()  
  
	def kill(self):  
		try:  
			os.kill(self.child, signal.SIGKILL)  
		except OSError:  
			pass 

print("getting players info -- " + time.strftime("%Y-%m-%d %H:%M:%S"))

maxThread=10

Watcher() 

sem=threading.BoundedSemaphore(maxThread)

if not os.path.exists('temp'):
	os.makedirs('temp')


for page in range(250):
	sem.acquire()
	start_time = datetime.datetime.now()
	t = threading.Thread(target=get_and_parse_page,args=(page,start_time,))  
	t.start()
    
for a in range(maxThread):
	print("a: "+str(a))
	sem.acquire()


print("merging the files")

all_players = {}
for page in range(250):
	offset = page * 80
	try:
		f = open('temp/players_rank_'+str(offset+1)+'_to_'+str(offset+80)+'.txt') 
	except:
		print('file does not exist, offset ' + str(offset))
	else:
		players = json.load(f)
		all_players = dict(all_players, **players)

shutil.rmtree('temp') 

in_json = json.dumps(all_players)
file_object = open('all_players.txt', 'w')
file_object.write(in_json)
file_object.close()

print('players count:' + str(len(all_players)))

print("done -- " + time.strftime("%Y-%m-%d %H:%M:%S"))
