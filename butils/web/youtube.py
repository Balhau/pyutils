#Script to extract youtube video urls
import urllib2
from bs4 import BeautifulSoup
import json
import urllib

response=urllib2.urlopen("https://www.youtube.com/watch?v=oTXa6FFnPI0")
html=response.read()

soup=BeautifulSoup(html,from_encoding="utf-8")


scriptData=soup.find_all('script')[9]
text=scriptData.get_text()


START_PATTERN='ytplayer.config ='
END_PATTERN='ytplayer.load'

START_OFFSET=text.index(START_PATTERN)
END_OFFSET=text.index(END_PATTERN)

jsonv=text[START_OFFSET+len(START_PATTERN):END_OFFSET-1]

jsonv=jsonv.encode('utf-8')

#print jsonv

jsono=json.loads(jsonv)

data=urllib.unquote_plus(jsono["args"]['adaptive_fmts'])

#print data;

toks=[token for token in data.split("&")]

for k in toks:
    print k

i=0;
