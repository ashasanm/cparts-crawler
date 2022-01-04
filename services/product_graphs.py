from datetime import datetime

from models.products import Products



class productGraphs:
    def __init__(self, category):
        self.category = category
        self.product = Products()
        self.date_format = '%Y-%m-%d'
        self.months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.monthly = {}


    def price_invalid(self, price):
        if price == '':
            return True
        elif len(str(price)) > 8:
            return True
        elif price < 10000:
            return True
        else:
            return False
        
    
    def convert_month(self, date):
        return datetime.strptime(date, self.date_format).strftime("%B")


    def convert_year(self, date):
        return datetime.strptime(date, self.date_format).strftime("%Y")


    def get_average(self):
        average = {}
        for date in self.months:
            average[date] = 0
            items =  self.product.get_products(self.category)
            temp_month = []
            for item in items:
                month = self.convert_month(item['extraction_date'])
                year = self.convert_year(item['extraction_date'])
                price = item['price']
                if self.price_invalid(price):
                    continue
                if month == date:
                    temp_month.append(price)
                    self.monthly['category'] = self.category
                    average[date] = round(sum(temp_month)/len(temp_month))
                    average["year"] = year

        
        self.monthly['average'] = average
        self.monthly['year'] = average['year']
        average = self.convert_to_list(self.monthly['average'])
        self.monthly['average'] = average

        return self.monthly


    def get_minimum(self):
        minimum = {}
        for date in self.months:
            minimum[date] = 0
            items =  self.product.get_products(self.category)
            temp_month = []
            for item in items:
                month = self.convert_month(item['extraction_date'])
                year = self.convert_year(item['extraction_date'])
                price = item['price']
                if self.price_invalid(price):
                    continue
                if month == date:
                    temp_month.append(price)
                    minimum['category'] = self.category
                    minimum[date] = min(temp_month)
                    minimum["year"] = year


        self.monthly['minimum'] = minimum
        self.monthly['year'] = minimum['year']
        minimum = self.convert_to_list(self.monthly['minimum'])
        self.monthly['minimum'] = minimum
        

        return self.monthly


    def get_maximum(self):
        maximum = {}
        for date in self.months:
            maximum[date] = 0
            items =  self.product.get_products(self.category)
            temp_month = []
            for item in items:
                month = self.convert_month(item['extraction_date'])
                year = self.convert_year(item['extraction_date'])
                price = item['price']
                if self.price_invalid(price):
                    continue
                if month == date:
                    temp_month.append(price)
                    maximum['category'] = self.category
                    maximum[date] = max(temp_month)
                    maximum["year"] = year


        self.monthly['maximum'] = maximum
        self.monthly['year'] = maximum['year']
        maximum = self.convert_to_list(self.monthly['maximum'])
        self.monthly['maximum'] = maximum

        return self.monthly

    

    def convert_to_list(self, average: dict):
        result = map(lambda month: average[month], self.months)
        return list(result)
                