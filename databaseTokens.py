import pymysql
import furl
import nltk
import enchant
from nltk.corpus import stopwords
stop = stopwords.words('english')
dictionary = enchant.Dict("en_US")

def getTokensFromTitleMap(howmany=10):
    tokensmap={}
    outmap=[]
    counter=0
    import operator
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology')
    cur = conn.cursor()
    cur.execute("SELECT count(*) as freq,token FROM webtechnology.tokenstitle group by token")
    for r in cur:
        tokensmap[str(r[1]).lower()]=r[0]
        #print("#" +str(r[0])+ " "+str(r[1]))

    sorted_x = sorted(tokensmap.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    for s in sorted_x:
        if s[0].lower() not in stop:
            counter=counter+1
            if (counter<=howmany):
                outmap.append(s[0])
                #print(s[0]+ " " +str(s[1]))
            else:
                break
    cur.close()
    conn.close()
    return outmap

def getTokensFromTweetMap(howmany=10):
    tokensmap={}
    outmap=[]
    counter=0
    import operator
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology')
    cur = conn.cursor()
    cur.execute("SELECT count(*) as freq,token FROM webtechnology.tokenstweet group by token")
    for r in cur:
        tokensmap[str(r[1]).lower()]=r[0]
        #print("#" +str(r[0])+ " "+str(r[1]))

    sorted_x = sorted(tokensmap.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    for s in sorted_x:
        if s[0].lower() not in stop:
            counter=counter+1
            if (counter<=howmany):
                outmap.append(s[0])
                #print(s[0]+ " " +str(s[1]))
            else:
                break
    cur.close()
    conn.close()
    return outmap    

def getTokensFromUrlMap(howmany=10):
    tokensmap={}
    outmap=[]
    counter=0
    import operator
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology')
    cur = conn.cursor()
    cur.execute("SELECT count(*) as freq,token FROM webtechnology.tokensurl group by token")
    for r in cur:
        tokensmap[str(r[1]).lower()]=r[0]
        #print("#" +str(r[0])+ " "+str(r[1]))

    sorted_x = sorted(tokensmap.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    for s in sorted_x:
        if s[0].lower() not in stop:
            counter=counter+1
            if (counter<=howmany):
                outmap.append(s[0])
                #print(s[0]+ " " +str(s[1]))
            else:
                break
    cur.close()
    conn.close()
    return outmap    

#print(stop)                       
#tk=getTokensFromTitleMap()
#print(tk)
