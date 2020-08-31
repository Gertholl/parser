import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
import re
from scrapy.selector import Selector
from selenium import webdriver
import time
from scrapy_selenium import SeleniumRequest
import requests

class AbiturLoader(ItemLoader):
    default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "pi"
    links = []
    with open('C:\\Users\\gerth\\ballu\\ballu\\ballu\\фильтры.txt', 'r') as f:
        for i in f:
            links.append('https://shop.geizer.com/search/?q={}&s='.format(i.strip("\n")))
    start_urls = links
    rules = {
        Rule(LinkExtractor(restrict_xpaths=('//tr[@class="even"]//td[4]//a'),), follow=True),
        Rule(LinkExtractor(allow='https://shop.geizer.com/catalog/*'), callback='parse_items')
    }

    def parse_items(self,response):
            global title, art, price, vitr
            title = response.xpath('//*[@id="content"]/article/h1/text()').get()
            price = response.xpath('//dl[@class="cost"]//dd/text()').get()
            ul = response.xpath("//div[@id ='tab2']/ul/li/text()").getall()
            a = response.xpath('//div[@class="product_article"]/text()').get()
            art = re.findall(r'\d+', response.request.url)

            ves = []
            size = []
            productivity = []
            temp = []
            dav = []
            for li in ul:
                if "кг" in li:
                    a = li.split(' ')
                    if a[-1] == "кг":
                        ves.append(a[-2] + " кг")
                    else:
                        ves.append('')
                elif "Масса" in li:
                    a = re.findall(r"\d+[.,]\d+|\d+", "li")
                    if len(a) == 0:
                        ves.append('')
                    if len(a) == 1:
                        ves.append(a[0] + " кг")

            for li in ul:
                if "размер" in li:
                    b = re.findall(r'\d+\х\d+\х\d+', li.lower())
                    if len(b) == 1:
                        size.append(b[0] + " мм")
                    if len(b) == 0:
                        size.append('')
                elif "Габар" in li:
                    b = re.findall(r'\d+\х\d+', li.lower())
                    if len(b) == 1:
                        size.append(b[0] + " мм")
                    if len(b) == 0:
                        size.append('')

            for li in ul:
                if "Производительность" in li:
                    c = re.findall(r"\d+[.,]\d+|\d+", li)
                    if len(c) == 0:
                        productivity.append('')
                    elif len(c) >= 2:
                        productivity.append(max(c))
                    else:
                        productivity.append(c[0])
                elif "скорость фильтрации" in li:
                    c = re.findall(r"\d+[.,]\d+|\d+", li)
                    if len(c) == 0:
                        productivity.append('')
                    elif len(c) >= 2:
                        productivity.append(max(c))
                    else:
                        productivity.append(c[0])

            for li in ul:
                if "°С" in li:
                    a = re.findall(r"\d+[.,]\d+|\d+", li)
                    if len(a) == 1:
                        temp.append(a[0] + " °С")
                    elif len(a) >= 2:
                        temp.append(max(a) + " °С")
                    elif len(a) == 0:
                        temp.append('')

            for li in ul:
                if "атм." in li:
                    a = re.findall(r"\d+[.,]\d+|\d+", li)
                    if len(a) == 1:
                        dav.append(a[0] + " атм.")
                    elif len(a) >= 2:
                        dav.append(max(a) + " атм.")
                    else:
                        dav.append('')
            try:
                if "12 л" in title:
                    obem = "12 л"
                elif "8 л" in title:
                    obem = "8 л"
                else:
                    obem = ""
            except:
                obem = None

            for li in ul:
                if "Артикул" in li:
                    art = li.strip("Артикул: ")
            try:
                cr_op = response.xpath("//ul/p/text()").get()
            except:
                cr_op = None
            try:
                vitr = response.request.url.split('/')
            except:
                pass
            data = {
                'Наименование': title,
                'Наименование артикула': '',
                'Код артикула': art,
                'Валюта': '',
                'ID артикула': '',
                'Цена': price,
                'Доступен для заказа': '',
                'Зачеркнутая цена': '',
                'Закупочная цена': '',
                'В наличии': '',
                'В наличии @Красноярск': '',
                'ID товара': '',
                'Краткое описание': cr_op,
                'Наклейка': '',
                'Статус': '',
                'Тип товаров': '',
                'Теги': '',
                'Облагается налогом': '',
                'Заголовок': '',
                'META Keywords': '',
                'META Description': '',
                'Ссылка на витрину': vitr[-2],
                'Адрес видео на YouTube или Vimeo': '',
                'Дополнительные параметры': '',
                'Производитель': '',
                'Вес': ves,
                "Габариты (В х Ш х Г)": size,
                "Макс. производительность л/час": productivity,
                "Макс. температура воды": temp,
                "Давление": dav,
                "Объем": obem,
                "URL": response.request.url
            }
            self.parse_img(response)
            yield data

    def parse_img (self,response):
        try:
                    z = response.request.url.split('/')
                    b_url = 'https://shop.geizer.com/'
                    img = response.xpath('//div[@class="photo"]//img/@src').get()
                    r = requests.get(b_url + str(img))
                    out = open(f'D:\\Geizer\\фильтры\\{z[-2]}.jpg', 'wb')
                    out.write(r.content)
                    out.close()
        except:
            pass
