import urllib2
import urllib

class summarywithid:
	def __init__(self):
		self.url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1;Win64; x64)'
		self.headers = {'User-Agent':self.user_agent}
	def __call__(self,database,idlist):
		self.ids = ','.join(idlist)
		self.values = {'db':database,'id':self.ids}
		self.data  = urllib.urlencode(self.values)
		self.req = urllib2.Request(self.url,self.data,self.headers)
		self.response = urllib2.urlopen(self.req)
		return self.response.read()
		
class searchwithkeywords:
	def __init__(self):
		self.url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1;Win64; x64)'
		self.headers = {'User-Agent':self.user_agent}
	def __call__(self,database,keywords):
		self.keywordterm = ' '.join(keywords)
		self.values = {'db':database,'term':self.keywordterm,'usehistory':'y'}
		self.data  = urllib.urlencode(self.values)
		self.req = urllib2.Request(self.url,self.data,self.headers)
		self.response = urllib2.urlopen(self.req)
		return self.response.read()

class fetchwithid:
	def __init__(self):
		self.url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1;Win64; x64)'
		self.headers = {'User-Agent':self.user_agent}
	def __call__(self,database,idlist):
		self.ids = ','.join(idlist)
		self.values = {'db':database,'id':self.ids,'retmode':'xml'}
		self.data  = urllib.urlencode(self.values)
		self.req = urllib2.Request(self.url,self.data,self.headers)
		self.response = urllib2.urlopen(self.req)
		return self.response.read()
