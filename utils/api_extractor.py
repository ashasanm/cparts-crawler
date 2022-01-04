import requests
import json
import time


class ShopeeAPI:
    def __init__(self):
        self.api_url = "https://shopee.co.id/api/v4/item/get?"

    def construct_url(self, itemid:str, shopid:str):
        return self.api_url + f"itemid={itemid}" + f"&shopid={shopid}"
    
    def extract(self, url:str):
        print(f"Waiting for response from {url}")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}
        res = requests.get(url, headers=headers)
        time.sleep(0.3)
        print("fetching api..")
        return res.json()



        
