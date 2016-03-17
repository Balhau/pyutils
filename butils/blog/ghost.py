from ebooklib import epub
import sqlite3
from time import gmtime, strftime
from epubutil import *



'''
Structure for author information
'''
class Author():
    authorId=None
    name=None
    email=None

    def __init__(self,a_id,name,email):
        self.authorId=a_id
        self.name=name
        self.email=email


'''
Data structure to represent a Ghost entry blog
'''
class BlogEntry():

    def __init__(self,html,date,author):
        self.html=html
        self.date=date
        self.author=author


'''
This class will be responsible to extract posts and publish it.
For now it will only export for epub format. Eventually others
could be added
'''
class GhostBlog():

    AUTHORS_QUERY='select id,name,email from users'
    POSTS_QUERY='select title, html, published_at, author_id from posts'
    SETTINGS_QUERY='select key,value from settings'

    def __init__(self,dbpath):
        self.db=dbpath
        self.conn=sqlite3.connect(self.db)

    '''
    Returns a dictionary with the blog authors
    '''
    def _getAuthors(self):
        authors={}
        c=self.conn.cursor()
        c.execute(self.AUTHORS_QUERY)
        auths = c.fetchall()
        for a in auths:
            authors[str(a[0])]={'name': a[1], 'email': a[2]}
        return authors

    def _getBlogInfo(self):
        info={}
        c=self.conn.cursor()
        c.execute(self.SETTINGS_QUERY)
        settings=c.fetchall()
        for s in settings:
            info[s[0]]=s[1]
        return info


    def _getBlogEntries(self):
        a=self._getAuthors()
        entries = []
        c = self.conn.cursor()
        c.execute(self.POSTS_QUERY)
        ents=c.fetchall()
        for e in ents:
            auth=a[str(e[3])]['name']+" | "+a[str(e[3])]['email']
            entries.append({'title':e[0],'html':e[1],'date':e[2],"author":auth})
        return entries

    def toEpub(self,path='.'):
        spine=['nav']
        authors=self._getAuthors()
        astring = ""
        for k,v in authors.iteritems():
            astring+=v['name']+" "
        info=self._getBlogInfo()
        blog_title=info['title']
        language=info['defaultLang']
        ebook=createEbook(blog_title,blog_title,language,astring)
        entries = self._getBlogEntries()
        for e in entries:
            date=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime(e['date']))
            data="<h1>"+e['title']+"</h1>"+e['html']+"<p><b>"+date+"</b></p>"
            addEntry(ebook,e['title'],language,data,spine)
        addStyle(ebook,spine)
        epub.write_epub(blog_title+'.epub',ebook,{})









gb=GhostBlog('ghost-dev.db')

gb.toEpub()

#for k,v in info.iteritems():
#    print k,v
