import json
import config
from requests_oauthlib import OAuth1Session
from time import sleep
import emoji


# 絵文字除去
def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)


# APIキー設定
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
USER = config.USER


# 認証処理
twitter = OAuth1Session(CK, CS, AT, ATS)

# タイムライン取得エンドポイント
url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

# パラメータの定義
params = {
    'screen_name': USER,
    'exclude_replies': True,
    'include_rts': False,
    'count': 200
}

with open('output/user_data/user_tweet_data.txt', 'w') as f:
    for _ in range(30):
        res = twitter.get(url, params=params)
        if res.status_code == 200:

            # API残回数
            limit = res.headers['x-rate-limit-remaining']
            print(f'API Remain: {limit}')
            if limit == 1:
                sleep(60 * 15)

            n = 0
            timeline = json.loads(res.text)

            # 各ツイートの本文を表示
            for i in range(len(timeline)):
                f.write(remove_emoji(timeline[i]['text']) + '\n')
                
                if i == len(timeline) - 1:
                    # 一番最後のツイートIDをパラメータmax_idに追加
                    params['max_id'] = timeline[i]['id'] - 1
