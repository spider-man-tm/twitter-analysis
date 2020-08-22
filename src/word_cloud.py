# coding:utf-8
import os
import csv
import argparse
from PIL import Image
import numpy as np
from janome.analyzer import Analyzer
from janome.tokenfilter import CompoundNounFilter
from wordcloud import WordCloud, ImageColorGenerator
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--output_file', type=str, required=True, help='output file')
parser.add_argument('-m', '--mask_file', type=str, required=True, help='mask file')
args = parser.parse_args()
OUTPUT_FILE = args.output_file
MASK_FILE = args.mask_file


# 名詞のみ抽出 & 単語数のカウント
def counter(texts):
    a = Analyzer(token_filters=[CompoundNounFilter()])
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = a.analyze(text)

        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞', '形容詞']:
                words_count[token.base_form] += 1
                if 'engineers_lt' in token.base_form:
                    token.base_form = 'engineers_lt'
                words.append(
                    token.base_form.strip('@').strip('#').strip(':').strip('\"')
                )
    return words_count, words


with open(f'output/{OUTPUT_FILE}.txt', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    texts = []
    for row in reader:
        if(len(row) > 0):
            text = row[0].split('http')
            texts.append(text[0])

words_count, words = counter(texts)
text = ' '.join(words)

fpath = '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'

stop_words = [
    u'こと', u'よう', u'そう', u'これ', u'それ',
    u'みたい', u'ため', u'やつ', u'さん', u'RT',
    u'ない', u'ほど',
]

mask_path = os.path.join('mask_data', MASK_FILE)
mask = np.array(Image.open(mask_path))
image_color1 = ImageColorGenerator(mask)
image_color2 = lambda *args, **kwargs: (255, 255, 255)

wordcloud1 = WordCloud(
    collocations=False,
    background_color='white',
    font_path=fpath,
    width=1200,
    height=800,
    stopwords=set(stop_words),
    max_words=1000,
    min_font_size=5
).generate(text)

wordcloud2 = WordCloud(
    mask=mask,
    color_func=image_color1,
    background_color=(16, 41, 97),
    font_path=fpath,
    stopwords=set(stop_words),
    max_words=2000,
    contour_width=11,
    contour_color=(255, 255, 255),
    min_font_size=10
).generate(text)

wordcloud3 = WordCloud(
    mask=mask,
    color_func=image_color2,
    background_color=(16, 41, 97),
    font_path=fpath,
    stopwords=set(stop_words),
    max_words=2000,
    contour_width=10,
    contour_color=(170, 0, 10),
    min_font_size=10
).generate(text)

wordcloud1.to_file(f'output/{OUTPUT_FILE}1.png')
wordcloud2.to_file(f'output/{OUTPUT_FILE}2.png')
wordcloud3.to_file(f'output/{OUTPUT_FILE}3.png')
