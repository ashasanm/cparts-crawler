import csv
from pprint import pprint
from time import sleep
from datetime import datetime
from random import randint

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .marketplace import Marketplace
from models.products import Products
from .preprocessor.preprocessor import clean_price, clean_sold, is_desktop
from utils.id_finder import find_item_id, find_shop_id
from utils.api_extractor import ShopeeAPI

class Shopee(Marketplace):
    def __init__(self, product_name, category, page_limit=10,):
        super().__init__(product_name, page_limit)
        self.product_db = Products()
        self.category = category


    def get_links(self):
        links = self.main_driver.find_elements_by_css_selector('div.row.shopee-search-item-result__items > div > a')
        links = [link.get_attribute('href') for link in links]

        return links


    def get_detail(self, link):
        print("loading content..")
        # driver.get(link)

        # title_xpath = '//*[@id="main"]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/span'
        # price_xpath = '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/div[3]/div/div/div/div/div/div'
        # sold_xpath = '//*[@id="main"]/div/div[2]/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/div[1]'
        
        # city_xpath = '//*[text() = "Dikirim Dari"]/following-sibling::div'
        
        # # image_xpath = '//*[@id="main"]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]/div[1]/div/div/div'
                        
        
        # # my_property = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, image_xpath))).value_of_css_property("background-image").split('"')[1]
        
        # # print(my_property)

        # xpaths = [title_xpath, price_xpath, sold_xpath, city_xpath]
        # details = [self.check_detail(driver, xpath, css_selector=False, xpath=True) for xpath in xpaths]

        # print(details)

        itemid = find_item_id(link)
        shopid = find_shop_id(link)
        print("ITEM ID AND SHOP ID: ", itemid, shopid)
        shopee_api = ShopeeAPI()
        api_url = shopee_api.construct_url(shopid=shopid, itemid=itemid)
        print("API_URL", api_url)
        details = shopee_api.extract(api_url)
        price = details['data']['price']



        result = {
            'marketplace': 'shopee',
            'title': details['data']['name'],
            'price': int(str(price)[:-5]),
            'sold': details['data']['sold'],
            'city': details['data']['shop_location'],
            'link': link,
            'extraction_date':datetime.now().strftime("%Y-%m-%d")
        }
        print("content extracted..")
        pprint(result)

        return result

    # def get_images(self):
    #     img_xpath = '//*[@id="main"]/div/div[3]/div/div[2]/div[2]/div[2]/div/a/div/div/div[1]/img'
    #     self.main_driver.find_elements_by_xpath()

    def extract(self):
        # load Base URL
        base_url = self.main_driver.current_url
        self.main_driver.get("https://shopee.co.id/search?keyword=" + self.product_name)

        # searchbar_xpath = '//*[@id="main"]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div/form/input'
        # ads_xpath = '//*[@id="modal"]/div/div/div[2]/div'
        # self.remove_overlay(ads_xpath)
        # self.find_product(searchbar_xpath)
        
        page = 1
        current_link = self.main_driver.current_url
        
        # Open new window
        # driver = self.open_browser()

        while page <= self.page_limit:
            # Check page
            if page > 1:
                next_url = current_link + "&page={}".format(page)
                self.main_driver.get(next_url)

            self.scrolls(driver=self.main_driver)
            links = self.get_links()
            tries = 0
            for link in links:
                # Extract Items
                try:
                    item = self.get_detail(link)
                except Exception as e:
                    print("FOUND EXCEPTION: ", e)
                    tries += 1
                    if tries > 7:
                        page = self.page_limit + 1
                        break
                    continue
                if item['title'] == '':
                    continue
                if self.product_db.is_exist(query=item, category=self.category):
                    print("item already exist!")
                    continue
                if is_desktop(item['title'], self.category):
                    self.product_db.add_product(item, category=self.category)
                    print("Saved to database")
                sleep(randint(0, 2))
            
            page += 1


        self.main_driver.close()



# if __name__ == '__main__':
#     product_name = input("find products: ")
#     shopee = Shopee(product_name=product_name, page_limit=5)
#     products = shopee.extract()
#     shopee.save_to_csv(products)
 