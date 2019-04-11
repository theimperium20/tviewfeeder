#!/usr/local/bin/python3.6
#### initializing traders ################
import csv
import os
#initializing feedparser
import feedparser
import time
from dhooks import Webhook, Embed
from datetime import datetime


csvurl = os.path.dirname(os.path.realpath(__file__)) +'/tviewfeeder.csv'
#csvurl = 'tviewfeeder.csv'

with open(csvurl, 'r') as f:
    data = list(csv.reader(f))

feedurl = []
lasttime = []
profilepic = []
caphookurl = []
pname = []

for i in data:
    feedurl.append(i[0])
    lasttime.append(i[1])
    profilepic.append(i[2])
    caphookurl.append(i[3])
    pname.append(i[4])

i = 1
for x in range(i,10):
    #Looper
    print ("Working for " + pname[i])
    tview=feedparser.parse(feedurl[i])
    last_modified = tview.modified.rsplit(' ', 1)[0] #Cutting the word GMT
    print (last_modified)
    c= last_modified.split(',')
    d= lasttime[i].split(',')
    datetime_diff = datetime.strptime(c[1], ' %d %b %Y %H:%M:%S') - datetime.strptime(d[1], ' %d %b %Y %H:%M:%S')

    if(str(datetime_diff)!="00:00:00"):
        tview_update = feedparser.parse(feedurl[i],modified=last_modified)
        entry = tview_update.entries[0]
        title = entry.title
        tviewlink = entry.id
        desc = "**[Open in Tradingview]("+tviewlink+")** \n \n " + entry.summary
        print("Length of Desc is - " + str(len(desc)))
        if len(desc) > 2000 : desc = desc[0:2000]
        pubDate= "Originally Posted on " + entry.published
        img = 'https://s3.tradingview.com/'+ tviewlink[28].lower() + '/' + tviewlink[28:-1]+ '_mid.png'
        # Reference for future https://dhooks.readthedocs.io/en/latest/api.html#webhook
        hook = Webhook(caphookurl[i],avatar_url=profilepic[i],username=pname[i])
        embed = Embed(description=desc, color=0x1e0f3, timestamp='now')
        embed.set_author(name=title, icon_url=profilepic[i])
        embed.set_footer(text=pubDate, icon_url=profilepic[i])
        embed.set_image(img)
        hook.send(embed=embed)
        lasttime[i]=last_modified
        i=i+1
    else:
        print("No post from " + pname[i])
        i=i+1

#Write to file
myFile = open(csvurl, 'w', newline='')
with myFile:
        myFields = ['feedurl', 'lasttime', 'profilepic', 'caphookurl', 'pname']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writeheader()
        j = 1
        for x in range(len(feedurl)-1):
            writer.writerow({'feedurl' : feedurl[j], 'lasttime' : lasttime[j], 'profilepic' : profilepic[j], 'caphookurl' : caphookurl[j], 'pname' : pname[j]})
            j = j+1


