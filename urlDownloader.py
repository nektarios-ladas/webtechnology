import urllib.request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from tld import get_tld
from socket import timeout
from lxml.html import fromstring
import lxml.html
from langdetect import detect
import pymysql
import furl
import nltk
import enchant
from nltk.corpus import stopwords
stop = stopwords.words('english')
dictionary = enchant.Dict("en_US")
#check's what kind of delimiter a url string contains
#most of times is a - or _
def whichDelimiterUrlStringContains(urlstr):
    delimiter=""
    if "-" in urlstr:
        sentence=urlstr.replace("-"," ")
        tokens= nltk.word_tokenize(sentence)
        tokens2=[x for x in tokens if x not in stop]
        if not tokens2 is None:
            return "-"
    if "_" in urlstr:
        sentence=urlstr.replace("_"," ")
        tokens= nltk.word_tokenize(sentence)
        tokens2=[x for x in tokens if x not in stop]
        if not tokens2 is None:
            return "_"     

#takes a delimited word that is a multiple word and returns the words on a list
def urlPathToWords(word,delimiter,words_list):
    if delimiter=="":
        tokens=nltk.word_tokenize(word)
    else:
        sentence=word.replace(delimiter, " ")
        tokens= nltk.word_tokenize(sentence)
        #tokens2=[x for x in tokens if x not in stop]
    for tk in tokens:
        if dictionary.check(tk):
            words_list.append(tk)
            
#takes a url, and by reference the domain , the paths list and the word tokens of the paths    
def urlTooler(url,domain,paths_list,words_list):
    f=furl.furl(url)
    #print(f)
    #print(f.host)
    domain.append(f.host)
    if (not f.path==""):
        paths=str(f.path).split("/")
        for p in paths:
            delimiter=whichDelimiterUrlStringContains(p)
            if not delimiter is None:
                w_l=[]
                urlPathToWords(p,delimiter,w_l)
                
                paths_list.append(p)
                for w in w_l:
                    words_list.append(w)
            else:
                w_l=[]
                urlPathToWords(p,"",w_l)
                        
              
    if (not f.fragment==""):
        paths=str(f.fragment).split("/")
        for p in paths:
            delimiter=whichDelimiterUrlStringContains(p)
            if not delimiter is None:
                w_l=[]
                urlPathToWords(p,delimiter,w_l)
                paths_list.append(p)
                for w in w_l:
                    words_list.append(w)
            else:
                w_l=[]
                urlPathToWords(p,"",w_l)


#writes on a filename a text (string)       
def writeToFile(filename,text):
    fo = open(filename, "wb")
    #fo.write(text);
    fo.write(bytes(text, 'UTF-8'))
    # Close opend file
    fo.close()

#Takes a url , checks if it exists and then expands it
def urlExists(urlLookup):
    try:
        session = requests.Session()
        resp = session.head(urlLookup, allow_redirects=True,timeout=10)
        if not (resp.status_code==404 and resp.status_code==403):
            return resp.url
        else:
            return ""
    except:
        return ""
    
#returns the domain name of a url
def getDomainName(url):
    domain=""
    try:
        domain=get_tld(url)
        return domain
    except:
        return ""
    
#to check for meta keywords
def PrintMetaKeywords(soup):
  print('<h3>Page meta keywords:</h3>')
  mk = ''
  l = soup.findAll("meta")
  print(l)
  if l == []:
    mk = "No meta keywords"
  else:
    mk = l[0]['content'].encode('utf-8')
  print('<h4>' + mk + '</h4>')
    

#returns the domain name of a html text
def getHtmlText(url,metaArray,info):
    text=""
    #print("setting metaArray")
    #metaArray["set"]=222
    #print("setted")
    
    #user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    #headers={'User-Agent':user_agent,} 
    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
                #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
             
        )
       
        #req=urllib.request.Request(url,None,headers)
    

        f = urllib.request.urlopen(req,timeout=10)
       
        html=f.read().decode('utf-8')

        soup = BeautifulSoup(html)

        
        title=soup.html.head.title.string
        info["title"]=title
        #print(title)
      

        html_element = lxml.html.fromstring(html)
        
        
        # get all the name attributes from all meta elements
        meta_name_list = html_element.xpath("//meta/@name")
        # print them out
        tree = fromstring(html)

        #print("Getting metadata")
        for name in meta_name_list:
            metaArray[name]=tree.xpath('//meta[@name="'+name+'"]/@content')
            #print(name)
            #print(tree.xpath('//meta[@name="'+name+'"]/@content'))     

        #print("Got metadata")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        #      drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        language=detect(text)
        print(language)
        info["language"]=language
    except:
        print("Error downloading "+url)

    return text

#downloads the url and inserts them on the database , see the inserts ....
#for multithreading needs the starLine Number of the file and the how many to download for each thread (breaknumber).
# ----------- usage example --------------#
#
#import _thread
#try:
#    _thread.start_new_thread( downloadPages, (6723, 20000))
#    _thread.start_new_thread( downloadPages, (26723, 20000))
#    _thread.start_new_thread( downloadPages, (46723, 20000))
#    _thread.start_new_thread( downloadPages, (66723, 20000))
#except:
#    print("unable to start thread")


