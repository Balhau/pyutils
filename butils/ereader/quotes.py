# coding=utf-8
import urllib
import urllib2
from bs4 import BeautifulSoup


#get login page

url = 'https://www.goodreads.com/user/sign_in?source=home'
req = urllib2.Request(url)
res = urllib2.urlopen(req)

htmlLogin=res.read()

soup = BeautifulSoup(htmlLogin, 'html.parser')

forms=soup.find_all('form')

#This is the auth_token
auth_token=forms[0].find("input", {"name":"authenticity_token"})['value']

values = {'utf8' : '✓',
          'user[email]' : 'balhau@balhau.net',
          'authenticity_token' : auth_token,
          'remember_me' : 'Python',
          'user[password]' : 'balhau-007'
}

#Post login, pass
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()

#Get the session id
headers=""+str(response.info())
harray=headers.split("\n")
sid=harray[len(harray)-2].split("Set-Cookie:")[1]

#Get quotes in csv
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', '_session_id2=fbef491ea7eaf23af000b6fe40199f45'))
f = opener.open("https://www.goodreads.com/quotes/goodreads_quotes_export.csv")

print f.read()
