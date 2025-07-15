import requests
import time
from discord_webhook import DiscordWebhook

IDS = [] #separated by comma

timeperrequest = 1 # recommend more time for less items, and vice versa
Webhook = "" # do not share

idstat = {}

session = requests.Session()
cookie = ''
session.headers.update({
    'Cookie': cookie,
})

def sendmessage(message):
    webhook = DiscordWebhook(url=Webhook, content=message)
    webhook.execute()

def getnames():
    global idstat
    names = []
    for id in IDS:
        ar = session.get(f'https://economy.roblox.com/v2/assets/{id}/details').json()
        name = ar['Name']
        yes = ar['IsForSale']
        price = ar['PriceInRobux']
        idstat[id] = {
                'sale': yes,
                'price': price,
                'name': name
                }
        if yes:
            names.append(f"[{name}](<https://roblox.com/catalog/{id}>) {price} <:robux:1394424886507864075>\n")
        else:
            names.append(f"[{name}](<https://roblox.com/catalog/{id}>) :x:\n")
        
    return ''.join(names)

def checkitem(id):
    global idstat
    sale = idstat[id]['sale']
    price = idstat[id]['price']
    ar = session.get(f'https://economy.roblox.com/v2/assets/{id}/details').json()
    newsale = ar['IsForSale']
    newprice = ar['PriceInRobux']

    if newsale != sale:
        idstat[id]['sale'] = newsale
        idstat[id]['price'] = newprice
        return 1
    else:
        if newprice != price:
            idstat[id]['price'] = newprice
            return 2
        return 3
    

sendmessage(f"**Sniper** is targetting **{len(IDS)}** items :\n{getnames()}")

while True:
    try:
        for id in IDS:
            info = idstat[id]
            status = checkitem(id)
            if status == 1:
                if info['sale']:
                   sendmessage(f"[{info['name']}](https://roblox.com/catalog/{id}) is **ONSALE** for **{info['price']}**")
                else:
                    sendmessage(f"[{info['name']}](<https://roblox.com/catalog/{id}>) went OFFSALE")
            elif status == 2:
                sendmessage(f"[{info['name']}](<https://roblox.com/catalog/{id}>) price changed to {info['price']}")
            elif status == 3:
                pass
            time.sleep(timeperrequest)
    except:
        time.sleep(15)


    
