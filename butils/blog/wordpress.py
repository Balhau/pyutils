from bs4 import BeautifulSoup
from ebooklib import epub
from epubutil import *
import sys
import urllib2


BLOG_HOST='https://blog.balhau.net/'
EBOOK_NAME="Gamma Dreams Book"


class Wordpress:

    def __init__(self,blogHost,ebookName,language='en',authors=['Author Name']):
        self.bloghost=blogHost
        self.ebookName=ebookName
        self.language=language
        self.authors=authors
        self.spine=['nav']

    def getDoc(self,pageNum):
        try:
            pageUrl='{}?paged={}'.format(self.bloghost,str(pageNum))
            page=urllib2.urlopen(pageUrl)
            return BeautifulSoup(page, 'html.parser')
        except:
            return []

    def checkIfIsValidPage(self,soupObject):
        try:
            len(soupObject.find_all("article"))
            return True
        except:
            return False

    def toEpub(self,path):
        ebook=createEbook(self.ebookName,self.ebookName,self.language,self.authors)
        UNTITLED=1
        pages=[]

        pageNum=1
        soupObject=self.getDoc(pageNum)

        #print "Extracting data from blog"
        while self.checkIfIsValidPage(soupObject):
            pages.append(soupObject.find_all('article'))
            pageNum+=1
            soupObject=self.getDoc(pageNum)


        #print "Converting into epub"
        for page in reversed(pages):
            #Flatten article
            for article in reversed(page):
                #Parse data if article valid
                if article != None:
                    title=article.header.h1.get_text()
                    if title == None or title.strip() == '':
                        title = "Entry: "+str(UNTITLED)
                        UNTITLED+=1
                    title=title.strip()
                    #sys.stdout.flush()
                    content=str(article).decode('utf-8')
                    addEntry(ebook,title,self.language,content,self.spine)

        addStyle(ebook,self.spine)

        #Write the epub
        outputPath=self.ebookName+".epub"
        if path != None:
            outputPath=path
        epub.write_epub(outputPath,ebook,{})




def parseArticles(articles):
    return 1
    #Build ebook entries here

#Function to create ebook headers
def createEbook(idEbook,ebookTitle,lang,authors):

    book = epub.EpubBook()
    book.set_identifier(idEbook)
    book.set_title(ebookTitle)
    book.set_language(lang)

    for author in authors:
        book.add_author(author)

    return book


#articles=doc.find_all("article")

#Title
#print articles[0].header.h1.a.string
#Post
#print articles[0].find_all('div')[1].get_text()

'''
ebook=createEbook("gammaDreamsBook",'Gamma Dreams Blog','pt',['Balhau'])

spine=['nav']

##Main loop where we exctract all post info and create ebook entries

#dataPublished = entry['published']['$t']

UNTITLED=1
pages=[]

pageNum=1
soupObject=getDoc(pageNum)

print "Extracting data from blog"
while checkIfIsValidPage(soupObject):
    pages.append(soupObject.find_all('article'))
    pageNum+=1
    soupObject=getDoc(pageNum)


print "Converting into epub"
for page in reversed(pages):
    #Flatten article
    for article in reversed(page):
        #Parse data if article valid
        if article != None:
            title=article.header.h1.get_text()
            if title == None or title.strip() == '':
                title = "Entry: "+str(UNTITLED)
                UNTITLED+=1
            title=title.strip()
            sys.stdout.flush()
            content=str(article).decode('utf-8')
            c1 = epub.EpubHtml(title=title, file_name=title+'.xhtml', lang='pt')
            c1.content=content
            ebook.add_item(c1)
            ebook.toc = ebook.toc + [epub.Link(title+'.xhtml', title, title)]
            spine.append(c1)

ebook.add_item(epub.EpubNcx())
ebook.add_item(epub.EpubNav())
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
# add CSS file
ebook.add_item(nav_css)
# basic spine
ebook.spine = spine
# write to the file
epub.write_epub(EBOOK_NAME+'.epub', ebook, {})

#articles=doc.find_all("article")
#for article in articles:
'''