def downloadPages(startLine=0,breakNumber=0):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology',use_unicode=True, charset="utf8")
    domains = {}
    missed=0
    fobj = open("d:/urldata/urls2.tsv",encoding="utf8")
    line=0
    id=0
    if (startLine>0):
        for x in fobj:
            line=line+1
            id=id+1
            if (line>=startLine):
                break
    for x in fobj:
        line=line+1
    
        if line>=(breakNumber+startLine):
            break
        if line>=0:
            id=id+1
            url=x.split("\t")[0]
            urlOriginal=url
            tweetMessage=x.split("\t")[4]
            dateurl=x.split("\t")[1]
            tweetId=str(x.split("\t")[2])
            nof_users=x.split("\t")[5]
            nof_tweets=x.split("\t")[6]
            max_retweets=x.split("\t")[7]
        
            #print(tweetMessage)
            url=urlExists(url)
            print("="+str(line)+"=")
            if url!="":
                domain=getDomainName(url)
                if not domain=="": 
                    if not domain in domains:
                        domains[domain]=1
                    else:
                        domains[domain]=domains[domain]+1
                #print(getDomainName(url))
                title=""
                metaArray={}
                info={}
                language=""
                text=getHtmlText(url,metaArray,info)
                if not text=="":
                    rowId=id
                    title=info["title"]
                    if (title!=None):
                        title=title.replace("\\","")
                    else:
                        title=""          
                        #print("Setting id "+str(id))
                    #print(info["title"])
                    #print(info["language"])
                    #print(metaArray)

                    try:
                        language=info["language"]
                        sql = "INSERT INTO webtechnology.urls (rowid, originalurl,expandedurl,title,language,tweet_id,tweet_text,urldate,nof_users,nof_tweets,max_retweets) VALUES ("+str(rowId)+",'" + urlOriginal.replace("'","''") + "','"+url.replace("'","''")+"','"+title.replace("'","''")+"','"+language+"','"+tweetId+"','"+tweetMessage.replace("'","''")+"','"+dateurl+"',"+nof_users+","+nof_tweets+","+max_retweets+")"
                        #print(sql)
                        with conn.cursor() as cursor:
                            cursor.execute(sql)
                        conn.commit()
                        for key in metaArray:
                            val=str(metaArray[key]).replace("['","")
                            val=str(val).replace("']","")
                    
                            val=val.replace("'","''")
                            val=val.replace("\\","")
                            sql = "INSERT INTO webtechnology.metadata (rowid, metadataname,metadatavalue) VALUES ("+str(rowId)+",'" + key.replace("'","''") + "','"+val+"')"
                        #print(sql)
                            with conn.cursor() as cursor:
                                cursor.execute(sql)
                                #print(sql)
                                conn.commit()
                    except:
                        pass
                    writeToFile("d:/webtechnology/urls2/"+str(id)+".txt",text)

    strData=""
    for k in domains:
        strData=strData+"\n"+k+"\t"+str(domains[k])

    writeToFile("d:/webtechnology/domainsFrequency2.txt",strData)

def urlTokenizeData():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Fireblade', db='webtechnology')
    cur = conn.cursor()
    cur1= conn.cursor()
    cur.execute("SELECT rowId,expandedurl,title,tweet_text FROM webtechnology.urls where language='en'")
    for r in cur:
        print("#" +str(r[0]))
        domain=[]
        paths_list=[]
        words_list=[]
        urlTooler(r[1],domain,paths_list,words_list)

        sql = "update webtechnology.urls set domain='"+ domain[0]  +"' where rowid="+str(r[0])               
       
        cur1.execute(sql)
        conn.commit()

        for p in paths_list:
            sql = "insert into webtechnology.url_paths (rowid,path) values ("+ str(r[0])+",'"+p.replace("'","''")+"')"
            #print(sql)
            cur1.execute(sql)
            conn.commit()
        
        for w in  words_list:
            sql = "insert into webtechnology.tokensurl (rowid,token) values ("+ str(r[0])+",'"+w.replace("'","''")+"')"
            #print(sql)
            cur1.execute(sql)
            conn.commit()

        titles_list=[]
        
        urlPathToWords(r[2],"",titles_list)
        for t in  titles_list:
            sql = "insert into webtechnology.tokenstitle (rowid,token) values ("+ str(r[0])+",'"+t.replace("'","''")+"')"
            #print(sql)
            cur1.execute(sql)
            conn.commit()

        tweets_list=[]
        urlPathToWords(r[3],"", tweets_list)
        
        for tw in tweets_list:
            sql = "insert into webtechnology.tokenstweet (rowid,token) values ("+ str(r[0])+",'"+tw.replace("'","''")+"')"
            cur1.execute(sql)
            conn.commit()
        
        #print(domain)

        #print(paths_list)
        #print(words_list)


        
    cur.close()
    conn.close()

    
urlTokenizeData()

#domain=[]
#paths_list=[]
#words_list=[]
#urlTooler("http://www.krellinst.org/csgf/conf/2014/video/kantypas",domain,paths_list,words_list)
#print(domain)
#print(paths_list)
#print(words_list)


#
#import _thread
#try:
#    _thread.start_new_thread( downloadPages, (6723, 20000))
#    _thread.start_new_thread( downloadPages, (26723, 20000))
#    _thread.start_new_thread( downloadPages, (46723, 20000))
#    _thread.start_new_thread( downloadPages, (66723, 20000))
#except:
#    print("unable to start thread")
