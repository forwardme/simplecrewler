from urllib2 import urlopen
import csv
from lxml import etree

search_term = 'lung+recruitment+lung+(ultrasound+OR+ultrosonic)+(ARDS+OR+(acute+respiratory+distress+syndrome))'
search_query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s&usehistory=y'%search_term
search_result = urlopen(search_query).read()
resulttree = etree.fromstring(search_result)
print 'get %s articles.'%resulttree.xpath(r'//Count')[0].text
querykey = resulttree.xpath(r'//QueryKey')[0].text
webenv = resulttree.xpath(r'//WebEnv')[0].text
print 'downloading summary results...'
summary_query = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&query_key=%s&WebEnv=%s'%(querykey,webenv)
summary_result = urlopen(summary_query).read()
summarytree = etree.fromstring(summary_result)
itemname = ['PMID']
itemname += summarytree.xpath(r'//DocSum[1]/Item/@Name')

DocSum_objs = summarytree.xpath(r'//DocSum')
print 'saving result to file...'
with open(r'download.csv','wb') as file:
	csvwriter = csv.writer(file,delimiter=',')
	csvwriter.writerow(itemname)
	for doc in DocSum_objs:
		text_content_list = [doc.xpath(r'./Id')[0].text]
		items = [item for item in doc.xpath(r'./Item')]
		text_content_list += [''.join(x.itertext()) for x in items]
		print 'downloading abstract of PMID: ',text_content_list[0]
		abstract_xml = urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%s&retmode=xml'%text_content_list[0]).read()
		abstract_tag = etree.fromstring(abstract_xml).xpath(r'//Abstract')
		if abstract_tag:
			sub_ab_tag = abstract_tag[0].xpath(r'./AbstractText')
			abstract = ''
			for sub in sub_ab_tag:
				if sub.attrib:
					abstract += sub.attrib['Label'] + sub.text
				else:
					abstract += sub.text
			text_content_list.append(abstract)
		csvwriter.writerow([s.encode('utf-8','ignore') for s in text_content_list])
print 'Done!'