import re
import urllib2
import urllib
import cookielib
import lxml.html

base_url='https://www.safaribooksonline.com/library/view/data-visualization-with/9781491920565/'
url_list = []

for i in range(21):
	url_list.append(base_url+'ch{:02}.html'.format(i+1))

def getcookies(signin_url):
	data = {"username":"forwardme@126.com","password":"gaoyuan123"}
	data = urllib.urlencode(data)
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(signin_url,data)
	return (cookie,response)
	
def getdoc(url):
	print 'downloading doc with post data from: ',url
	data = {"username":"forwardme@126.com","password":"gaoyuan123"}
	data = urllib.urlencode(data)
	request = urllib2.Request(url, data)
	html = urllib2.urlopen(request).read()
	page = lxml.html.fromstring(html)
	doc = page.xpath(r'//div[@id="sbo-rt-content"]')[0].text_content()
	return doc
	
def run():
	with open('bookdownloaded.txt','wb') as file:
		for url in url_list:
			file.writelines(getdoc(url))
	print 'Done.'
	
if __name__ == "__main__":
	run()