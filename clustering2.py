from __future__ import print_function
from math import log, sqrt
from itertools import combinations
import sys
import nltk, sklearn, string, os

def cosine_distance(a, b):
    cos = 0.0
    a_tfidf = a["tfidf"]
    for token, tfidf in b["tfidf"].items():
        if token in a_tfidf:
            cos += tfidf * a_tfidf[token]
    return cos

def normalize(features):
    s=0
    for i in features.items():
        #print(i[1])
        s=s+i[1]**2
    
    norm = 1.0 / sqrt(s)
    
    #                  sum(i**2 for i in features.items()))

    for k, v in features.items():
        features[k] = v * norm
    return features



#def append_tfidf_to(id,doc):
    #tokens = {}
    
    #for id, doc in enumerate(documents):
        #tf = {}
#        doc["tfidf"] = {}
#        doc_tokens = doc.get("tokens", [])
 #       for token in doc_tokens:
#            tf[token] = tf.get(token, 0) + 1
#        num_tokens = len(doc_tokens)
#        if num_tokens > 0:
#            for token, freq in tf.items():
 #               tokens.setdefault(token, []).append((id, float(freq) / num_tokens))

# #   doc_count = float(len(documents))
#    for token, docs in tokens.items():
#        idf = log(doc_count / len(docs))
#        for id, tf in docs:
 #           tfidf = tf * idf
#            if tfidf > 0:
 #               documents[id]["tfidf"][token] = tfidf

#    for doc in documents:
#        doc["tfidf"] = normalize(doc["tfidf"])


def add_tfidf_to(documents):
    tokens = {}
    for id, doc in enumerate(documents):
        tf = {}
        doc["tfidf"] = {}
        doc_tokens = doc.get("tokens", [])
        for token in doc_tokens:
            tf[token] = tf.get(token, 0) + 1
        num_tokens = len(doc_tokens)
        if num_tokens > 0:
            for token, freq in tf.items():
                tokens.setdefault(token, []).append((id, float(freq) / num_tokens))

    doc_count = float(len(documents))
    for token, docs in tokens.items():
        idf = log(doc_count / len(docs))
        for id, tf in docs:
            tfidf = tf * idf
            if tfidf > 0:
                documents[id]["tfidf"][token] = tfidf

    for doc in documents:
        doc["tfidf"] = normalize(doc["tfidf"])

def choose_cluster(node, cluster_lookup, edges):
    new = cluster_lookup[node]
    if node in edges:
        seen, num_seen = {}, {}
        for target, weight in edges.get(node, []):
            seen[cluster_lookup[target]] = seen.get(
                cluster_lookup[target], 0.0) + weight
        for k, v in seen.items():
            num_seen.setdefault(v, []).append(k)
        new = num_seen[max(num_seen)][0]
    return new

def majorclust(graph):
    cluster_lookup = dict((node, i) for i, node in enumerate(graph.nodes))

    count = 0
    movements = set()
    finished = False
    while not finished:
        finished = True
        for node in graph.nodes:
            new = choose_cluster(node, cluster_lookup, graph.edges)
            move = (node, cluster_lookup[node], new)
            if new != cluster_lookup[node] and move not in movements:
                movements.add(move)
                cluster_lookup[node] = new
                finished = False

    clusters = {}
    for k, v in cluster_lookup.items():
        clusters.setdefault(v, []).append(k)

    return clusters.values()

def get_distance_graph(documents):
    class Graph(object):
        def __init__(self):
            self.edges = {}

        def add_edge(self, n1, n2, w):
            self.edges.setdefault(n1, []).append((n2, w))
            self.edges.setdefault(n2, []).append((n1, w))

    graph = Graph()
    doc_ids = range(len(documents))
    graph.nodes = set(doc_ids)
    for a, b in combinations(doc_ids, 2):
        graph.add_edge(a, b, cosine_distance(documents[a], documents[b]))
    return graph


def get_documentFromFiles(hashIndexPointer):
    path = 'D:/webtechnology/urls2'
    c=0
    k=-1
    texts=[]
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
                k=k+1
                texts.append(no_punctuation)
                hashIndexPointer[k]=f.split(".txt")[0]
                #print(k + " "+hashIndexPointer[k])
                token_dict[f] = no_punctuation
            except:
                pass
            
    return [{"text": text, "tokens": text.split()}
            for i, text in enumerate(texts)]
    

def get_documents():
    texts = [
        "foo blub baz",
        "foo bar baz",
        "asdf bsdf csdf",
        "foo bab blub",
        "csdf hddf kjtz",
        "123 456 890",
        "321 890 456 foo",
        "123 890 uiop",
        "a",
    ]
    return [{"text": text, "tokens": text.split()}
             for i, text in enumerate(texts)]

def main(args):
    hashIndexDocumentPointer={}
    #hashIndexPointer[0]=1
    documents=get_documentFromFiles(hashIndexDocumentPointer)
    #for k in hashIndexPointer:
    #    print(str(k)+ " "+str(hashIndexPointer[k]))
    #print(hashIndexPointer[0])
    #return
    
    #documents = get_documents()
    add_tfidf_to(documents)
    dist_graph = get_distance_graph(documents)
    id=0
    for cluster in majorclust(dist_graph):
        print("=========")
        id=id+1
        print("cluster id" + str(id))
        for doc_id in cluster:
            #print(documents[doc_id]["text"])
            #print(documents[doc_id])
            print(str(hashIndexDocumentPointer[doc_id]))
            #str(doc_id))

if __name__ == '__main__':
    main(sys.argv)
