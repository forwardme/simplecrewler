import urllib2
import csv
from threading import Thread

with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articlelist.txt','rb') as handle:
	list = handle.read().split('\n')[:-1]

html_dict = {}

class fetchhtml:
	def __init__(self,url):
		self.url = url
	def get_html(self):
		try:
			print 'downloading ',self.url
			self.html = urllib2.urlopen(self.url).read()
		except URLError as self.e:
			print 'URLError:',self.e
			self.html = None
		finally:
			return self.html

def mainloop(list):
	while list:
		url = list.pop()
		fetch = fetchhtml(url)
		html_dict[url] = fetch.get_html()

class Mythread(Thread):
	def __init__(self,list):
		Thread.__init__(self)
		self.list = list
	def run(self):
		mainloop(self.list)
threadlist = []
num_threads = 5
for i in range(num_threads):
	athread = Mythread(list)
	athread.start()
	threadlist.append(athread)

for i in range(num_threads):
	threadlist[i].join()

print 'finished fetch htmls, get %d items.'%(len(html_dict.keys()))
print 'writing to articleshtml.csv'
with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articleshtml.csv','wb') as handle:
	thewriter = csv.writer(handle,delimiter=',')
	for item in html_dict.items():
		thewriter.writerow(item)
	
	