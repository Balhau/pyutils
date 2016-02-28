import xmltodict
import json
import oauth2 as oauth
import urllib

'''
  Author: Balhau, <balhau@balhau.net>

  This is a API, using OAUTH, for the goodreads shitty API. Others API that I checked for python were badly designed or with lots of methods unimplemented
  Here I'll try to implement as much as I can regarding goodreads.com oauth API


'''
class GoodreadsClient():

  base_url = "https://www.goodreads.com"

  def __init__(self, app_key, app_secret,access_token,access_secret):
      """Initialize the client"""
      self.headers = {'content-type': 'application/x-www-form-urlencoded'}
      consumer = oauth.Consumer(key=app_key,
                                secret=app_secret)

      token = oauth.Token(access_token,
                          access_secret)

      self.client = oauth.Client(consumer, token)


  ''' This will return statistics regarding the user'''
  def userStats(self):
    response,content = self.client.request('%s/user_status/index.xml' % self.base_url, 'GET', '',self.headers)
    return response,self.respToDic(content)


  def addBookReview(self,idBook,review,rating,shelve='read'):
    body = urllib.urlencode({'book_id': idBook, 'review[review]': review , 'review[rating]' : rating, 'shelf':shelve})
    response, content = self.client.request('%s/review.xml' % self.base_url, 'POST', body, self.headers)
    print response,content
    return response,self.respToDic(content)

  def updateBookReview(self,idBook,review,rating,shelve='read'):
   body = urllib.urlencode({'book_id': idBook, 'review[review]': review , 'review[rating]' : rating, 'shelf':shelve})
   response, content = self.client.request('%s/review/%s.xml' % (self.base_url,idBook), 'PUT', body, self.headers)
   return response,self.respToDic(content)

  def addBookShelf(self,name,exclusive="false",sortable="false",featured="false"):
    body = urllib.urlencode({'user_shelf[name]': name, 'user_shelf[exclusive_flag]': exclusive , 'user_shelf[sortable_flag]' : sortable, 'user_shelf[featured]':featured})
    response,content= self.client.request('%s/user_shelves.xml' % self.base_url, 'POST', body, self.headers)
    print response,content
    return response,self.respToDic(content)

  def getUserFollowers(self, idUser):
    body = ''
    response,content= self.client.request('%s/user/%s/followers?format=xml' % (self.base_url,idUser), 'GET', '')
    return response,self.respToDic(content)

  def getUserFollowing(self, idUser):
    body = ''
    response,content= self.client.request('%s/user/%s/following?format=xml' % (self.base_url,idUser), 'GET', '')
    return response,self.respToDic(content)

  def getUserInfo(self,idUser):
    body = ''
    response,content= self.client.request('%s/user/show/%s.xml' % (self.base_url,idUser), 'GET', '')
    return response,self.respToDic(content)

  def findBook(self,query,page):
    body = ''
    response,content= self.client.request('%s/search/index.xml?q=%s&page=%s' % (self.base_url,query,page), 'GET', '')
    print response,content
    return response,self.respToDic(content)


  def respToDic(self,content,data_format='xml'):
    if data_format == 'xml':
        data_dict = xmltodict.parse(content)
        return data_dict
    elif data_format == 'json':
        return json.loads(content)
