# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ProductItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    colors = Field() #need additional processing
    gender = Field()
    brand = Field() #
    price = Field() #
    salePrice = Field() #
    sizesInv = Field() #
    name = Field() #
    colorwayName = Field() #<- look at this
    description = Field()
    imgs = Field() #
    displayPic = Field() #
    productType = Field() #
    style = Field() #ie: boots-----------------
    pageUrl = Field() #
    _id: Field() #For MongoDB querying
    '''
    Worry abotu after: Structure of _id: storeName_locationId_productName_variantName

    '''
