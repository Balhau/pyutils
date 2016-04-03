# coding=utf-8
import xmltodict
import json
import oauth2 as oauth
import urllib
from urllib import quote_plus
import urllib2
from bs4 import BeautifulSoup

'''
    Utility function to encode UTF8 data
'''
def urlencode_utf8(params):
    if hasattr(params, 'items'):
        params = params.items()
    return '&'.join(
        (quote_plus(k.encode('utf8'), safe='/') + '=' + quote_plus(v.encode('utf8'), safe='/')
            for k, v in params))

'''
  Author: Balhau, <balhau@balhau.net>

  This is a API, using OAUTH, for the goodreads shitty API. Others API that I checked for python were badly designed or with lots of methods unimplemented
  Here I'll try to implement as much as I can regarding goodreads.com oauth API


'''
class GoodreadsClient():

  base_url = "https://www.goodreads.com"
  consumer = None
  token = None

  '''
      This is GoodreadsClient constructor and receives four parameters which are all that is needed to do oauth requests
      To see how you can create a access_token and access_secret check the file goauth.py which is a python script
      that uses OAuth to create a token request. Then you use that link on the browser to give access to the application after that
  '''
  def __init__(self, app_key, app_secret,access_token,access_secret):
      """Initialize the client"""
      self.headers = {'content-type': 'application/x-www-form-urlencoded'}
      self.consumer = oauth.Consumer(key=app_key,
                                secret=app_secret)

      self.token = oauth.Token(access_token,
                          access_secret)

      self.client = oauth.Client(self.consumer, self.token)


  ''' This will return statistics regarding the user'''
  def userStats(self):
    response,content = self.client.request('%s/user_status/index.xml' % self.base_url, 'GET', '',self.headers)
    return response,self.respToDic(content)


  def addBookReview(self,idBook,review,rating,shelve='read'):
    body = urlencode_utf8({'book_id': idBook, 'review[review]': review , 'review[rating]' : rating, 'shelf':shelve})
    response, content = self.client.request('%s/review.xml' % self.base_url, 'POST', body, self.headers)
    print response,content
    return response,self.respToDic(content)

  def updateBookReview(self,idBook,review,rating,shelve='read'):
   body = urlencode_utf8({'book_id': idBook, 'review[review]': review , 'review[rating]' : rating, 'shelf':shelve})
   response, content = self.client.request('%s/review/%s.xml' % (self.base_url,idBook), 'PUT', body, self.headers)
   return response,self.respToDic(content)

  def addBookShelf(self,name,exclusive="false",sortable="false",featured="false"):
    body = urlencode_utf8({'user_shelf[name]': name, 'user_shelf[exclusive_flag]': exclusive , 'user_shelf[sortable_flag]' : sortable, 'user_shelf[featured]':featured})
    response,content= self.client.request('%s/user_shelves.xml' % self.base_url, 'POST', body, self.headers)
    print response,content
    return response,self.respToDic(content)

  def getUserFollowers(self, idUser):
    response,content= self.client.request('%s/user/%s/followers?format=xml' % (self.base_url,idUser), 'GET', '')
    return response,self.respToDic(content)

  def getUserFollowing(self, idUser):
    response,content= self.client.request('%s/user/%s/following?format=xml' % (self.base_url,idUser), 'GET', '')
    return response,self.respToDic(content)

  def getUserInfo(self,idUser):
    response,content= self.client.request('%s/user/show/%s.xml' % (self.base_url,idUser), 'GET', '')
    return response,self.respToDic(content)

  def findBook(self,query,page):
    response,content= self.client.request('%s/search/index.xml?q=%s&page=%s' % (self.base_url,query,page), 'GET', '')
    #print response,content
    return response,self.respToDic(content)

  def recentMembersReviews(self):
    response,content = self.client.request('%s/review/recent_reviews.xml' % self.base_url, 'GET','')
    print response,content
    return response,self.respToDic(content)

  def getFriendsUpdate(self):
      response,content = self.client.request('%s/updates/friends.xml' % self.base_url, 'GET', '')
      print response,content
      return response,self.respToDic(content)

  def addQuote(self,author_name,book_id,quote,comma_separated_tags='',isbn=''):
    #body = urllib.urlencode({'quote[author_name]' : author_name, 'quote[book_id]' : book_id, 'quote[body]' : quote, 'quote[tags]' : comma_separated_tags,'isbn':isbn},encoding='UTF-8')
    body=urlencode_utf8({'quote[author_name]' : author_name, 'quote[book_id]' : book_id, 'quote[body]' : quote, 'quote[tags]' : comma_separated_tags,'isbn':isbn})
    response,content = self.client.request('%s/quotes?format=xml' % self.base_url, 'POST', body,self.headers)
    print response,content
    return response,self.respToDic(content)

  def respToDic(self,content,data_format='xml'):
    if data_format == 'xml':
        data_dict = xmltodict.parse(content)
        return data_dict
    elif data_format == 'json':
        return json.loads(content)

  '''
  This will fetch the csv with all the existing quotes in your account
  '''
  def getCSVQuotes(self,email,password):
      #get login page

      url = 'https://www.goodreads.com/user/sign_in'
      req = urllib2.Request(url)
      res = urllib2.urlopen(req)

      h1s=str(res.info())

      h1=h1s.split("\n")
      csid=h1[len(h1)-4].split("Set-Cookie: ")[1].split(";")[0]
      locale=h1[len(h1)-3].split("Set-Cookie: ")[1].split(";")[0]
      sid=h1[len(h1)-2].split("Set-Cookie: ")[1].split(";")[0]

      htmlLogin=res.read()

      soup = BeautifulSoup(htmlLogin, 'html.parser')

      forms=soup.find_all('form')

      #This is the auth_token
      auth_token=forms[0].find("input", {"name":"authenticity_token"})['value']
      num = forms[0].find("input",{"name":"n"})['value']

      headers={
          "Host" : "www.goodreads.com",
          "Origin" : "https://www.goodreads.com",
          "Referer": "https://www.goodreads.com/user/sign_in",
          "Cookie" : csid+";"+locale+";"+sid+";"
      }


      post = {
          'utf8' : '✓',
          'user[email]' : email,
          'authenticity_token' : auth_token,
          'remember_me' : 'on',
          'next' : 'Sign in',
          'n' : str(num),
          'user[password]' : password
      }

      #print post

      #url="http://localhost/lolada"
      #Post login, pass
      data = urllib.urlencode(post)
      req = urllib2.Request(url, data,headers)
      response = urllib2.urlopen(req)
      the_page = response.read()

      #Get quotes in csv
      opener = urllib2.build_opener()
      opener.addheaders.append(('Cookie', sid))
      opener.addheaders.append(('Origin','http://www.goodreads.com'))
      #opener.addheaders.append(('Referer','https://www.goodreads.com'))
      f = opener.open("https://www.goodreads.com/quotes/goodreads_quotes_export.csv")

      return f.read()
