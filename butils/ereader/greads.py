from goodreads import *
import oauth2 as oauth
import urllib
import csv

API_KEY="cf2Z3socJtT9qnlbjxTNw"
API_SECRET="1pSjMkE3tgrHmXdfT3wgpk7vFdYUsdU19t4NoyBg1BA"

OAUTH_TOKEN="1nApzFhQPdb9gFox9llDKw"
OAUTH_SECRET="bP8k8IK0kHRnqOlVXQKWa4xzvDqBvv7FhO4Pq5m3DI"



#print gc.session.get("review.xml")

consumer = oauth.Consumer(key=API_KEY,
                          secret=API_SECRET)

token = oauth.Token(OAUTH_TOKEN,
                    OAUTH_SECRET)

client = oauth.Client(consumer, token)
url = 'http://www.goodreads.com'

#body = urllib.urlencode({'name': 'read', 'book_id': '1'})
#headers = {'content-type': 'application/x-www-form-urlencoded'}
#response, content = client.request('%s/shelf/add_to_shelf.xml' % url,'POST', body, headers)

#print response, content

#body = urllib.urlencode({'book_id': '1', 'review[review]': 'sdkasdhkasd aksjdh kajsdh kajs hdkashd kasdh adasdakshfkajshfas asjf haskjfhaksjf haksfh kashfkashf asfhkash faksfha' , 'review[rating]' : 4, 'shelf':'read'})
#headers = {'content-type': 'application/x-www-form-urlencoded'}
#response, content = client.request('%s/review.xml' % url, 'PUT', body, headers)

#print response,content

#response,content = client.request('%s/user_status/index.xml' % url, 'GET', '',headers)

#print response,content

gc=GoodreadsClient(API_KEY,API_SECRET,OAUTH_TOKEN,OAUTH_SECRET)


#print gc.userStats()
'''
with open('quotes.csv','rb') as quotes_file:
    quotes_reader = csv.reader(quotes_file,delimiter=',')
    for quote in quotes_reader:
        print "ola"#quote[4],'\n\n'
'''

#gc.addBookShelf("Tiririca")
#gc.addBookReview('280111','This is too much for my stomach...','1','Tiririca')
#gc.findBook('JavaScript Application Design_ A Build First Approach - Nicolas Bevacqua','1')
#gc.addQuote('Eric Gamma','1','Os caes ladram e a caravana abana as rodas, dirirara...','','9780201485370')
#gc.getFriendsUpdate()

#gc.getUserFollowers('25570848')
#gc.getUserInfo('25570848')




#print user.name, user.link
