import lxml.html
import csv
import sys
#修改csv field大小限制
csv.field_size_limit(sys.maxsize)
source_file = r'D:\SoftwareBackup2017-5-10\articleshtml.csv'
object_file = r'D:\SoftwareBackup2017-5-10\document.csv'
selector = '#mainbodyininfo > div:nth-child(3)'
html_list = []
#从html源文件获取文章内容（GBK编码需转换）
def get_article_content(html):
	html_gbk = html.decode('gbk','ignore')
	tree = lxml.html.fromstring(html_gbk)
	doc_element = tree.cssselect(selector)[0]
	return doc_element.text_content().encode('gbk','ignore')

with open(source_file,'rb') as file:
	reader = csv.reader(file)
	print 'reading source data:'
	for row in reader:
		html_list.append(row)
#缩短写入文件时间，减小文件大小
html_list = html_list[-10:]
with open(object_file,'wb') as file:
	writer = csv.writer(file,delimiter=',')
	print 'writing to file:'
	for item in html_list:
		item[1] = get_article_content(item[1])
		writer.writerow(item)






