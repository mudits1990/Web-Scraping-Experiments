from BeautifulSoup import BeautifulSoup
import urllib2
import re
import json
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
#Ask for movie title
title = raw_input("Please enter a movie title: ")
#Ask for which year
year = raw_input("which year? ")
#Search for spaces in the title string
raw_string = re.compile(r' ')
#Replace spaces with a plus sign
searchstring = raw_string.sub('+', title)
#Prints the search string
print searchstring
#The actual query
url = "http://www.imdbapi.com/?t=" + searchstring + "&y="+year
request = urllib2.Request(url)
response = json.load(urllib2.urlopen(request))
searchstring = raw_string.sub('_',title)
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
try :
    infile = opener.open('http://en.wikipedia.org/w/index.php?title='+ searchstring + '_(film)'+'&printable=yes')
    page = infile.read()
    soup = BeautifulSoup(page)
    header = soup.h2
    result = header.findAllPrevious("p")
    for i in xrange(0,len(result)):
        print strip_tags(result[len(result)-i-1].__str__())
except urllib2.HTTPError,e :
    infile = opener.open('http://en.wikipedia.org/w/index.php?title='+ searchstring +'&printable=yes')
    page = infile.read()
    soup = BeautifulSoup(page)
    header = soup.h2
    result = header.findAllPrevious("p")
    for i in xrange(0,len(result)):
        print strip_tags(result[len(result)-i-1].__str__())
print json.dumps(response,indent=2)
