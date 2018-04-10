import csv
from zipfile import ZipFile
from StringIO import StringIO
from urllib2 import urlopen, HTTPError, URLError

zip_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
try:
	print 'Downloading from : ',zip_url
	data = urlopen(zip_url).read()
	print 'data length is : ',len(data)
except HTTPError, e:
    print "HTTP Error:", e.code, zip_url
except URLError, e:
    print "URL Error:", e.reason, zip_url

urls = []
with ZipFile(StringIO(data)) as zf:
	csv_filename = zf.namelist()[0]
	for _, website in csv.reader(zf.open(csv_filename)):
		urls.append('http://'+website)
print 'urls length is :',len(urls)