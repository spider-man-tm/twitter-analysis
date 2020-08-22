import config
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = 'https://api.twitter.com/1.1/statuses/update.json'

print('twitter test APIから投稿')

# キーボード入力の取得
tweet = input('>> ')

print('*******************************************')

params = {'status': tweet}

# post送信
res = twitter.post(url, params=params)

# 正常投稿出来た場合
if res.status_code == 200:
    print('Success.')

# 正常投稿出来なかった場合
else:
    print('Failed. : %d' % res.status_code)
