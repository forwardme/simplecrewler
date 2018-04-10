from urllib2 import urlopen, HTTPError, URLError

def dlfile(url):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open('top_1m.csv.zip', "wb+") as local_file:
            local_file.write(f.read())
            readfile(local_file)

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url

    except URLError, e:
        print "URL Error:", e.reason, url


def readfile(file):
		for i in range(10):
			print file.readline()


if __name__ == '__main__':
    dlfile('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
