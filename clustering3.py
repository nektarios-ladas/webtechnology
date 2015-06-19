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
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline

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
c=0
for subdir, dirs, files in (os.walk(path)):
    for i,f in enumerate(files):
        #print(f)
        c=c+1
        file_path = subdir + os.path.sep + f
        try:
            shakes = open(file_path, 'r')
            text = shakes.read()
            lowers = text.lower()
            no_punctuation = lowers.translate(string.punctuation)
            #print(no_punctuation)
            token_dict[f] = no_punctuation
        except:
            pass
###########################################################################
#Number of Clusters
true_k = 100 # *

print("\n Performing stemming and tokenization...")


hasher = TfidfVectorizer(max_df=0.5,
                             min_df=2, stop_words='english',
                             use_idf=1)
make_pipeline(hasher, TfidfTransformer())
vectorizer = make_pipeline(hasher, TfidfTransformer())
# document_text_list is a list of all text in a given article
X = vectorizer.fit_transform(token_dict.values())

#term frequency-inverse document frequency (tf-idf)

#vectorizer = TfidfVectorizer(tokenizer=tokenize, encoding='latin-1',
                             # stop_words='english')


#X = vectorizer.fit_transform(token_dict.values())


print("n_samples: %d, n_features: %d" % X.shape)
print()
###############################################################################
# Do the actual clustering
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)

#X=X_train_tfidf

#y=km.fit(X)

clusters=km.fit_predict(X)

#print(X.shape)
#print(clusters.shape)

# Example to get all documents in cluster 0
cluster_0 = np.where(clusters==2) # don't forget import numpy as np

# cluster_0 now contains all indices of the documents in this cluster, to get the actual documents you'd do:
X_cluster_0 = X[cluster_0]

#print(hasher.get_feature_names()[1748])

print("X null cluster")
print(X_cluster_0)
print("-------------")
#y = km.fit_predict(X)

#print(X_cluster_0[1])


print(km)
clusters = km.labels_.tolist()
print("The clusters :" + str(clusters))

print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = hasher.get_feature_names()

#Number of clusters, with top word.
for i in range(true_k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()


#print(X)

#.keys()

data={'file':token_dict.keys(),'cluster':clusters}

frame=pd.DataFrame(data,index=[clusters],columns=['file','cluster'])

print(frame['cluster'].value_counts())

#print(frame['file'][80])

#print(frame['file'][2])
#cluster_0=np.where(clusters==0)
#x_cluster_0=y[cluster_0]
#print(x_cluster_0)


#print(cluster_0)
#print(len(cluster_0))
#for j in cluster_0:
#    print(j)

#print(cluster_0[0])
