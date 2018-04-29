import re
import urllib2
import lxml.html

base_url='https://www.safaribooksonline.com/library/view/data-visualization-with/9781491920565/'
url_list = []
for i in range(21):
	url_list.append(base_url+'ch{:02}.html'.format(i+1))

def getdoc(url):
	print 'downloading doc from: ',url
	html = urllib2.urlopen(url).read()
	page = lxml.html.fromstring(html)
	doc = page.xpath(r'//div[@id="sbo-rt-content"]')[0].text_content()
	return doc

with open('bookdownloaded.txt','wb') as file:
	for url in url_list:
		file.writelines(getdoc(url))
print 'Done.'