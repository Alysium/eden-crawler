# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#Connecting pipeline to mongoDB: https://alysivji.github.io/mongodb-pipelines-in-scrapy.html

class EdencrawlerPipeline:

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri



    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI')
        )

    def open_spider(self, spider):
        #initialize spider and connect to MongoDB
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client.get_database() #will get the 'crawler-test' database

    def close_spider(self, spider): 
        self.client.close()


    def process_item(self, item, spider):
        #how to handle each item
        self.db['products'].insert(dict(item))
        print("Product added to MongoDB")
        return item