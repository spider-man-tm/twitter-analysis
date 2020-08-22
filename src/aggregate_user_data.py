# coding:utf-8
import csv
import collections

with open('output/user_data/user_tweet_data.txt', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    texts = []
    for row in reader:
        if(len(row) > 0):
            texts.append(row[0])

words = collections.Counter(texts)
print(words.most_common(10))

with open('output/user_data/user_tweet_data_ranking.txt', 'w') as f:
    for i, item in enumerate(words.most_common(100)):
        print(f'word{i+1} : {item}')
        f.write(item[0] + ' : ' + str(item[1]) + 'ツイート' + '\n')
