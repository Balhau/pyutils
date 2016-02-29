API_KEY="APP_KEY"
API_SECRET="API_SECRET"

# oauth example for goodreads
#
# based on code found in https://gist.github.com/gpiancastelli/537923 by Giulio Piancastelli
#
# edit script with your dev key and secret
# run it
# visit the url
# confirm that you have accepted
# write down token!
#

import oauth2 as oauth
import urllib
import urlparse

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token' % url
authorize_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token' % url

consumer = oauth.Consumer(key=API_KEY,
                          secret=API_SECRET)

client = oauth.Client(consumer)

response, content = client.request(request_token_url, 'GET')
if response['status'] != '200':
    raise Exception('Invalid response: %s, content: ' % response['status'] + content)

request_token = dict(urlparse.parse_qsl(content))

authorize_link = '%s?oauth_token=%s' % (authorize_url,
                                        request_token['oauth_token'])
print "Use a browser to visit this link and accept your application:"
print authorize_link
accepted = 'n'

while accepted.lower() == 'n':
    # you need to access the authorize_link via a browser,
    # and proceed to manually authorize the consumer
    accepted = raw_input('Have you authorized me? (y/n) ')

token = oauth.Token(request_token['oauth_token'],
                    request_token['oauth_token_secret'])

client = oauth.Client(consumer, token)
response, content = client.request(access_token_url, 'POST')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

access_token = dict(urlparse.parse_qsl(content))
