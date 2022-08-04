from datetime import datetime

from models.products import Products



class productGraphs:
    def __init__(self, category):
        self.category = category
        self.product = Products()
        self.date_format = '%Y-%m-%d'
        self.months = ['1','2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        self.monthly = {}
        self.CALCULATOR = {
            'avg': 'average',
            'min': 'minimum',
            'max': 'maximum'
        }
        self.MAX_CPU = 12000000


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

    def get_monthly(self, count_by:str, year_filter:str='2022'):
        data = {}
        calculator = self.CALCULATOR.get(count_by)
        for date in self.months:
            data[date] = 0
            items = self.product.get_products_with_aggregate(self.category, date, year_filter, count_by)
            for item in items:
                raw_month = item.get('_id').get('month')
                result = item.get('result')
                if not result:
                    result = self.MAX_CPU
            
                if raw_month:
                    raw_month = raw_month.get('match').replace("-", "").replace("0", "")
                else: continue
                data[raw_month] = round(result)
        
        result = self.convert_to_list(data)

        self.monthly['year'] = year_filter
        self.monthly['category'] = self.category
        self.monthly[calculator] = result
                


    # def get_average(self, year_filter='2022'):
    #     average = {}
    #     for date in self.months:
    #         average[date] = 0
    #         items =  self.product.get_products(self.category, year_filter)
    #         print(items)
    #         temp_month = []
    #     #     for item in items:
    #     #         month = self.convert_month(item['extraction_date'])
    #     #         year = self.convert_year(item['extraction_date'])
    #     #         price = item['price']
    #     #         if self.price_invalid(price):
    #     #             continue
    #     #         if month == date:
    #     #             temp_month.append(price)
    #     #             self.monthly['category'] = self.category
    #     #             average[date] = round(sum(temp_month)/len(temp_month))
    #     #             average["year"] = year

        
    #     # self.monthly['average'] = average
    #     # self.monthly['year'] = average['year']
    #     # average = self.convert_to_list(self.monthly['average'])
    #     # self.monthly['average'] = average

    #     # return self.monthly


    # def get_minimum(self, year_filter="2022"):
    #     minimum = {}
    #     for date in self.months:
    #         minimum[date] = 0
    #         # items =  self.product.get_products(self.category, year_filter)
    #         items =  self.product.get_products_with_aggregate(self.category, date, year_filter)
    #         print(items)
    #         temp_month = []
    #     #     for item in items:
    #     #         month = self.convert_month(item['extraction_date'])
    #     #         year = self.convert_year(item['extraction_date'])
    #     #         price = item['price']
    #     #         if self.price_invalid(price):
    #     #             continue
    #     #         if month == date:
    #     #             temp_month.append(price)
    #     #             minimum['category'] = self.category
    #     #             minimum[date] = min(temp_month)
    #     #             minimum["year"] = year


    #     # self.monthly['minimum'] = minimum
    #     # self.monthly['year'] = minimum['year']
    #     # minimum = self.convert_to_list(self.monthly['minimum'])
    #     # self.monthly['minimum'] = minimum
        

    #     # return self.monthly


    # def get_maximum(self, year_filter="2022"):
    #     maximum = {}
    #     for date in self.months:
    #         maximum[date] = 0
    #         # items =  self.product.get_products(self.category, year_filter)
    #         items =  self.product.get_products_with_aggregate(self.category, date, year_filter)
    #         print(items)
    #         temp_month = []
    #     #     for item in items:
    #     #         month = self.convert_month(item['extraction_date'])
    #     #         year = self.convert_year(item['extraction_date'])
    #     #         price = item['price']
    #     #         if self.price_invalid(price):
    #     #             continue
    #     #         if month == date:
    #     #             temp_month.append(price)
    #     #             maximum['category'] = self.category
    #     #             maximum[date] = max(temp_month)
    #     #             maximum["year"] = year



    #     # self.monthly['maximum'] = maximum
    #     # self.monthly['year'] = maximum['year']
    #     # maximum = self.convert_to_list(self.monthly['maximum'])
    #     # self.monthly['maximum'] = maximum

    #     # return self.monthly

    

    def convert_to_list(self, average: dict):
        result = map(lambda month: average[month], self.months)
        return list(result)
                