import time
from pprint import pprint
from datetime import datetime
from random import randint

from .marketplace import Marketplace
from .preprocessor.preprocessor import clean_price, clean_sold, is_desktop
from models.products import Products

class Tokopedia(Marketplace):
    def __init__(self, product_name, category, page_limit=10):
        super().__init__(product_name, page_limit)
        self.url = "https://www.tokopedia.com"
        self.product_db = Products()
        self.category = category

    def get_links(self):
        print("extract content urls..")
        urls = self.main_driver.find_elements_by_xpath('//*[@id="zeus-root"]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div[2]/a')
        urls = [url.get_attribute('href') for url in urls]
        
        promo_url = []

        for url in urls[:]:
            if 'ta.tokopedia' in url:
                promo_url.append(url)
                urls.remove(url)
        try:
            promo = self.reformat_promo_url(promo_url)
            links = [*urls, *promo]
        except:
            links = urls
            pass

        return links

    
    def reformat_promo_url(self, promo_url):
        separator = 'https%3A%2F%2F'
        urls = []
        for url in promo_url:
            url = url.split(separator)
            url = url[1].replace("%2F", "/")
            urls.append(url)
        
        return urls


    def get_detail(self, driver, link):
        print("loading content..")
        driver.get(link)

        title_xpath = '//*[@id="pdp_comp-product_content"]/div/h1'
        sold_xpath = '//*[@id="pdp_comp-product_content"]/div/div[1]/div/div[@data-testid="lblPDPDetailProductSoldCounter"]'
        price_xpath = '//div/div[contains(@class, "price")]'
        city_xpath = '//*[@id="pdp_comp-shipment"]/div/div/div[1]/div/b'

        xpaths = [title_xpath, sold_xpath, price_xpath, city_xpath]
        details = []
        for  xpath in xpaths:
            detail = self.check_detail(driver, xpath, css_selector=False, xpath=True)
            details.append(detail)

        result = {
            'marketplace': 'tokopedia',
            'title': details[0],
            'price': clean_price(details[2]),
            'sold': clean_sold(details[1]),
            'city': details[3],
            'link': driver.current_url,
            'extraction_date':datetime.now().strftime("%Y-%m-%d")
        }
        print("content extracted..")
        pprint(result)

        return result


    def next_page(self, base_search_url, page):
        self.main_driver.get(base_search_url + '&page={}'.format(page))

    
    def extract(self):
        self.main_driver.get(self.url)
        searchbar_xpath = '//*[@id="search-container"]/form/div/div/div/input'
        self.find_product(searchbar_xpath)
        overlay1_xpath = "//*[contains(text(),'Oke, Lanjut Belanja')]"
        overlay2_xpath = "/html/body/div[5]/div[7]/section/div/div/div[2]/div"
        self.scrolls(scroll_num=7, driver=self.main_driver)
        self.remove_overlay(overlay1_xpath, overlay2_xpath)
        
        base_search_url = self.main_driver.current_url
        print("open new chrome instance..")
        sub_driver = self.open_browser()
        for page in range(1, self.page_limit+1):
            if page > 1:
                print("load page {}".format(page))
                self.next_page(base_search_url, page)
                self.scrolls(driver=self.main_driver)
                links = self.get_links()
            else:
                links = self.get_links()
            
            print(links)
            for link in links:
                try:
                    item = self.get_detail(sub_driver, link)
                    if item['title'] == '':
                        continue
                    # Check if product already inside Database
                    if self.product_db.is_exist(query=item, category=self.category):
                        print("item already exist!")
                        continue
                    if is_desktop(item['title'], self.category):
                        self.product_db.add_product(product=item, category=self.category)
                        print("item saved..")
                except Exception as e:
                    print(e)
                    pass

                time.sleep(randint(0, 2))

        sub_driver.close()
        self.main_driver.close()

    







# if __name__ == '__main__':
#     product_name = 'gtx 1050'
#     page_limit = 10
    
#     tokped = Tokopedia(product_name, page_limit)
#     data = tokped.extract()
#     pprint(data)
#     print(len(data))
#     print("Tokopedia extraction complete!")
