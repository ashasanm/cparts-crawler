import json
from pymongo import MongoClient


class DBExtract():
    def __init__(self, connection_type='local'):
        self.connection_type = connection_type
        self.client = self.set_connection()
        self.db = self.client['productsDB']
        self.gpu = self.db['gpu']
        self.cpu = self.db['cpu']
        self.case = self.db['case']
        self.memory = self.db['memory']
        self.storage = self.db['storage']
        self.motherboard = self.db['motherboard']
        self.category = ['gpu', 'cpu', 'motherboard', 'case', 'memory', 'storage']
    
    def set_connection(self):
        if self.connection_type == 'local':
            print("Connecting to local database...")
            return MongoClient("mongodb://localhost", 27017)
        if self.connection_type == 'live':
            print("Connecting to live database...")
            return MongoClient("mongodb+srv://cpartproject:cparts1030@cluster0.zkpdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        else:
            raise Exception("Invalid Connection Type")

    def extract_from_db(self, query=None):
        if not query:
            return {
                "gpu": self.gpu.find({}, {'_id': False }),
                "cpu": self.cpu.find({}, {'_id': False }),
                "case": self.case.find({}, {'_id': False }),
                "memory": self.memory.find({}, {'_id': False }),
                "storage": self.storage.find({}, {'_id': False }),
                "motherboard": self.motherboard.find({}, {'_id': False })
            }
        return {
                "gpu": self.gpu.find(query),
                "cpu": self.cpu.find(query),
                "case": self.case.find(query),
                "memory": self.memory.find(query),
                "storage": self.storage.find(query),~
                "motherboard": self.motherboard.find(query)
            }
        
    def cursor_to_list(self, cursor_obj):
        return list(cursor_obj)

    def save_to_json(self):
        data = self.extract_from_db()
        for cat in self.category:
            filename = "./extracted_db/{}/{}.json".format(self.connection_type, cat)
            cat_data = list(data.get(cat))
            with open(filename, 'w') as f:
                json.dump(cat_data, f)
            print(self.connection_type + " " + cat + " saved!")
        print("Done!")
    
    def insert_from_json(self, json_path, collection_name):
        with open(json_path) as file_json:
            data = json.load(file_json)
            print(f"Inserting {collection_name} data into database..")
            self.db[collection_name].insert_many(data)
            print("data imported")

if __name__ == '__main__':

    dbextract = DBExtract(connection_type='local')
    # dbextract.save_to_json()
    for cat in ['case', 'cpu', 'case', 'gpu', 'memory', 'motherboard', 'storage']:
            json_path = f"/Users/mymac/Documents/kuliah/semester_7/cparts/cparts-crawler/scripts/extracted_db/live/{cat}.json"
            dbextract.insert_from_json(json_path, collection_name=cat)