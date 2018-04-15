import urllib2
from lxml import etree
import re
EUTILITIES_BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

def getTitle(IdList):
	idterm = ','.join(IdList)
	url = EUTILITIES_BASE + 'esummary.fcgi?db=pubmed&id=' +idterm
	xml = urllib2.urlopen(url).read()
	TitleList = re.findall(r'<Item Name="Title" Type="String">(.*?)</Item>',xml)
	return TitleList