import urllib.request
from bs4 import BeautifulSoup

url = "http://insidehpc.com/2014/11/mellanox-speeds-infiniband-sc14/"
req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

f = urllib.request.urlopen(req)
print(f.read().decode('utf-8'))



url = "http://insidehpc.com/2014/11/mellanox-speeds-infiniband-sc14/"
html = urllib.request.urlopen(url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0'
    }).read()

req = Request('http://www.cmegroup.com/trading/products/#sortField=oi&sortAsc=false&venues=3&page=1&cleared=1&group=1', headers={'User-Agent': 'Mozilla/5.0'})

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




import requests

session = requests.Session()  # so connections are recycled
url="http://bit.ly/1zlf7DX"
resp = session.head(url, allow_redirects=True)
print(resp.url)
