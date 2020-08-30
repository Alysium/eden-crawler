import scrapy
import re
from edenCrawler.items import ProductItem


class HavenSpider(scrapy.Spider):
    name = 'haven'
    allowed_domains = ['shop.havenshop.com']
    start_urls = ['https://shop.havenshop.com/collections/footwear?view=all']


    def getSizeInv(self, productBox):
        """
        Function get size inventory from product box
        :param arg: productBox Selector class type
        :return: returns productBox dict type
        """
        sizesSelectors = productBox.css("p.product-sizes>span")
        sizes = {}
        for sizesSelector in sizesSelectors:
            inv = int(sizesSelector.attrib['data-stock'])
            if inv != 0:
                sizes[sizesSelector.css("::text").get().strip().replace(".", "_")] = inv
        return sizes

    def getPrice(self, productBox):
        """
        Function gets price from product box
        :param arg: productBox Selector class type
        :return: returns price and salePrice int type
        """
        priceSelector = productBox.css("p.product-price")
        salePrice = ''
        price = ''
        if priceSelector.css("del") != []:
            price = priceSelector.css("del::text").get()
            salePrice = priceSelector.css("span.highlight::text").get()
            salePrice = int(''.join(filter(str.isdigit, salePrice)))
        else:
            price = priceSelector.css("::text").get().strip()
        price = int(''.join(filter(str.isdigit, price))) #remove none number characters        
        return price, salePrice

    def getName(self, productBox):
        """
        Function gets name from product box
        :param arg: productBox Selector class type
        :return: returns name str type
        """
        name = productBox.css("p.product-card-name::text").get().strip()
        #remove collab "x" if required
        if name[:2] == "x ":
            name = name[2:]
        return name

    def getBrand(self, productBox):
        """
        Function gets brand name from product box
        :param arg: productBox Selector class type
        :return: returns brand str type (all lowercase)
        """
        return productBox.css("p.product-card-brand::text").get().lower()


    def parseProductPage(self, response):
        '''
        Function to parse productPage
        - gets pic links
        - gets gets item description
        :param: response of downloaded html page
        
        '''

        item = response.meta['item']

        item['description'] = response.css('[id="accordion-description"]>div>p::text').get()
        imgs = response.css('[id="product-gallery-main"]>div>img::attr(src)').getall()
        item['displayPic'] = imgs.pop(0)
        item['imgs'] = imgs
        

        yield item

    def productPageError(self, response):
        print("An error has occured getting the product page here:", response.url)

    def parse(self, response):
        #this returns string of html components -> can do string manipulation, but not optimal
        #productBoxes = response.xpath('//a[contains(@class,"product-card")]').getall()        
        hrefs = response.css("a.product-card::attr(href)").getall()

        for i,product in enumerate(response.css("a.product-card")[:10]):
            item = ProductItem()
            #loops for each item seen in the footwear product car
            sizes = self.getSizeInv(product)
            if sizes == {}:
                continue
            else:
                item['sizesInv'] = sizes
            item['brand'] = self.getBrand(product)
            item['price'], item['salePrice'] = self.getPrice(product) 
            item['name'] = self.getName(product)
            item['pageUrl'] = hrefs[i]
            item['gender'] = 'mens' #gender assumed to be mens


            productClasses = re.sub('\n+', ' ',re.sub(" +", '-', product.attrib['class'])).split(" ")

            item['productType'] = productClasses[1]

            yield scrapy.Request(hrefs[i],\
                callback=self.parseProductPage, errback=self.productPageError,\
                meta={'item': item})
