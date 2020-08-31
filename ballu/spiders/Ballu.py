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
    name = "ballu"
    # allowed_domains = ["luis.ru/catalog/videonablyudenie/"]
    start_urls = ['https://www.ballu.ru/catalog/tekhnika_dlya_doma_i_ofisa/obogrevateli/']
    rules = {
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="series-list-item"]//a'), ), follow=True,),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="item-content"]//a'), ), follow=True, ),
        Rule(LinkExtractor(restrict_xpaths=('//table[@class="content-table"]//td[1]//a'), ), follow=True, callback='parse_item'),
    }


    def parse_item(self,response):
        name = response.xpath('//div[@class="product-name"]//h1[@itemprop="name"]/text()').get()
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
            try:
                hr = self.driver.find_element_by_xpath('//div[@class="tabs-holder low"]//li[2]')
                if hr.text() == "Технические характеристики":
                    hr.click()
                else:
                    self.driver.find_element_by_xpath('//div[@class="tabs-holder low"]//li[1]')
            except:
                pass
            name_hark = response.xpath('//tr[not(@class="group-props")]//td[1]/span/text()').getall()
            znach_harl = response.xpath('//tr[not(@class="group-props")]//td[2]/span/text()').getall()
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

