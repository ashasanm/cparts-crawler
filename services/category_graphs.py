from datetime import datetime

from models.products import Products
from .product_graphs import productGraphs

class categoryGraphs(productGraphs):
    def __init__(self, category):
        super().__init__(category)
        self.marketplace = ['tokopedia', 'shopee', 'blibli']
        # self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


    def get_by_marketplace(self, marketplace, year_filter):
        data_object = self.product.filter_by_marketplace(marketplace, self.category, year_filter)
        return [result for result in data_object]


    def calculate_month(self, data: list, value):
        if value == "average":
            return round(sum(data)/len(data))
        elif value == "minimum":
            return min(data)
        elif value == "maximum":
            return max(data)
    
    def calculate_data_v2(self, value_calculator:str, year_filter:str,):
        data = {}
        for market in self.marketplace:
            for date in self.months:
                items = self.product.get_cat_graph(value_calculator, date, self.category, year_filter)
                check_items = [item.get('_id').get('month') for item in items]
                if not any(check_items):
                    data[date] = 0
                for item in items:
                    db_market = item.get('_id').get('marketplace')
                    raw_month = item.get('_id').get('month')
                    result = item.get('result')
                    if not result:
                        result = self.MAX_CPU
                    if db_market == market and raw_month:
                        data[date] = round(result)


            result = self.convert_to_list(data)
            self.monthly['category'] = self.category
            self.monthly['sort_by'] = self.CALCULATOR.get(value_calculator)
            self.monthly[market] = result
            self.monthly['year'] = year_filter
            print(data, self.category, market, year_filter, self.CALCULATOR.get(value_calculator))


    def calculate_data(self, value_calculator: str, year_filter: str):
        for market in self.marketplace:
            temp_calculation = {}
            items =  self.get_by_marketplace(market, year_filter)
            temp_month = []
            for date in self.months:
                temp_calculation[date] = 0
                for item in items:
                    month = self.convert_month(item['extraction_date'])
                    price = item['price']
                    if self.price_invalid(price):
                        continue
                    if month == date:
                        temp_month.append(price)
                        temp_calculation[date] = self.calculate_month(temp_month, value_calculator)
                print(temp_calculation)
            print(temp_month)
            
            self.monthly['category'] = self.category
            self.monthly["sort_by"] = value_calculator
            self.monthly[market] = temp_calculation
            self.monthly["year"] = year_filter
            temp_calculation = self.convert_to_list(self.monthly[market])
            self.monthly[market] = temp_calculation

        return self.monthly



    
        
