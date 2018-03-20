import urllib2
from threading import Thread
import csv
with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articlelist.txt','rb') as handle:
	list = handle.read().split('\n')[:-1]
	
list = list[:50]
article_dict = {}


def get_html(url):
	try:
		print 'downloading ',url
		html = urllib2.urlopen(url).read()
	except URLError as e:
		print 'URLError:',e
		html = None
	finally:
		article_dict[url] = html

class Mythread(Thread):
	def __init__(self,url):
		Thread.__init__(self)
		self.url = url
	def run(self):
		get_html(self.url)

while len(list)>0:
	threads = []
	num_thread = 5 if len(list)>5 else len(list)
	for i in range(num_thread):
		art_thead = Mythread(list.pop())
		art_thead.start()
		threads.append(art_thead)
	for i in range(num_thread):
		threads[i].join()
	
print 'Finished downloading htmls,\nWriting to File.'

with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articleshtml.csv','wb') as handle:
	csv_writer = csv.writer(handle, delimiter = ',')
	for item in article_dict:
		csv_writer.writerow([item,article_dict[item]])