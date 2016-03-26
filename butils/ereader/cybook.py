import sqlite3
import os
import xml.etree.ElementTree as ET
#from greads import *
from goodreads import *
import csv

API_KEY="cf2Z3socJtT9qnlbjxTNw"
API_SECRET="1pSjMkE3tgrHmXdfT3wgpk7vFdYUsdU19t4NoyBg1BA"

OAUTH_TOKEN="1nApzFhQPdb9gFox9llDKw"
OAUTH_SECRET="bP8k8IK0kHRnqOlVXQKWa4xzvDqBvv7FhO4Pq5m3DI"

class Annotation:

    def __init__(self,date,book,body):
        self.book=book
        self.body=body
        self.date=date

'''
    This is a class for the cybook odissey info scrapping
'''
class Odissey():

    system_folder = "system"
    annotation_folder = "Annotations"
    path = None
    library = None
    annotations = None
    conn = None

    def __init__(self,path):
        self.path=path
        self.library = "%s/%s/library" % (self.path,self.system_folder)
        self.annotations = "%s/%s" % (self.path,self.annotation_folder)
        self.conn = sqlite3.connect(self.library)

    def _getExisting(self,csv_existing):
        existing=[]
        with open(csv_existing,'rb') as quotes_file:
            quotes_reader = csv.reader(quotes_file,delimiter=',')
            for quote in quotes_reader:
                existing.append(quote[4])
        return existing;

    def _getAnnotationsBook(self,path,an):
        at = ET.parse(path)
        root = at.getroot()
        book = path.split("/")[-1].split(".")[0].split(".")[0].split(":")[0].split("-")[0]
        a=[]
        for c in root:
            if len(c) == 4 and len(c[2][0]):
                a.append(Annotation(c[0].text,book,c[2][0][0].text))
        return an.append(a)

    def _getAllAnnotations(self):
        anotations=[]
        dirs = os.walk(self.annotations)
        bookAnnotations = []
        for d in dirs:
            if len(d[2]) != 0:
                self._getAnnotationsBook(d[0]+"/"+d[2][0],bookAnnotations)
        return bookAnnotations

    def uploadAnnotations(self,csv_existing):
        existing=self._getExisting(csv_existing)
        c = self.conn.cursor()
        bookAnnotations = self._getAllAnnotations()
        anot = 0

        for banno in bookAnnotations:
            gc=GoodreadsClient(API_KEY,API_SECRET,OAUTH_TOKEN,OAUTH_SECRET)
            author=""
            if len(banno) != 0:
                books=gc.findBook(banno[0].book,'1')
                for a in banno:
                    #print a.book, "+++++" ,a.body
                    if len(books) > 0 and books[1]['GoodreadsResponse']['search']['results'] != None:
                        try:
                            bk=books[1]['GoodreadsResponse']['search']['results']['work'][0]['best_book']
                            idBook=bk['id']['#text']
                            author=bk['author']['name']
                            qbody=a.body.strip().replace("/"," /")
                            #print a.book,"-----", idBook, "-----", author, "----", a.body
                            if qbody not in existing:
                                anot+=1
                                gc.addQuote(author,idBook,qbody)
                        except:
                            s=1
                            #print a.book,"-----","Error"
                    else:
                        print "Not found: ","?????????????????",a.book
        print "ANOT: ",anot


cardPath = '/home/vitorfernandes/Documents/ereader/card'

cb=Odissey(cardPath)
cb.uploadAnnotations('quotes.csv')

'''
db = '/home/vitorfernandes/Documents/ereader/card/system/library'
annotation = '/home/vitorfernandes/Documents/ereader/card/Annotations/Baron-Cohen, Simon/Science of Evil_ On Empathy and the Origins of Cruelty, The - Simon Baron-Cohen.epub.annot'

conn = sqlite3.connect(db)

c=conn.cursor()

query='PRAGMA table_info(T_ITEM);'
query2="SELECT name FROM sqlite_master WHERE type='table';"

c.execute(query)

tables = c.fetchall()

#for t in tables:
#    print t

at = ET.parse(annotation)
root = at.getroot()

#print root.tag

def getAnnotations(path,an):
    at = ET.parse(path)
    root = at.getroot()
    book = path.split("/")[-1].split(".")[0].split(".")[0].split(":")[0].split("-")[0]
    print book
    a=[]
    for c in root:
        if len(c) == 4 and len(c[2][0]):
            a.append(Annotation(c[0].text,book,c[2][0][0].text))
    return an.append(a)

anotdir = '/home/vitorfernandes/Documents/ereader/card/Annotations/'

dirs = os.walk(anotdir)
bookAnnotations = []

for d in dirs:
    if len(d[2]) != 0:
        #print d[0]+"/"+d[2][0]
        getAnnotations(d[0]+"/"+d[2][0],bookAnnotations)

print len(bookAnnotations)





Add annotation found in books!

for banno in bookAnnotations:
    author=""
    if len(banno) != 0:
        books=gc.findBook(banno[0].book,'1')
        for a in banno:
            #print a.book, "+++++" ,a.body
            if len(books) > 0 and books[1]['GoodreadsResponse']['search']['results'] != None:
                try:
                    bk=books[1]['GoodreadsResponse']['search']['results']['work'][0]['best_book']
                    idBook=bk['id']['#text']
                    author=bk['author']['name']
                    #print a.book,"-----", idBook, "-----", author, "----", a.body
                    #gc.addQuote(author,idBook,a.body)
                except:
                    s=1
                    #print a.book,"-----","Error"
            else:
                print "Not found: ","?????????????????",a.book
'''
