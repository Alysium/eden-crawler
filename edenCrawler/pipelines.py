# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import PySimpleGUI as sg
from PIL import Image
import requests
from io import BytesIO


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#import utils.constants as constants
from utils.constants import *
from utils.pipelineUtils import *

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


    '''
    will need to manually insert category here, since we need to check that entry
    exists in mongoDB or not
    '''
    def insert_category(self, item):
        displayPicURL = item['displayPic']
        response = requests.get(displayPicURL)
        img = convertImgToPNG(Image.open(BytesIO(response.content)))

        layout = [
            [sg.Text('Category Selector: Please Enter a Number based on the following for this image')],
            [sg.Text('Shoe name: %s' %(item['name']))],
            [sg.Image(data=img)],
            [sg.Text('0: Casual/Lifestyle/Sneakers, 1: Running, 2: Boots, 3: Sandals/Slippers, 4: Luxury, 5: Formal')],
            [sg.Text('Category (enter Integer):'), sg.InputText()], 
            [sg.Button('Ok'), sg.Button('Cancel')] 
        ]

        window = sg.Window('Category Selector', layout,resizable=True, finalize=True)
        style = False
        while True:
            event, inputVal = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                #possibly need to write some error out or something here such that it doesn't update the database
                break
            elif (event == 'Ok'):
                try:
                    if int(inputVal[1]) in variant_categories:
                        style = int(inputVal[1])
                        break
                except:
                    sg.Popup('Invalid Value Entered! Please enter the values given above')

        window.close()
        return style


    def process_item(self, item, spider):
        print("Pipeline Initiated")
        #how to handle each item
        #self.db['products'].insert(dict(item))

        '''
        Note: 
            When .find_one finds no entry, None is returned
        '''

        #_id = "placeholder"
        #entry = self.db['products'].find_one({"_id": _id})  
        entry = None #this is a placeholder for now
        if entry == None:
            #indicates that the product is a new product
            '''
            need to call to allow user to enter variant to manually fill
            '''
            itemStyle = self.insert_category(item)

            if itemStyle == False:
                print("Entry not entered into MongoDB due to cancelled Style Input")
                return item
            item['style'] = itemStyle
        else:
            #indicates that product can be found
            '''
            need to get entry and update it
            '''
            pass

        return item