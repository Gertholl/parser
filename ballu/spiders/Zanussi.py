import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium import webdriver
import time
from scrapy_selenium import SeleniumRequest


class AbiturLoader(ItemLoader):
    default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "zanussi"
    # allowed_domains = ["luis.ru/catalog/videonablyudenie/"]
    start_urls = ['http://www.easy-comfort.ru/catalog/vodonagrevateli/gazovye_vodonagrevateli/','http://www.easy-comfort.ru/catalog/vodonagrevateli/nakopitelnye_vodonagrevateli/']
    rules = {
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="section-tiles__img-link"]//a[@class="section-tiles__img-link"]'), ), follow=True,),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="catalog-plate__img-holder"]//a'), ), follow=True,callback='parse_item' ),
    }


    def parse_item(self,response):
        name = response.xpath('//div[@class="element-item__title"]//h1/text()').get()
        if name != None:
            names = ['Модель', 'Url']
            harks = [name.replace('\t','').replace('\n','').replace('\r',''), response.request.url]
            self.driver = webdriver.Chrome('C:\\Users\gerth\\ballu\\ballu\\chromedriver.exe')
            self.driver.get(response.request.url)
            try:
                self.driver.find_element_by_xpath('//div[@class="mail-modal__close"]').click()
                time.sleep(1)
            except:
                print('good')

            self.driver.find_element_by_xpath('//div[@class="element-item__table-button"]').click()
            name_hark = response.xpath('//div[@class="element-item__main-tech-wrap"]//table[@class="element-item__table"]//td[1]/text()').getall()
            znach_harl = response.xpath('//div[@class="element-item__main-tech-wrap"]//table[@class="element-item__table"]//td[2]/text()').getall()
            for i in name_hark:
                names.append(i.replace('\r','').replace('\t','').replace('\n',''))
            for i in znach_harl:
                harks.append(i.replace('\r','').replace('\t','').replace('\n',''))

            name_and_harks = dict(zip(names, harks))
            # name_and_harks = {'Модель': name.replace('\r','').replace('\t','').replace('\n',''),
            #                   'Url': response.request.url,}
            # for i in z:
            #     name_and_harks[i[0]] = i[1]
            # print(name_and_harks)
            self.driver.close()
            yield name_and_harks
    #
    # def btn_click(self, response):
    #         self.driver = webdriver.Chrome('C:\\Users\gerth\\ballu\\ballu\\chromedriver.exe')
    #         self.driver.get('http://www.home-comfort.ru/catalog/vodonagrevateli/')
    #         self.driver.find_element_by_xpath('//div[@class="CategoryNav__item CategoryNav__item_category"]//a').click()
    #         time.sleep(3)
    #         self.driver.find_element_by_xpath('//div[@class="filt__catalog-item-name"]//a').click()
    #         time.sleep(3)
    #         self.driver.find_element_by_xpath('//div[@class="filt__catalog-item-img"]//a').click()
    #         try:
    #             self.driver.find_element_by_xpath('//div[@class="mail-modal__close"').click()
    #         except:
    #             pass
    #

