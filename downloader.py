import urllib2
import random
import urlparse
import time
from datetime import datetime

class Downloader:
	def __init__(self, delay=0,user_agent='wswp',proxies=None,
                 num_retries=1,cache=None):
		self.throttle = Throttle(delay)
		self.user_agent = user_agent
		self.proxies = proxies
		self.num_retries = num_retries
		self.cache = cache
	def __call__(self,url):
		result = None
		if self.cache:
			try:
				result = self.cache[url]
			except KeyError:
				#url is not available in cache
				pass
			else:
				if self.num_retries > 0 and 500 <= result['code']<600:
					#server error so ignore result from cache
					#so still need to download
					result = None
		if result is None:
			#result was not loaded from cache
			#so still need to download
			self.throttle.wait(url)
			proxy = random.choice(self.proxies) if  self.proxies else None
			headers = {'User-agent':self.user_agent}
			result = self.download(url, headers,proxy,self.num_retries)
			if self.cache:
				#save result to cache
				self.cache[url] = result
		return result['html']

	def download(self, url, headers, proxy, num_retries, data=None):
		print 'Downloading:', url
		request = urllib2.Request(url, data, headers)
		opener = urllib2.build_opener()
		if proxy:
			proxy_params = {urlparse.urlparse(url).scheme: proxy}
			opener.add_handler(urllib2.ProxyHandler(proxy_params))
		try:
			response = opener.open(request)
			html = response.read()
			code = response.code
		except urllib2.URLError as e:
			print 'Download error:', e.reason
			html = ''
			if hasattr(e, 'code'):
				code = e.code
				if num_retries > 0 and 500 <= code < 600:
					# retry 5XX HTTP errors
					html = download(url, headers, proxy, num_retries-1, data)
			else:
				code = None
		return {'html':html,'code':code}

class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
        
    def wait(self, url):
        """Delay if have accessed this domain recently
        """
        domain = urlparse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()