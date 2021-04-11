from pymongo import MongoClient

class dbBrainly():
    client = MongoClient('mongodb+srv://adjipras:skripsi@cluster0.j6djb.mongodb.net/brainly?retryWrites=true&w=majority')
    database = 'brainly'

    def insert_url(self, collection, url):
        db  = self.client[self.database]
        db[collection].insert_one({'url':url})

    def get_all_urls(self, collection):
    	db = self.client[self.database]
    	collection = db['bahasa_indonesia']
    	result = collection.find()
    	return result

    def insert_info(self, collection, data):
    	db = self.client[self.database]
    	db[collection].insert_one(data)

    def check_docs(self, collection, url):
    	db = self.client[self.database]
    	result = db[collection].find_one({'url': url})
    	if result is None:
    		value = False
    	else: 
    		value = True
    	return value
