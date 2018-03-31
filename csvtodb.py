import sqlite3
import csv
import sys
#import urllib2
#url = u'https://stackoverflow.com/questions/6109532/what-is-the-maximum-size-limit-of-varchar-data-type-in-sqlite'
#html = urllib2.urlopen(url).read().decode('utf-8')
csv.field_size_limit(sys.maxsize)
conn = sqlite3.connect(r'C:\Users\Leo\Desktop\articles.db')
c = conn.cursor()
c.execute("create table if not exists article (url text, html text);")

with open(r'C:\Users\Leo\Desktop\articleshtml.csv') as file:
	reader = csv.reader(file)
	for line in reader:
		print "inserting url:", line[0]
		c.execute("insert into article values (?,?);",(line[0],line[1].decode('gbk','ignore')))

conn.commit()
conn.close()