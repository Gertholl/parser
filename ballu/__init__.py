# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

#//div[@class="bx_catalog_item"]//span[@class="your-price"] - цены
#//div[@class="bx_catalog_item_title"]//a/@title - наименование товра
#//div[@class="bx_catalog_item_title"]//a - ссылка на товар
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
rules = {
             Rule(LinkExtractor(restrict_xpaths=('//div[@class="CategoryNav__item CategoryNav__item_category"]//a')), follow=True,),#Перход из каталога
             Rule(LinkExtractor(restrict_xpaths=('//div[@class="filt__catalog-item-name"]//a')), follow=True,),#Выбор серии
             Rule(LinkExtractor(restrict_xpaths=('//div[@class="filt__catalog-item-name"]//a')), follow=True, ),
             Rule(LinkExtractor(restrict_xpaths=('//a[@role = "button"]')),follow = True, callback='chlen'),#Выбор товара

      }



