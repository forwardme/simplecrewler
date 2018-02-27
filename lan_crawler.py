import re
import urllib2
import csv

articlelist = []
for i in range(1):
	object_url = 'http://172.20.1.12/cms/ArticleList_jdey.aspx?LMID=A&page=' + str(i+1)
	print 'crawling page '+ str(i+1)
	html = urllib2.urlopen(object_url).read()
	articlelist.extend(re.findall(r'<td.*?href="(.*?)" *title="(.*?)"',html))

print 'articlelist length is', len(articlelist)

articlelist = [list(tu) for tu in articlelist]
for article in articlelist:
	html = urllib2.urlopen('http://172.20.1.12/cms/'+article[0]).read()
	print 'crawling page ', article[0]
	art_add = re.findall(r'class="article_addition">(.*?)<',html) 
	article.extend(art_add)

print 'writing to file...'

with open ('csvfile.csv','wb') as outfile:
	thewriter = csv.writer(outfile,delimiter=',')
	for article in articlelist:
		thewriter.writerow(article)