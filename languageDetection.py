from langdetect import detect

with open("D:/webtechnology/urls2/5.txt",encoding="utf8") as myfile:
    data="".join(line.rstrip() for line in myfile)

print(detect(data))
cur = conn.cursor()
cur.execute("SELECT Host,User FROM user")
for r in cur:
    print(r)
cur.close()
conn.close()
