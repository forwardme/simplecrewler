import mechanize
from urlparse import urlparse
import lxml.html
from lxml import etree
import re
login_url = 'https://www.safaribooksonline.com/accounts/login/'
base_url = 'https://www.safaribooksonline.com/library/view/data-visualization-with/9781491920565/'

def getlinks():
	booklinks = []
	booklinks.append(base_url + "preface01.html")
	booklinks.append(base_url + "preface02.html")
	for i in range(21):
		booklinks.append(base_url + "ch%02d.html"%(i+1))
	for i in range(5):
		booklinks.append(base_url + "part%02d.html"%(i+1))
	booklinks.append(base_url + "app01.html")	
	return booklinks

def login(br):
	response = br.open(login_url)
	assert br.viewing_html()
	print 'login page: ', response.geturl()
	br.select_form(nr=0)
	br['email'] = 'forwardme@163.com'
	br['password1']= 'gaoyuan123'
	br.submit()
	
def downloading():
	booklinks = getlinks()
	figurelinks = set()

	for link in booklinks:
		name = urlparse(link).path
		name = name.split('/')[-1]
		with open(name,'wb') as dfile:
			print 'downloading page:',link
			html = br.open(link).get_data()
			tree = lxml.html.fromstring(html)
			figures = tree.xpath(r'//*[@id="sbo-rt-content"]//img')
			for fig in figures:
				figlink = fig.attrib.get('src')
				figname = figlink.split('/')[-1]
				figurelinks.add(figlink)
				html = re.sub(figlink,figname,html)
			dfile.write(html)
	return figurelinks
	
def downloadfigs(figurelinks):
	for fig in figurelinks:
		print 'downloading figure:',fig
		name = fig.split('/')[-1]
		fd = br.open(fig).get_data()
		with open(name,'wb') as ff:
			ff.write(fd)
	
	
	
if __name__ == "__main__":	
	br = mechanize.Browser()
	br.set_handle_robots(False)
	login(br)
	figs = downloading()
	downloadfigs(figs)
	br.close()
