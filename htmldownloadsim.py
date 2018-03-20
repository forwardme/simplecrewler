import urllib2
import csv
with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articlelist.txt','rb') as handle:
	list = handle.read().split('\n')[:-1]



def get_html(url):
	try:
		print 'downloading ',url
		html = urllib2.urlopen(url).read()
	except URLError as e:
		print 'URLError:',e
		html = None
	finally:
		return html

with open(r'D:\SoftwareBackup2017-5-10\simplecrewler\articleshtml.csv','wb') as handle:
	thewriter = csv.writer(handle,delimiter=',')
	for url in list:
		thewriter.writerow((url,get_html(url)))
	
	