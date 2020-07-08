# author = 'F. Cigdem Tosun'

from scrapy.item import Item, Field  

class EksifeedItem(Item):
    url = Field()
    entry = Field()
    author = Field()
    date = Field()
    
