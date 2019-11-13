import crawl
from threading import Thread
t=int(input())
for i in range(t):
    q=input().strip()
    print("going through %s .."%(q,))
    cr=crawl.spider("%d.txt"%(i+2,),10)
    cr.crawl(q)
