from __future__ import print_function
import nltk, sklearn, string, os
import pandas as pd
from databaseTokens import getTokensFromTitleMap
from databaseTokens import getTokensFromUrlMap
from databaseTokens import getTokensFromTweetMap
import pymysql
from DDatabase import openDatabase
from DDatabase import closeDatabase

from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import numpy as np
from pickler import dumpObject
from pickler import loadObject

from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean


# Preprocessing text with NLTK package
stemmer = PorterStemmer()

#what="title"
#=tweet
#=url
def getTokensDict(conn,limit=0,tokensHaving=None,mapIndexUrl=None,what="title"):
    token_dict = {}
    
    cur = conn.cursor()
    index=-1
    if (limit>0):
        sql="SELECT rowid FROM webtechnology.urls where language='en' LIMIT 0,"+str(limit)
        cur.execute(sql)
    else:
        sql="SELECT rowid FROM webtechnology.urls where language='en'"
        cur.execute(sql)

        
    for r in cur:
        if (what=="title"):
            sentence=titleToTokenSentence(conn,r[0],tokensHaving)
        if (what=="tweet"):
            sentence=tweetToTokenSentence(conn,r[0],tokensHaving)
        if (what=="url"):
            sentence=urlToTokenSentence(conn,r[0],tokensHaving)
            
        if (sentence!=""):
            index=index+1
            mapIndexUrl[index]=r[0]
            token_dict[str(r[0])]=sentence

    cur.close()
    return token_dict


def tweetToTokenSentence(conn,rowId,tokensHaving):
    sentence=""
    cur = conn.cursor()
    cur.execute("SELECT token FROM webtechnology.tokenstweet where rowid="+str(rowId))
    for r in cur:
        if (str(r[0]).lower() in tokensHaving):
            sentence=sentence+" "+str(r[0]).lower()
    cur.close()
    if (sentence==""):
        print(str(rowId))
    return sentence


def urlToTokenSentence(conn,rowId,tokensHaving):
    sentence=""
    cur = conn.cursor()
    cur.execute("SELECT token FROM webtechnology.tokensurl where rowid="+str(rowId))
    for r in cur:
        if (str(r[0]).lower() in tokensHaving):
            sentence=sentence+" "+str(r[0]).lower()
    cur.close()
    if (sentence==""):
        print(str(rowId))
    return sentence

def titleToTokenSentence(conn,rowId,tokensHaving):
    sentence=""
    cur = conn.cursor()
    cur.execute("SELECT token FROM webtechnology.tokenstitle where rowid="+str(rowId))
    for r in cur:
        if (str(r[0]).lower() in tokensHaving):
            sentence=sentence+" "+str(r[0]).lower()
    cur.close()
    if (sentence==""):
        print(str(rowId))
    return sentence

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems



def loadCluster():
    true_k=20
    km=loadObject("d:/webtechnology/km.p")

    tokensTitle=getTokensFromTitleMap(10000)
    conn=openDatabase()
    token_dict=getTokensDict(conn,1000,tokensTitle)
    closeDatabase(conn)
    print("\n Performing stemming and tokenization...")

    #term frequency-inverse document frequency (tf-idf)
    ### change encoding......
    vectorizer = TfidfVectorizer(tokenizer=tokenize, encoding='utf-8',
                              stop_words='english')


    X = vectorizer.fit_transform(token_dict.values())

    centroids = km.cluster_centers_


  
    cosine=cosine_similarity(X.A[0], centroids[0])
    print("cosine ... "+ str(cosine))

    #print("File for :"+filesHash[443])

    for i in range(true_k):
        d = euclidean(X.A[0], centroids[i])
        cosine=cosine_similarity(X.A[0], centroids[i])
        print("i "+ str(i)+" eucl " + str(d)+ " cosine "+str(cosine))






