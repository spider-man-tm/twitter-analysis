# Twitter data analysis

## 1. Setup
- 必要なライブラリをインストール
- オリジナルではpipenvを利用して、仮想環境を構築
```
$ pipenv install
```
- config.pyを編集

<br>

## 2. Twitterに投稿
```
$ sh post_tweet.sh
>> (tweet を入力)
```

<br>

## 3. 指定したTwitter AccountからWord Cloudを作成
```
$ sh user_data.sh
```
- output file
    - user_data/user_tweet_data.txt
    - user_data/user_tweet_data_ranking.txt
    - user_data/user_tweet_data1.png
    - user_data/user_tweet_data2.png
    - user_data/user_tweet_data3.png

![wc1](output/user_data/user_tweet_data1.png)

<br>

## 4. 指定したWordを含むtweet（全ユーザー）からWord Cloudを作成
```
$ sh word_data.sh
```
- output file
    - word_data/time_data.txt
    - word_data/tweet_data.txt
    - word_data/tweet_data1.png
    - word_data/tweet_data2.png
    - word_data/tweet_data3.png

![wc1](output/word_data/tweet_data3.png)