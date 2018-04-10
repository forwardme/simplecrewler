from urllib2 import urlopen
import csv
from lxml import etree

search_term = 'science%5bjournal%5d+AND+breast+cancer'
search_query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s&usehistory=y'%search_term
search_result = urlopen(search_query).read()
resulttree = etree.fromstring(search_result)
print 'get %s articles.'%resulttree.xpath(r'//Count')[0].text
querykey = resulttree.xpath(r'//QueryKey')[0].text
webenv = resulttree.xpath(r'//WebEnv')[0].text
summary_query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&query_key=%s&WebEnv=%s'%(querykey,webenv)
summary_result = urlopen(summary_query).read()
summarytree = etree.fromstring(summary_result)
itemname = summarytree.xpath(r'//DocSum[1]/Item/@Name')
DocSum_objs = summarytree.xpath(r'//DocSum')
print 'saving result to file...'
with open(r'C:\Users\Leo\Desktop\download.csv','wb') as file:
	csvwriter = csv.writer(file,delimiter=',')
	csvwriter.writerow(itemname)
	for doc in DocSum_objs:
		items = [item for item in doc.xpath(r'./Item')]
		text_content_list = [''.join(x.itertext()) for x in items]
		csvwriter.writerow([unicode(s).encode('utf-8') for s in text_content_list])
print 'Done!'