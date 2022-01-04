from pymongo import MongoClient

class Products():
    def __init__(self):
        self.client = MongoClient("mongodb+srv://cpartproject:cparts1030@cluster0.zkpdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # self.client = MongoClient("mongodb://localhost", 27017)
        self.db = self.client['productsDB']
        self.gpu = self.db['gpu']
        self.cpu = self.db['cpu']
        self.case = self.db['case']
        self.memory = self.db['memory']
        self.storage = self.db['storage']
        self.motherboard = self.db['motherboard']

    
    def add_product(self, product: dict, category: str):
        """ add user into mongoDB """
        if category == "gpu":
            self.gpu.insert_one(product)
        elif category == "cpu":
            self.cpu.insert_one(product)
        elif category == "case":
            self.case.insert_one(product)
        elif category == "memory":
            self.memory.insert_one(product)
        elif category == "storage":
            self.storage.insert_one(product)
        elif category == "motherboard":
            self.motherboard.insert_one(product)


    def find_product(self, query: dict, category:str):
        """ find account by query """
        if category == "gpu":
            return self.gpu.find_one(query)
        elif category == "cpu":
            return self.cpu.find_one(query)
        elif category == "case":
            return self.case.find_one(query)
        elif category == "memory":
            return self.memory.find_one(query)
        elif category == "storage":
            return self.storage.find_one(query)
        elif category == "motherboard":
            return self.motherboard.find_one(query)


    def get_products(self, category:str):
        """ find account by query """
        if category == "gpu":
            return self.gpu.find()
        elif category == "cpu":
            return self.cpu.find()
        elif category == "case":
            return self.case.find()
        elif category == "memory":
            return self.memory.find()
        elif category == "storage":
            return self.storage.find()
        elif category == "motherboard":
            return self.motherboard.find()


    def is_exist(self, query: dict, category: str):
        if category == 'gpu':
            if self.gpu.find(query).count() > 0:
                return True
            else:
                return False
        elif category == 'cpu':
            if self.cpu.find(query).count() > 0:
                return True
            else:
                return False
        elif category == 'case':
            if self.case.find(query).count() > 0:
                return True
            else:
                return False
        elif category == 'memory':
            if self.memory.find(query).count() > 0:
                return True
            else:
                return False
        elif category == 'storage':
            if self.storage.find(query).count() > 0:
                return True
            else:
                return False
        elif category == 'motherboard':
            if self.motherboard.find(query).count() > 0:
                return True
            else:
                return False


    def get_collection_by_category(self, category):
        if category == "gpu":
            return self.gpu
        elif category == "cpu":
            return self.cpu
        elif category == "case":
            return self.case
        elif category == "memory":
            return self.memory
        elif category == "storage":
            return self.storage
        elif category == "motherboard":
            return self.motherboard


    def filter_year(self, year, category):
        query = {"extraction_date": {"$regex": year}}
        collection = self.get_collection_by_category(category)
        return collection.find(query)


    def filter_by_marketplace(self, marketplace, category):
        query = {"marketplace": marketplace}
        collection = self.get_collection_by_category(category)
        return collection.find(query)

    
    # def get_average(self, category: str, date: str):
    #     if category == "gpu":
    #         return self.gpu.aggregate([{ 
    #         "$group": {
    #             "_id": 0, 
                
    #             "average": { "$avg": "$price" } 
    #         } 
    #         }])
    #     elif category == "cpu":
    #         return self.cpu.aggregate([{ 
    #         "$group": {
    #             "_id": 0, 
    #             "average": { "$avg": "$price" } 
    #         } 
    #         }])
    #     elif category == "case":
    #         return self.case.aggregate([{ 
    #         "$group": {
    #             "_id": 0, 
    #             "average": { "$avg": "$price" } 
    #         } 
    #         }])
    #     elif category == "memory":
    #         return self.memory.aggregate([{ 
    #         "$group": {
    #             "_id": 0, 
    #             "average": { "$avg": "$price" } 
    #         } 
    #         }])
    #     elif category == "storage":
    #         return self.storage.aggregate([{ 
    #         "$group": {
    #             "_id": 0, 
    #             "average": { "$avg": "$price" } 
    #         } 
    #         }])
    #     elif category == "motherboard":
    #         return self.motherboard.aggregate([{ 
    #         "$group": {
    #             "_id": 0, 
    #             "average": { "$avg": "$price" } 
    #         } 
    #         }])