import re
import urllib2
import urlparse
import csv
import lxml.html

def download(url,user_agent='wcwp',num_retries = 2):
	print 'Downloading:',url
	headers = {'User-agent':user_agent}
	request = urllib2.Request(url, headers = headers)
	try:
		html = urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print 'Download error:', e.reason,'\ne.code:',e.code
		html = None
		if num_retries > 0:
			if hasattr(e,'code') and 500 <= e.code < 600:
				#recursively retry 5XX HTTP errors
				return download(url, num_retries-1)
	return html
	
def crawl_sitemap(url):
	#download the sitemap file
	sitemap = download(url)
	#print sitemap
	#extract the sitemap links
	links = re.findall('<td(.*?)<a[^>]+href=["\'](.*?)["\']', sitemap)
	#download each link
	for link in links:
		link = urlparse.urljoin(url,link[1])
		html = download(link)
		#scrape html here
		
def link_crawler(seed_url, link_regex, max_depth=2, scrape_callback=None):
	'''Crawl from the given seed URL following links matched by link_regex'''
	crawl_queue = [seed_url]
	#keep track which URL's have seen before
	seen = {seed_url:0}
	while crawl_queue:
		url = crawl_queue.pop()
		depth = seen[url]
		#not go further than max_depth layers of links
		if depth < max_depth:
			html = download(url)
			if scrape_callback:
				scrape_callback(url,html)
			#filter for links matching our regular expression
			for link in get_links(html):
				if re.search(link_regex, link[1]):
					link = urlparse.urljoin(seed_url,link[1])
					if link not in seen:
						seen[link] = depth + 1
						crawl_queue.append(link)
		else:
			print 'link: %.20s' %url[51:],' is deeper than max_depth, abort.'

def get_links(html):
	'''Return a list of links from html'''
	#a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<td(.*?)<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	#list of all links from the webpage
	return webpage_regex.findall(html)

def test_function(url,func,link_regex):
	links = func(download(url))
	print links
	for link in links:
		if re.match(link_regex,link):
			print link,'get matched with',link_regex
		else:
			print link,'not match with',link_regex

class Throttle:
	"""Add a delay between downloads to the same domain"""
	def __init__(self, delay):
		#amount of delay between downloads for each domain
		self.delay = delay
		#timestamp of when a domain was last accessed
		self.domains = {}
		
	def wait(self, url):
		domain = urlparse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				#domain has been accessed recently
				#so need to sleep
				time.sleep(sleep_secs)
		#update the last accessed time
		self.domains[domain] = datetime.datetime.now()	

class ScrapeCallback:
	def __init__(self):
		self.writer = csv.writer(open('countries.csv','w+'))
		self.fields = ['area','population','iso','country','capital',
		               'continent','tld','currency_code','currency_name',
		               'phone','postal_code_format','postal_code_regex',
		               'languages','neighbours']
		self.writer.writerow(self.fields)
		
	def __call__(self, url, html):
		if re.search('/view/',url):
			tree = lxml.html.fromstring(html)
			row = []
			for field in self.fields:
				row.append(tree.cssselect('table>tr#places_{}__row>td.w2p_fw'.format(field))[0].text_content())
			self.writer.writerow(row)
				
		
if __name__ == '__main__':
	#test_function('http://example.webscraping.com',get_links,'/(index|view)')
	link_crawler('http://example.webscraping.com','/view/',scrape_callback = ScrapeCallback())
	#crawl_sitemap('http://example.webscraping.com')
	