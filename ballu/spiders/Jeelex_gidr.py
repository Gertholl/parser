import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from selenium import webdriver
import re
import requests
import time
from scrapy_selenium import SeleniumRequest


class AbiturLoader(ItemLoader):
    default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "pidr"
    # allowed_domains = ["luis.ru/catalog/videonablyudenie/"]
    # start_urls = ['https://www.jeelex-pumps.ru/shop/expansion-tanks/',
    #               'https://www.jeelex-pumps.ru/shop/expansion-tanks/page-2/',
    #
    #
    #             ]
    # start_urls = ['https://www.jeelex-pumps.ru/shop/pumps/',
    #               'https://www.jeelex-pumps.ru/shop/pumps/page-2/',
    #               'https://www.jeelex-pumps.ru/shop/pumps/page-3/',
    #               'https://www.jeelex-pumps.ru/shop/pumps/page-4/',
    #               'https://www.jeelex-pumps.ru/shop/pumps/page-5/',
    #               'https://www.jeelex-pumps.ru/shop/pumps/page-6/',
    #               'https://www.jeelex-pumps.ru/shop/pumps/page-7/',
    #               ]
    start_urls = ['https://www.jeelex-pumps.ru/shop/gidroakkumulyator/',
                  'https://www.jeelex-pumps.ru/shop/gidroakkumulyator/page-2/',
                  'https://www.jeelex-pumps.ru/shop/gidroakkumulyator/page-3/',

    ]
    rules = {
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="item-title"]/a'), allow="https://www.jeelex-pumps.ru/shop/gidroakkumulyator/*"), follow=True,callback="parse_item"),
    }


    def parse_item(self,response):
        global title
        title = response.xpath('//h1/text()').get()
        if title != None:
                names = ['Наименование',
                         'Наименование артикула',
                         'Код артикула',
                         'Валюта',
                         'ID артикула',
                         'Цена',
                         'Доступен для заказа',
                         'Зачеркнутая цена',
                         'Закупочная цена',
                         'В наличии',
                         'В наличии @Красноярск',
                         'ID товара',
                         'Краткое описание',
                         'Наклейка',
                         'Статус',
                         'Тип товаров',
                         'Теги',
                         'Облагается налогом',
                         'Заголовок',
                         'META Keywords',
                         'META Description',
                         'Ссылка на витрину',
                         'Адрес видео на YouTube или Vimeo',
                         'Дополнительные параметры','Производитель','Габариты (В х Ш х Г)','Объем (литры)','Материал корпуса','Диаметр присоединения',
                         'Макс. рабочее давление, атм.','Температурный диапазон воды, °C']
                harks = [title, '', '',
                         '', '', '',
                         '', '', '',
                         '', '', '',
                         '', '', '',
                         '', '', '',
                         '', '', '',
                         '', '', '','Jeelex'
                         ]
                # self.driver = webdriver.Chrome('C:\\Users\gerth\\ballu\\ballu\\chromedriver.exe')
                # self.driver.get(response.request.url)
                # try:
                #     self.driver.find_element_by_xpath('//div[@class="mail-modal__close"]').click()
                #     time.sleep(1)
                # except:
                #     print('good')

                # self.driver.find_element_by_xpath('//div[@class="tabs_section"]//li[3]').click()
                s = response.xpath('//td[@class="char_name"]/span/text()').getall()
                z = response.xpath('//td[@class="char_value"]/span/text()').getall()


                name_and_harks = dict(zip(s,z))
                # try:
                #     harks.append(name_and_harks['Высота'].strip('\nмм') + ' х ' + name_and_harks['Ширина'].strip('\nмм') + ' х ' + name_and_harks['Длина'].strip('\nмм') + ' мм')
                # except KeyError:
                #     harks.append('')
                #
                # try:
                #     try:
                #         if name_and_harks['Емкость']:
                #             harks.append(
                #                 re.findall(r'\d\w', name_and_harks['Емкость'])[0] + ' л')
                #     except IndexError:
                #         harks.append('')
                # except KeyError or IndexError:
                #     harks.append('')
                #
                # try:
                #     if name_and_harks['Материал фланцевого соединения'] == 'пластиковый':
                #         harks.append('Пластик')
                #     elif name_and_harks['Материал фланцевого соединения'] == 'металлический':
                #         harks.append('Металл')
                #     else:
                #         harks.append('')
                # except KeyError or IndexError:
                #     harks.append('')
                #
                # try:
                #     if name_and_harks['Присоединительный размер'] == '1 дюйм (25 мм)':
                #         harks.append('1" (25 мм)')
                #     elif name_and_harks['Присоединительный размер'] == '1 1/4 дюйма (32 мм)':
                #         harks.append('1 1/4" (32 мм)')
                #     elif name_and_harks['Присоединительный размер'] == '3/4 дюйма (19 мм)':
                #         harks.append('3/4" (20 мм)')
                #     else:
                #         harks.append('')
                # except KeyError or IndexError:
                #     harks.append('')
                #
                # # try:
                # #     if name_and_harks['Компоновка'] == 'вертикальная':
                # #         harks.append('Вертикальные')
                # #     elif name_and_harks['Компоновка'] == 'горизонтальная':
                # #         harks.append('Горизонтальные')
                # # except KeyError or IndexError:
                # #     harks.append('')
                # try:
                #     a = name_and_harks['Максимальное давление']
                #     if ' атмосферы' in a:
                #         harks.append(a.replace(' атмосферы',''))
                #     else:
                #         harks.append(a.replace(' атмосфер',''))
                # except IndexError or KeyError:
                #     harks.append('')
                # try:
                #     harks.append(name_and_harks['Рабочая температура теплоносителя'].strip('от').strip(' °C').replace('до','—').replace('+','').replace('º','').replace('  ',''))
                # except KeyError:
                #     harks.append('')
                n_h = dict(zip(names,harks))
                # self.driver.close()
                self.parse_img(response)
                yield n_h

    def parse_img(self,response):
        b_url = 'https://www.jeelex-pumps.ru/'
        img = response.xpath('//div[@class="slides"]//img/@src').get()
        print(img)
        try:
            name = title.replace('/','')
        except:
            pass
        r = requests.get(b_url+str(img))
        out = open('C:\\Users\\gerth\\OneDrive\\Документы\\DATABASE\\Jeelex\\Gidr\\'+name+'.jpg', 'wb')
        out.write(r.content)
        out.close()

