import re
import urllib2
import urlparse

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
	links = re.findall('<a[^>]+href=["\'](.*?)["\']', sitemap)
	#download each link
	for link in links:
		link = urlparse.urljoin(url,link)
		html = download(link)
		#scrape html here
		
def link_crawler(seed_url, link_regex):
	'''Crawl from the given seed URL following links matched by link_regex'''
	crawl_queue = [seed_url]
	#keep track which URL's have seen before
	seen = set(crawl_queue)
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url)
		#filter for links matching our regular expression
		for link in get_links(html):
			if re.search(link_regex, link):
				link = urlparse.urljoin(seed_url,link)
				if link not in seen:
					seen.add(link)
					crawl_queue.append(link)

def get_links(html):
	'''Return a list of links from html'''
	#a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
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
	
		
if __name__ == '__main__':
	#test_function('http://example.webscraping.com',get_links,'/(index|view)')
	link_crawler('http://example.webscraping.com','/view')
	#crawl_sitemap('http://example.webscraping.com')
	