#makes the cluster , based on top frequent words and saves the distances on a table mysql
#parameters number of clusters, how urls to load =0 (all),how many words (tokens) order by frequency to use for the classification
#what="title","url","tweet"
def makeCluster(true_k=5,numberOfUrls=5000,tokensFromMap=5000,what="title"):
   
    mapIndexUrl={}

    if what=="title":
        tokensHaving=getTokensFromTitleMap(tokensFromMap)
    if what=="url":
        tokensHaving=getTokensFromUrlMap(tokensFromMap)
    if what=="tweet":
        tokensHaving=getTokensFromTweetMap(tokensFromMap)
        
    conn=openDatabase()
    token_dict=getTokensDict(conn,numberOfUrls,tokensHaving,mapIndexUrl,what)
    cur = conn.cursor()
    totalUrls=len(token_dict)
    sql = "insert into webtechnology.cluster_info (noOfClusters,noOfUrls,clusterType,noOfTerms,noOfUrlsHavingTerms)"
    sql=sql+" values ("+ str(true_k)+","+str(numberOfUrls)+",'"+ what +"',"+ str(tokensFromMap)+","+ str(totalUrls) +")"
    cur.execute(sql)
    conn.commit()
    cluster_id=cur.lastrowid
    
    print("\n Performing stemming and tokenization...")

    #term frequency-inverse document frequency (tf-idf)
    ### change encoding......
    vectorizer = TfidfVectorizer(tokenizer=tokenize, encoding='utf-8',
                              stop_words='english')

    X = vectorizer.fit_transform(token_dict.values())

    print("n_samples: %d, n_features: %d" % X.shape)
    print()
    ###############################################################################
    # Do the actual clustering
    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)


    clusters = km.fit_predict(X)
    dumpObject(km,"d:/webtechnology/km.p")
    
    centroids = km.cluster_centers_

    for id in mapIndexUrl:
        
        cosineCheck=0.0
        euclideanCheck=2.0
        cosineCluster=-1
        euclideanCluster=-1
        print("url " + str(mapIndexUrl[id]))
        print()
        for i in range(true_k):
            e = euclidean(X.A[id], centroids[i])
            cosine=cosine_similarity(X.A[id], centroids[i])
            if (e<euclideanCheck):
                euclideanCluster=i
                euclideanCheck=e
            if (cosine>cosineCheck):
                cosineCluster=i
                cosineCheck=cosine
        cosineStr="0.0"
        if not (cosineCheck=="0.0"):
            if not (cosineCheck is None):
                if hasattr(cosineCheck, "__getitem__"):
                    cosineStr=cosineCheck[0]
                    cosineStr=str(cosineStr).replace("[","")
                    cosineStr=str(cosineStr).replace("]","")
        
        sql="insert into webtechnology.cluster_urls (rowid,euclidean_distance,cosine_distance,euclidean_cluster,cosine_cluster,cluster_id)"
        sql=sql+" values (" + str(mapIndexUrl[id]) +","+str(euclideanCheck)+","+str(cosineStr)+","+str(euclideanCluster)+","+str(cosineCluster)+","+str(cluster_id)+")"
        print(sql)
        cur.execute(sql)
        conn.commit()

        print("Cosine cluster "+str(cosineCluster))
        print("euclidean cluster "+str(euclideanCluster))   
            
    cur.close()             
    closeDatabase(conn)
    



    ################## test purposes #######################  
    #cosine=cosine_similarity(X.A[0], centroids[0])
    #print("cosine ... "+ str(cosine))

    #print("File for :"+filesHash[443])
    #print("url is "+str(mapIndexUrl[0]))
    #for i in range(true_k):
    #    d = euclidean(X.A[0], centroids[i])
    #    cosine=cosine_similarity(X.A[0], centroids[i])
    #    print("i "+ str(i)+" eucl " + str(d)+ " cosine "+str(cosine))
    #
    #order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    #terms = vectorizer.get_feature_names()

    #Number of clusters, with top word.
    #for i in range(true_k):
    #    print("Cluster %d:" % i, end='')
    #    for ind in order_centroids[i, :30]:
    #        print(' %s' % terms[ind], end='')
    #    print()
    ##################### end of test purposes ################    


#parameters number of clusters, how urls to load =0 (all),how many words (tokens) order by frequency to use for the classification
def debugCluster(true_k=5,numberOfUrls=5000,tokensFromMap=5000):
    ###########################################################################
    #Number of Clusters
    
    tokensTitle=getTokensFromTitleMap(tokensFromMap)
    
    conn=openDatabase()
    token_dict=getTokensDict(conn,numberOfUrls,tokensTitle)
    
    closeDatabase(conn)
    print("\n Performing stemming and tokenization...")

    #term frequency-inverse document frequency (tf-idf)
    ### change encoding......
    vectorizer = TfidfVectorizer(tokenizer=tokenize, encoding='utf-8',
                              stop_words='english')


    X = vectorizer.fit_transform(token_dict.values())

    print("n_samples: %d, n_features: %d" % X.shape)
    print()
    ###############################################################################
    # Do the actual clustering
    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)


    y=km.fit(X)

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

#number of clusters....
#number of top words (terms)
#type=url,title,tweet
makeCluster(20,1000,10000,"tweet")
#loadCluster()
