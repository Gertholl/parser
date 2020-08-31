import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
# from selenium import webdriver
import time



class AbiturLoader(ItemLoader):
    default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "zzz"
    # allowed_domains = ["luis.ru/catalog/videonablyudenie/"]
    start_urls = ['http://www.home-comfort.ru/catalog/teplye_poly/infrakrasnaya_plenka/?PAGEN_1=1',
                  'http://www.home-comfort.ru/catalog/teplye_poly/infrakrasnaya_plenka/?PAGEN_1=2',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_maty/seriya_easy_fix_mat/?PAGEN_1=1',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_maty/seriya_easy_fix_mat/?PAGEN_1=2',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_maty/seriya_multi_size_mat/',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_maty/seriya_eco_mat/?PAGEN_1=1',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_maty/seriya_eco_mat/?PAGEN_1=2',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_sektsii/?PAGEN_1=1',
                  'http://www.home-comfort.ru/catalog/teplye_poly/nagrevatelnye_sektsii/?PAGEN_1=2',
                  'http://www.home-comfort.ru/catalog/teplye_poly/termoregulyatory/']
    rules = {
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="filt__catalog-item-img"]//a'), ), follow=True,callback='parse_item'),
    }


    def parse_item(self,response):
        name = response.xpath('//h1[@class="ProductLanding-content-header-title"]/text()').get()
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

            self.driver.find_element_by_xpath('//a[@class="Specs-toggle-btn"]').click()
            s = response.xpath('//li[@class="SpecList-item"]').getall()
            a = []
            for i in s:
                a.append(i.replace('</li>','').replace('<li class="SpecList-item">','').replace('<strong class="SpecList-item-label">','').replace('</strong>','').replace('\r','').replace('\t','').replace('\n',''))
            z = []
            for i in a:
                z.append(i.split(':'))

            name_and_harks = {'Модель': name.replace('\r','').replace('\t','').replace('\n',''),
                              'Url': response.request.url,}
            for i in z:
                name_and_harks[i[0]] = i[1]
            print(name_and_harks)
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

