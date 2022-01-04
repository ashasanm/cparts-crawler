import time
from datetime import datetime
from random import randint
from pprint import pprint

from .marketplace import Marketplace
from .preprocessor.preprocessor import clean_price, clean_sold, is_desktop
from models.products import Products


class Blibli(Marketplace):
    def __init__(self, product_name, category, page_limit=10 ):
        super().__init__(product_name, page_limit)
        self.product_db = Products()
        self.category = category

    
    def next_page(self, base_search_url, page):
        self.main_driver.get(base_search_url + '?page={}&start=40'.format(page))


    def get_detail(self, driver):
        """ Extracting web content detail from a product in blibli

        Keyword arguments:
            driver -- a new window of a chromedriver that load a product from a url

        Return:
            a dictionary contains title, price, sold, city, and product url
        """

        print("extract product info .. ")
        title_selector = '.product-name'
        price_selector = '.product-price > div.final-price > span'
        sold_selector = '#product-info > div.product-statistics > span'
        city_selector = '.text-ellipsis'

        css_selectors = [title_selector, price_selector, sold_selector, city_selector]
        details = []
        # Check each elements existence
        for css_selector in css_selectors:
            detail = self.check_detail(driver,css_selector)
            details.append(detail)

        link = driver.current_url

        result = {
            'marketplace': 'blibli',
            'title': details[0],
            'price': clean_price(details[1]),
            'sold': clean_sold(details[2]),
            'city': details[3],
            'link': driver.current_url,
            'extraction_date':datetime.now().strftime("%Y-%m-%d")
        }

        print("content extracted..")
        pprint(result)

        return result


    def get_links(self):
        links = self.main_driver.find_elements_by_css_selector('.product__card > div > .product__item > a')
        links = [link.get_attribute('href') for link in links]

        return links


    def extract(self):
        self.main_driver.get('https://blibli.com')
        searchbar_xpath = '/html/body/div[1]/div/header/div/div/div/div[1]/input'
        self.find_product(searchbar_xpath)
        base_search_url = self.main_driver.current_url
        sub_driver = self.open_browser()
        page = 1
        
        if self.get_maximum_page() < self.page_limit:
            self.page_limit = self.get_maximum_page()
        
        while page <= self.page_limit:
            self.scrolls(driver=self.main_driver, scroll_num=4)
            links = self.get_links()
            print(links)

            # extracting details from new chrome windows
            for link in links:
                time.sleep(randint(1, 3))
                sub_driver.get(link)
                product = self.get_detail(sub_driver)
                
                if product['title'] == '':
                    continue

                print("check into databases..")
                # Check if product already inside Database
                if self.product_db.is_exist(query=product, category=self.category):
                    print("item already exist!")
                    continue
                
                print("check items..")
                if is_desktop(product['title'], self.category):
                    self.product_db.add_product(product, self.category)
                    print("item saved..")
                    
                time.sleep(randint(0, 3))

            page += 1
            self.next_page(base_search_url, page)

        self.main_driver.close()
        sub_driver.close()

    
    def get_maximum_page(self):
        total_product = self.main_driver.find_element_by_css_selector('.product-listing-totalItem').text
        total_product = total_product.lower()
        total_product = total_product.replace(" ", "")
        total_product = total_product.replace("produk", "")
        max_page = float() / 40
        max_page = round(max_page)
        if max_page == 0:
            return 1

        return max_page 



# if __name__ == '__main__':
#     blibli = Blibli(product_name='rtx 2060', page_limit=5)
#     data = blibli.extract()
#     print('{} data extracted:'.format(len(data)))
#     pprint(data)
    