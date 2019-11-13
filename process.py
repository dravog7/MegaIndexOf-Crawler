from urllib.parse import unquote,urlparse
import json
import re
def getseason(a):
    s=re.search('s[0-9]+',a)
    if not(s):
        s=re.search('season(\.| |_)[0-9]+',a)
        if not(s):
            return 1
        return int(s.group()[7:])
    return int(s.group()[1:])

def getepisode(a):
    s=re.search('e[0-9]+',a)
    if not(s):
        s=re.search('ep[0-9]+',a)
        if not(s):
            return 1
        return int(s.group()[2:])
    return int(s.group()[1:])

def getquality(a):
    qualities=['480','720','1080','2160']
    rep='('+"|".join(qualities)+')'
    s=re.search(rep,a)
    if not(s):
        return 'unknwn'
    return s.group()+'p'

def getshow(a):
    qualities=['480','720','1080','2160']
    rep="|".join(qualities)
    s=re.findall('/([a-z| |\.|-|_]+)(?:/|\.|_|-)(?:(?:s[0-9]+)|'+rep+'|E/)',a)
    if not(s):
        return 'unknwn'
    m=s[0]
    return re.sub("(\.| |_|-)"," ",m).strip()
def isdubbed(a):
    a=re.findall('(dubbed)',a)
    return True if a else False

website=input().strip()
filetypes=[".mov",".wmv",".mp4",".mkv",".flv",".avi",".m4v"]
shows=[website]
entries=0
while(True):
    entry={'show':'','season':'','episode':'','quality':'','url':''}
    try:
        url=input().strip()
    except:
        break
    fileformat=url[url.rindex('.'):]
    if(fileformat.lower() in filetypes):
        path=unquote(urlparse(url).path).lower()
        entry["season"]=getseason(path)
        entry['episode']=getepisode(path)
        entry['quality']=getquality(path)
        entry['show']=getshow(path)
        entry['url']=url
        if(isdubbed(path)):
            continue
        if(entry['show']=='unknwn'):
            continue
        shows.append(entry)
print(json.dumps(shows))
