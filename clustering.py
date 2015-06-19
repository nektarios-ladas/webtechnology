#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://www.textfiles.com/directory.html



from __future__ import print_function
import nltk, sklearn, string, os
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import numpy as np

# Preprocessing text with NLTK package
token_dict = {}
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems
###########################################################################
# Loading and preprocessing text data
print("\n Loading text dataset:")
path = 'D:/webtechnology/urls2'

for subdir, dirs, files in (os.walk(path)):
    for i,f in enumerate(files):
        print(f)
        file_path = subdir + os.path.sep + f
        try:
            shakes = open(file_path, 'r')
            text = shakes.read()
            lowers = text.lower()
            no_punctuation = lowers.translate(string.punctuation)
            token_dict[f] = no_punctuation
        except:
            pass
###########################################################################
#Number of Clusters
true_k = 20 # *

print("\n Performing stemming and tokenization...")

#term frequency-inverse document frequency (tf-idf)

vectorizer = TfidfVectorizer(tokenizer=tokenize, encoding='latin-1',
                              stop_words='english')


X = vectorizer.fit_transform(token_dict.values())


print("n_samples: %d, n_features: %d" % X.shape)
print()
###############################################################################
# Do the actual clustering
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)

print(X.shape)
#X=X_train_tfidf

y=km.fit(X)

print(km)
clusters = km.labels_.tolist()
print("The clusters :" + str(clusters))

print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

#Number of clusters, with top word.
for i in range(true_k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()
