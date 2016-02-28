import json
from ebooklib import epub
import urllib2


book = epub.EpubBook()

book.set_identifier('idMissIBook')
book.set_title('Mr P and Miss I\n The journal')
book.set_language('pt')

book.add_author('Mr P')
book.add_author('Miss I')

BLOGG = "mrp-and-missi"
BLOGGER_URL='http://{}.blogspot.com/feeds/posts/default?alt=json&callback=mycallbackfunc&start-index=1&max-results=500'.format(BLOGG)

httpdata = urllib2.urlopen(BLOGGER_URL)
jsonCallback = httpdata.read()

#Extract the callBack declaration
jsonData=jsonCallback[31:]
#Extract the final 2 chars that represent ");" for the enclosing of the callback
jsonData=jsonData[:-2]

#Now parse the data into json object
blogData=json.loads(jsonData)
entries= blogData['feed']['entry']

cc=['nav']

#Iterate over the posts
for entry in reversed(entries):
    name=entry['author'][0]['name']['$t']
    dataPublished = entry['published']['$t']
    title=entry['title']['$t']
    header='<h1>'+title+'</h1>'+'<h4>'+dataPublished.split("T")[0]+'</h4>'
    content=header+entry['content']['$t']
    c1 = epub.EpubHtml(title=title, file_name=title+'.xhtml', lang='pt')
    c1.content=content
    book.add_item(c1)
    book.toc = book.toc + [epub.Link(title+'.xhtml', title, title)]
    cc.append(c1)

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
# add CSS file
book.add_item(nav_css)
# basic spine
book.spine = cc
# write to the file
epub.write_epub('mrp-and-missi.epub', book, {})
