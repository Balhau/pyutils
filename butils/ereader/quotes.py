# coding=utf-8
from goodreads import *


API_KEY="cf2Z3socJtT9qnlbjxTNw"
API_SECRET="1pSjMkE3tgrHmXdfT3wgpk7vFdYUsdU19t4NoyBg1BA"

OAUTH_TOKEN="1nApzFhQPdb9gFox9llDKw"
OAUTH_SECRET="bP8k8IK0kHRnqOlVXQKWa4xzvDqBvv7FhO4Pq5m3DI"

gc=GoodreadsClient(API_KEY,API_SECRET,OAUTH_TOKEN,OAUTH_SECRET)

print gc.getCSVQuotes("balhau@balhau.net","gamma-007")
