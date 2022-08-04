import certifi
import dns.resolver
from pymongo import MongoClient
from .products import Products


class Graphs():
    def __init__(self):
        self.client = MongoClient("mongodb://localhost", 27017)
        # self.client = MongoClient("mongodb+srv://cpartproject:cparts1030@cluster0.zkpdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client['graphDB']
        self.monthly = self.db['monthly']
        self.category = self.db['category']
        self.product = Products()


    def add_graph_data(self, product: dict):
        if product.get('_id'):
            del product['_id']
        print("\nInserting ", product)
        self.monthly.insert_one(product)
        print("done!")


    def add_category(self, product: dict):
        if product.get('_id'):
            del product['_id']
        print("\nInserting ", product)
        self.category.insert_one(product)
        print("done!")


    def refresh_graph(self):
        self.monthly.drop()


    def refresh_category(self):
        self.category.drop()

    # def get_average_cpu(self, month):
    #     self.product.cpu.remove({"price": ""})
    #     return self.product.cpu.aggregate([
    #         {
    #             "$project": {
    #                 "monthly": {
    #                     "$month": {
    #                         "$dateFromString": {
    #                             "dateString": "$extraction_date"
    #                         }
    #                     }
    #                 },
    #                 "extractionDate": "$extraction_date",
    #                 "itemPrice": "$price"
    #             }
    #         },
    #         {
    #             "$match": {
    #                 "monthly": month
    #             }
    #         },
    #         {
    #             "$group": {
    #                 "_id": "$monthly",
    #                 "average": {
    #                     "$avg": "$itemPrice"
    #                 }
    #             }
    #         }
    #     ])