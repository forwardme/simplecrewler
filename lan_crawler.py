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
	article[0] = 'http://172.20.1.12/cms/'+article[0]
	html = urllib2.urlopen(article[0]).read()
	html_gbk = html.decode('gbk')
	print 'crawling page ', article[0]
	art_add = re.findall(r'class="article_addition">(.*?)<',html) 
	article.extend(art_add)
	art_ch_list = re.findall(ur'[\u4300-\u9fa5]+',html_gbk)
	art_main = ""
	for art_ch in art_ch_list:
		art_main += art_ch
	article.append(art_main.encode('gbk'))

print 'writing to file...'

with open ('csvfile.csv','wb') as outfile:
	thewriter = csv.writer(outfile,delimiter=',')
	for article in articlelist:
		thewriter.writerow(article)