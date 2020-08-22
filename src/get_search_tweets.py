import json
import config
from requests_oauthlib import OAuth1Session
from time import sleep
import emoji
from datetime import datetime, timezone, timedelta


# 絵文字を除去する
def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)


# APIキー設定
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
SEARCH_WORD = config.SEARCH_WORD
SINCE = config.SINCE
UNTIL = config.UNTIL

# 認証処理
twitter = OAuth1Session(CK, CS, AT, ATS)

# 指定したクエリに合致する関連 ツイートを取得します。
url = 'https://api.twitter.com/1.1/search/tweets.json'

# パラメータの定義
params = {
    'q': SEARCH_WORD,
    'count': 300,
    'result_type': 'recent',
    'exclude': 'retweets',  # リツイートを含まない
    'since': '2020-08-15_00:00:00_JST',
    'until': '2020-08-22_00:00:00_JST',
}

f_out = open('output/word_data/tweet_data.txt', 'w')
f_out2 = open('output/word_data/time_data.txt', 'w')
f_out3 = open('output/word_data/user_data.txt', 'w')

count = 0
for j in range(60):
    res = twitter.get(url, params=params)
    if res.status_code == 200:
        # API残り回数
        limit = res.headers['x-rate-limit-remaining']
        print(f'API remain: {limit}')
        if limit == 1:
            sleep(60 * 15)

        n = 0
        timeline = json.loads(res.text)

        if len(timeline["statuses"]) == 0:
            break

        # 各ツイートの本文を表示
        for i in range(len(timeline['statuses'])):
            data = timeline['statuses'][i]
            count += 1

            d = datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S %z %Y')
            JST = timezone(timedelta(hours=+9), 'JST')
            d = datetime.fromtimestamp(d.timestamp(), JST)

            f_out.write(remove_emoji(data['text']) + '\n')
            f_out2.write(d.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            f_out3.write('ユーザー名:' + data['user']['screen_name'] + '\n')
            
            if i == len(timeline['statuses']) - 1:
                # 一番最後のツイートIDをパラメータmax_idに追加
                params['max_id'] = data['id'] - 1

f_out.close()
f_out2.close()
f_out3.close()
print(f'ツイートデータ数 : {str(count)}')
