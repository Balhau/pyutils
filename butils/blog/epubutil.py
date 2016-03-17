from ebooklib import epub


def createEbook(idEbook,ebookTitle,lang,authors):

    book = epub.EpubBook()
    book.set_identifier(idEbook)
    book.set_title(ebookTitle)
    book.set_language(lang)

    for author in authors:
        book.add_author(author)

    return book

def addStyle(ebook,spine,style='BODY {color: white;}'):
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    ebook.add_item(nav_css)
    ebook.spine=spine

def addEntry(ebook,title,language,data,spine):
    c1=epub.EpubHtml(title=title,file_name=title+'.xhtml',lang=language)
    c1.content=data
    ebook.add_item(c1)
    ebook.toc=ebook.toc+[epub.Link(title+'.xhtml',title,title)]
    spine.append(c1)
