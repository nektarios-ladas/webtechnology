import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology')
print(conn)
sentence="This week on @Verold: tutorial videos for setting up animations &amp; cinematics. http://t.co/gizw49oFgA"
sentence="SpaceX unveils sleek, reusable Dragon crew capsule - space - 30 May 2014 - New Scientist"
#sentence="21635078-high-frequency-trading-might-reduce-liquidity-not-boost-it-its-defenders"
tokens= nltk.word_tokenize(sentence)
tokens2=[x for x in tokens if x not in stop]

print(tokens)
print(tokens2)
