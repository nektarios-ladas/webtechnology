import urllib.request
import requests
from bs4 import BeautifulSoup


from urllib.parse import urlsplit
url = "http://stackoverflow.com/questions/9626535/get-domain-name-from-url"
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
print(base_url)

session = requests.Session()  # so connections are recycled
urlLookup="http://bit.ly/1zlf7DdsdwrererrwereX"
#urlLookup="http://www.fucktheuniverse.com/"
resp = session.head(urlLookup, allow_redirects=True)
print(resp.status_code)




#404 not found

#"http://insidehpc.com/2014/11/mellanox-speeds-infiniband-sc14/"
url = resp.url
print(url)

#... get meta data .....#
#import metadata_parser
#page = metadata_parser.MetadataParser(url)
#print(page.metadata)



req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

html = urllib.request.urlopen(req)

soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)
