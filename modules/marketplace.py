import csv
import requests
import requests_random_user_agent

from pprint import pprint
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidArgumentException
from fake_useragent import UserAgent


class Marketplace():
    def __init__(self, product_name, page_limit):
        self.product_name = product_name
        self.page_limit = page_limit
        self.main_driver = self.open_browser()
    

    def randomize_user_agent(self):
        s = requests.Session()
        return s.headers['User-Agent']


    def set_options(self, full_screen=True, *args):
        user_agent = self.randomize_user_agent()

        options = Options()
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--user-agent={}'.format(user_agent))
        if full_screen:
            options.add_argument('--start-maximized')
        else:
            mobile_emulation = {
                "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        for arg in args:
            options.add_argument(arg)
        
        return options

    
    def open_browser(self):
        print("Running Chromedriver..")
        driver = Chrome(executable_path="./chromedriver/chromedriver.exe", options=self.set_options())
        driver.implicitly_wait(5)
        
        return driver


    def remove_overlay(self, *args):
        """ Remove an overlay or pop up ads.

            Keyword arguments:
            *args -- xpath of a html elements
        """
        try:
            print("removing overlay")
            for arg in args:
                overlay = self.main_driver.find_element_by_xpath(arg)
                overlay.click()
        except:
            pass

    
    def find_product(self, searchbar_xpath):
        print("Finding Product: {}".format(self.product_name))
        searchbar = self.main_driver.find_element_by_xpath(searchbar_xpath)
        searchbar.click()
        searchbar.send_keys(self.product_name)
        searchbar.send_keys(Keys.ENTER)


    def scrolls(self, driver, scroll_num=7):
        print("loading content..")
        for i in range(scroll_num):
            driver.find_element_by_xpath("/html/body").send_keys(Keys.PAGE_DOWN)
            sleep(0.8)


    def check_detail(self, driver, selector, css_selector=True, xpath=False):
        """Check if an element is exist or detail is exist in blibli
        
        Keyword arguments:
            driver -- a new window of a chromedriver that load a product from a product url
            css_selector -- the css selector of an html element (Boolean)
            xpath -- the xpath selector of an html element (Boolean)
            selector -- syntax for defining part of html can be xpath or css_selector
        
        Return:
            if content exist return content text
            else return an empty string
        """
        
        try:
            if css_selector:
                detail = driver.find_element_by_css_selector(selector)
            if xpath:
                detail = driver.find_element_by_xpath(selector)

            return detail.text

        except NoSuchElementException:
            return ''


    def is_laptop(self, product):
        title = product['title']
        if 'laptop' in title.lower():
            return True

