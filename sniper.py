import requests
import time
from discord_webhook import DiscordWebhook

ID = # SET ID HERE
timeperrequest = 2 # CHANGE TIME PER CHECK
Webhook = "" # ENTER YOUR WEBHOOK URL

onsale = 0
offsale = 0
pricechange = 0
firstprice = 0
first = 0

# DO NOT SHARE
# FULL COOKIE DATA NOT JUST ROBLOSECURITY
cookie = ""

headers = {
    'cookie': cookie,  
}



while True:   
    data = requests.get(f"https://economy.roblox.com/v2/assets/{ID}/details", headers=headers)
    status = data.status_code
    print(f"Status code: {data.status_code}")
    data = data.json()

    sale = data.get("IsForSale", True)
    name = data.get("Name", [])


    price = data.get("PriceInRobux", [])
    
    if first == 0:
        webhook = DiscordWebhook(url=Webhook, content=f"Sniper has been set to target {name} (https://roblox.com/catalog/{ID})")
        response = webhook.execute()
        first = 1 
        
    if sale:
        if onsale == 0 and status == 200:               
            print(f"{name} Is onsale for {price}")
            webhook = DiscordWebhook(url=Webhook, content=f"{name} Is onsale for {price} Robux! Buy it here: https://roblox.com/catalog/{ID}")
            response = webhook.execute()
            onsale = 1
            offsale = 0
            if pricechange == 0:
                firstprice = price
                print(f"defaulting original price to {firstprice} Robux")
            time.sleep(timeperrequest)
        elif onsale == 1:
            if price != firstprice:
                print("price changed")
                webhook = DiscordWebhook(url=Webhook, content=f"{name} https://roblox.com/catalog/{ID} 's price has changed from {firstprice} Robux to {price} Robux")
                response = webhook.execute()
                pricechange = 0
                firstprice = price
                print(f"defaulting original price to {firstprice} Robux")
            print("still onsale!")
            time.sleep(timeperrequest)
                
        elif status == 429:  # IF YOU GET 429 TOO MANY REQUESTS, YOUR COOKIE IS INVALID
            print("Too many requests")
            time.sleep(timeperrequest)
        
    else:
        if offsale == 0:           
            print("offsale")
            webhook = DiscordWebhook(url=Webhook, content="item is offsale")
            response = webhook.execute()
            onsale = 0
            offsale = 1
            time.sleep(timeperrequest)
        elif offsale == 1:
            print("still offsale")
            time.sleep(timeperrequest)
