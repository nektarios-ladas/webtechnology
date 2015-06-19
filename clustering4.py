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
filesHash={}
index=-1
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
            index=index+1
            filesHash[index]=f
        except:
            #print("Error")
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

#print(X.shape)
#X=X_train_tfidf

#y=km.fit(X)

#print(km)
#clusters = km.labels_.tolist()

clusters = km.fit_predict(X)


#print(X[0])
centroids = km.cluster_centers_
#print(centroids[0])

from scipy.spatial.distance import euclidean
cluster_0 = np.where(clusters==0)
X_cluster_0 = X[cluster_0]

from sklearn.metrics.pairwise import cosine_similarity
cosine=cosine_similarity(X.A[443], centroids[0])
print("cosine ... "+ str(cosine))

print("File for :"+filesHash[443])

for i in range(19):
    d = euclidean(X.A[443], centroids[i])
    cosine=cosine_similarity(X.A[443], centroids[i])
    print("i "+ str(i)+" eucl " + str(d)+ " cosine "+str(cosine))
    
#cluster_0 = np.where(clusters==0)

#cluster_1 = np.where(clusters==1)

#X_cluster_0 = X[cluster_0]
#X_cluster_1 = X[cluster_1]


#print(X_cluster_0[1])
#X_cluster_0.data#
#print(X_cluster_0.indices)
#print(X_cluster_0.data)
#print(X_cluster_1.indices)

#from sklearn.metrics.pairwise import euclidean_distances


#D = euclidean_distances(X_cluster_0, km.cluster_centers_[0])
#print(D)

#from scipy.spatial.distance import euclidean

#distance = euclidean(X_cluster_0[0], km.cluster_centers_[0])
#print(distance)

#print("The clusters :" + str(clusters))

print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

#Number of clusters, with top word.
for i in range(true_k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()
