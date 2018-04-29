import re
import urllib2
import lxml.html

url='https://www.safaribooksonline.com/library/view/data-visualization-with/9781491920565/ch09.html'
print 'downloading html'
html = urllib2.urlopen(url).read()
page = lxml.html.fromstring(html)
doc = page.xpath(r'//div[@id="sbo-rt-content"]')[0]
print 'fetch docs and saving'
with open('bookdownloaded.txt','wb') as file:
	file.writelines(doc.text_content())
print 'Done.'