import json
from ebooklib import epub
import urllib2
from epubutil import *

'''
Class to extract blog information from blogspot platform
'''
class Blogspot():

    BLOGGER_URL='http://{}.blogspot.com/feeds/posts/default?alt=json&callback=mycallbackfunc&start-index=1&max-results=500'

    def __init__(self,blogname,language,authors):
        self.ebook=createEbook(blogname,blogname,language,authors)
        self.language=language;
        self.url=self.BLOGGER_URL.format(blogname)
        self.title=blogname
        self.spine=['nav']

    def _getBloggerData(self):
        httpdata = urllib2.urlopen(self.url)
        jsonCallback = httpdata.read()


        #Extract the callBack declaration
        jsonData=jsonCallback[31:]
        #Extract the final 2 chars that represent ");" for the enclosing of the callback
        jsonData=jsonData[:-2]


        #Now parse the data into json object
        blogData=json.loads(jsonData)
        self.entries = blogData['feed']['entry']

    def _processEntries(self,entries,spine):
        for entry in reversed(self.entries):
            name=entry['author'][0]['name']['$t']
            dataPublished = entry['published']['$t']
            title=entry['title']['$t']
            header='<h1>'+title+'</h1>'+'<h4>'+dataPublished.split("T")[0]+'</h4>'
            content=header+entry['content']['$t']
            addEntry(self.ebook,title,self.language,content,spine)

    def toEpub(self,path):
        outputPath=self.title+".epub"
        spine=['nav']
        self._getBloggerData()
        self._processEntries(self.entries,self.spine)
        addStyle(self.ebook,self.spine)
        if path != None:
            outputPath=path
        epub.write_epub(outputPath,self.ebook,{})
