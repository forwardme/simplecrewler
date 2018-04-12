import time
import re
import urllib2
from threading import Thread
import csv

articlelist = []

def get_links(url):
	urllist = []
	try:
		print 'get links in URL: ',url
		html = urllib2.urlopen(url).read()
	except HTTPError as e:
		print 'HTTPError: ',e
	except URLError as e:
		print 'URLError: ',e
	urllist.extend(re.findall(r'<td.*?href="(.*?)"',html))
	return ['http://172.20.1.12/cms/'+lk for lk in urllist]

class MyThread(Thread):
	def __init__(self,url):
		Thread.__init__(self)
		self.url = url
	def run(self):
		#print 'start threading: ',self.name
		self.result = get_links(self.url)
	def get_result(self):
		return self.result

object_url_list = []
for i in range(324):
	object_url_list.append('http://172.20.1.12/cms/ArticleList_jdey.aspx?LMID=A&page='+str(i+1))
start_time = time.time()
while len(object_url_list)>0:
	threads = []
	if len(object_url_list) >5:
		numtry = 5
	else:
		numtry = len(object_url_list)
	for i in range(numtry):
		threads.append(MyThread(object_url_list.pop()))
	for i in range(numtry):
		threads[i].start()
	for i in range(numtry):
		threads[i].join()
	for i in range(numtry):
		#print threads[i].name,' has links: ',threads[i].get_result()
		articlelist.extend(threads[i].get_result())
end_time = time.time()

print 'time cost: ',str(end_time-start_time)
print 'get articles: ',len(articlelist)

with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articlelist.txt','wb') as handle:
	for art in articlelist:
		handle.write(art+'\n')
print 'write to file'	




