from datetime import datetime

from models.products import Products
from .product_graphs import productGraphs

class categoryGraphs(productGraphs):
    def __init__(self, category):
        super().__init__(category)
        self.marketplace = ['tokopedia', 'shopee', 'blibli']


    def get_by_marketplace(self, marketplace):
        data_object = self.product.filter_by_marketplace(marketplace, self.category)
        return [result for result in data_object]


    def calculate_month(self, data: list, value):
        if value == "average":
            return round(sum(data)/len(data))
        elif value == "minimum":
            return min(data)
        elif value == "maximum":
            return max(data)


    def calculate_data(self, value_calculator: str):
        for market in self.marketplace:
            temp_calculation = {}
            items =  self.get_by_marketplace(market)
            temp_month = []
            for date in self.months:
                temp_calculation[date] = 0
                for item in items:
                    month = self.convert_month(item['extraction_date'])
                    year = self.convert_year(item['extraction_date'])
                    price = item['price']
                    if self.price_invalid(price):
                        continue
                    if month == date:
                        temp_month.append(price)
                        self.monthly['category'] = self.category
                        temp_calculation[date] = self.calculate_month(temp_month, value_calculator)
                        temp_calculation["year"] = year
                        

            self.monthly["sort_by"] = value_calculator
            self.monthly[market] = temp_calculation
            self.monthly['year'] = temp_calculation['year']
            temp_calculation = self.convert_to_list(self.monthly[market])
            self.monthly[market] = temp_calculation

        return self.monthly



    
        
