from bs4 import BeautifulSoup # to parse html
import requests #to make the request
from urllib.parse import urljoin #to convert relative paths
from threading import Thread #for multithreading
import time #to sleep a thread
import json
class spider:
    q=[]
    nodes=0
    files=[]
    visited=[]
    filename=''
    foldercount=0
    def __init__(self,name,n):
        self.nodes=n
        self.filename=name
        self.q=[]
        self.files=[]
        self.visited=[]
        self.foldercount=0
    
    #main crawl function
    def crawl(self,a,resume=False):
        if(not resume):
            self.q.append(a)
            self.files.append(a)
            self.visited.append(urljoin(a,"../"))
            self.foldercount+=1
        threads=[]
        for i in range(self.nodes):
            threads.append(Thread(target=self.crawlpart,args=(i,)))
            threads[-1].start()
        for i in range(self.nodes):
            threads[i].join()
        self.write()
    
    # add the urls across all thread lists
    def addto(self,urls,n):
        #print(len(urls))
        for i in range(len(urls)):
            #check if folder
            if(urls[i] in self.visited):
                continue
            if(urls[i][-1]=='/'):
                self.foldercount+=1
            else:
                self.files.append(urls[i])
                continue
            self.q.append(urls[i])
        

    # write files found to file
    def write(self):
        a=open(self.filename,"w")
        a.write("\n".join(self.files))
        a.close()

    #the thread function
    def crawlpart(self,n):
        while(self.foldercount>0):
            try:
                i=self.q.pop(0)
                self.crawlthis(i,n)
            except:
                time.sleep(0)
    
    def crawlthis(self,i,n):
        print("viewing ",i,"folder count:",self.foldercount)
        
        try:
            req=requests.head(i,timeout=5) #to avoid downloading videos
            #print(req.headers)
            if(req.headers["Content-Type"].count('text/html')>0):
                req=requests.get(i,timeout=5)
                soup=BeautifulSoup(req.content,"html.parser")
                q=soup.find_all('a')
                urls=[urljoin(i,x.attrs["href"]) for x in q]
                self.visited.append(i)
                self.addto(urls,n)
                if(i[-1]=="/"):
                    self.foldercount-=1 #added after addto to prevent 0ing foldercount
            else:
                self.files.append(i)
        except:
            self.q.append(i)
            self.save()
    
    def save(self):
        a=open(self.filename+".sav","w")
        a.write(json.dumps(self.__dict__))
        a.close()
    def resume(self,filename):
        a=open(filename,"r")
        dic=json.loads(a.read())
        self.foldercount=len(dic['q'])
        self.visited=dic['visited']
        self.q=dic['q']
        self.files=dic['files']
        self.filename=dic['filename']
        self.nodes=dic['nodes']
        self.crawl("",resume=True)
