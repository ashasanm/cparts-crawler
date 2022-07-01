import csv
import pandas as pd
from datetime import datetime
import time
from random import randint

from utils.alert import print_alert
from modules.blibli import Blibli
from modules.tokopedia import Tokopedia
from modules.shopee import Shopee
from gpu_lists import get_amd_gpu, get_nvidia_gtx_gpu, get_nvidia_rtx_gpu


def get_from_blibli(product_name, category, page_limit):
    blibli = Blibli(product_name, category,page_limit)
    blibli_products = blibli.extract()
    
    return blibli_products

def get_from_tokopedia(product_name, category, page_limit):
    tokopedia = Tokopedia(product_name, category, page_limit)
    tokopedia_products = tokopedia.extract()

    return tokopedia_products

def get_from_shopee(product_name, category, page_limit):
    shopee = Shopee(product_name, category,page_limit)
    shopee_products = shopee.extract()

    return shopee_products



def start_extract_products(product_name, category, page_limit):
    try:
        # get_from_shopee(product_name, category, page_limit) # Shopee need to be fixed
        # get_from_blibli(product_name, category, page_limit)
        get_from_tokopedia(product_name, category, page_limit)
            
    except Exception as e:
        print("found an exception!")
        print_alert(e)
        pass

if __name__ == '__main__':

    # #CPU

    # intel_series = ["i3", "i5", "i7", "i9"]
    # for intel in intel_series:
    #     for gen in range(8, 12):
    #         product = "intel core {} gen {}".format(intel, gen)
    #         start_extract_products(product_name=product, category="cpu", page_limit=5)


    # amd_series = ["athlon", "ryzen 3", "ryzen 5", "ryzen 7", "ryzen 9"]
    # for amd in amd_series:
    #     product = "amd {}".format(amd)
    #     start_extract_products(product_name=product, category="cpu", page_limit=5)
    
    # # GPU

    # for product in get_nvidia_gtx_gpu():
    #     start_extract_products(product_name=product, category="gpu",page_limit=5)
    #     time.sleep(2)
    
    # for product in get_nvidia_rtx_gpu():
    #     start_extract_products(product_name=product, category="gpu",page_limit=5)
    #     time.sleep(2)
    
    for product in get_amd_gpu():
        start_extract_products(product_name=product, category="gpu",page_limit=5)
        time.sleep(2)

    # CASE
    start_extract_products(product_name='case pc desktop', category='case', page_limit=20)

    # MEMORY  
    for ddr in ['ddr3', 'ddr4']:
        start_extract_products(product_name='ram pc {}'.format(ddr), category='memory', page_limit=20)


    storages = ['ssd', 'hdd', 'nvme', 'm2 nvme']
    # # STORAGE
    for storage in storages:
        start_extract_products(product_name='{}'.format(storage), category='storage', page_limit=20)
    
    # # MOTHERBOARD
    brands = ["amd", 'intel']
    for brand in brands:
        start_extract_products(product_name='motherboard {}'.format(brand), category='motherboard', page_limit=30)

    # PSU
    

