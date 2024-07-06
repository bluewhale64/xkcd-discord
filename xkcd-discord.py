import requests
import datetime
import time
import html
#This uses the in-built html module. Do not try to install it with pip.
import os

webhook = os.getenv("XKCD_WEBHOOK_URL")

def sendRequest(method, args):
    #0 is get, 1 is post
    #wrapper for post and get to handle request failures
    #will catch requests failing from connection issues
    #will not catch xkcd.com being down or http errors
    check = 0
    while check == 0:
        if method == 0:
            try:
                r = requests.get(args[0])
                check = 1
                return(r.text)
            except:
                print("CONNECTION ISSUE. WAITING 10 SECONDS TO TRY AGAIN.")
                time.sleep(10)
        elif method == 1:
            try:
                r = requests.post(args[0],json=args[1])
                check = 1
                return(r)
            except:
                print("CONNECTION ISSUE. WAITING 10 SECONDS TO TRY AGAIN.")
                time.sleep(10)
        else:
            print("INVALID REQUEST TYPE")
            check = 1
            return("")

def storeLast(number):
    f = open("last.txt", "w+")
    f.write(str(number))
    f.close()

def getLast():
    #gets number of last comic from last.txt
    #if the number is invalid, returns -1
    f = open("last.txt", "a+")
    f.seek(0)
    last_raw = f.readline()
    f.close()
    try:
        last = int(last_raw)
        return(last)
    except:
        return(-1)

def getComic(comic):
    #if comic == -1, go straight to last comic
    #html.unescape() used to decode html character tags
    link = "https://xkcd.com"
    if comic != -1:
        link = link + "/" + str(comic) + "/"
    pass
    r = sendRequest(0, [link])
    website = r[r.index("<div id=\"comic\">")+17:]
    website = website[:website.index("</div>")-1]
    link = "https:" + website[website.index("img src")+9:website.index("title")-2]
    link = link[:-4] + "_2x.png" #edit link to double resolution version of comic
    text = html.unescape(website[website.index("title")+7:website.index("alt")-2])
    name = html.unescape(website[website.index("alt")+5:website.index("srcset")-2])
    number = r[r.index("Permanent link to this comic")+56:]
    number = number[:number.index("\"")]
    return([link, name, text, int(number)])

def makeEmbed(link, name, text, number):
    #By default, the message will use the profile picture of the Black Hat character, and the sender name will be Black Hat.
    #The colour will also be hex colour 0x004D33, represented as decimal 19763.
    #These can be customised by editing the relevant fields to whatever you want.
    #Custom hex colours must be converted into decimal format in order to display correctly.
    return({
        "avatar_url":"https://www.explainxkcd.com/wiki/images/6/6d/BlackHat_head.png",
        "username":"Black Hat",
        "embeds": [{
        "title": "#" + str(number) + " - " + name,
        "url": "https://xkcd.com/" + str(number),
        "description": "```\n" + text + "\n```",
        "image": {
        "url": link},
        "color": 19763,
        "footer": {
        "text": datetime.datetime.today().strftime('%Y/%m/%d')}}]})

def postEmbed(webhook_url, message):
    r = sendRequest(1, [webhook_url, message])

def sendComic(webhook_url, comic):
    xkcd = getComic(comic)
    postEmbed(webhook_url, makeEmbed(xkcd[0],xkcd[1],xkcd[2],xkcd[3]))
    storeLast(xkcd[3])

while True:
    last = getLast()
    recent = getComic(-1)[-1]
    if recent >= last:
        if recent > last and last > 0:
            #if most recent > last.txt : for each in between, post at 10 second intervals, then set number of current comic as last
            for  i in range(last + 1, recent + 1):
                print(i)
                sendComic(webhook, i)
                time.sleep(10)
        elif recent > last:
            sendComic(webhook, -1)
        pass
            #up to date so do nothing
    else:
        #if most recent < last.txt: proceed straight to most recent comic and set number of current comic as last
        sendComic(webhook, -1)
    time.sleep(3600)
