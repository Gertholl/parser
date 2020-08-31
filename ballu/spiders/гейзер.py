from typing import List, Any

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader

import time
import requests
import re


class AbiturLoader(ItemLoader):
    default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "zhopa"
    # allowed_domains = ["https://shop.geizer.com/"]
    
    start_urls = ["https://shop.geizer.com/catalog/gotovye_resheniya/","https://shop.geizer.com/catalog/gotovye_resheniya/?PAGEN_2=2","https://shop.geizer.com/catalog/gotovye_resheniya/?PAGEN_2=3"]
    links = []
    rules = {
        #Rule(LinkExtractor(restrict_xpaths='//div[@class="block-color block-blue"]//div[@class="block-white"]//ul[@class="list"]//span//a'), follow= True,callback='pagination'),
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='n-cat__card']//a[@class='n-cat__card-title']")),follow=True,callback='parse_item'),
    }

    def pagination(self,response):
        next_page_url = response.xpath('//div[@class="n-pagin__list"]//a[@class="n-pagin__item"]/@href').getall()
        for i in next_page_url:
            if i == 'javascript:void(0);':
                i = response.request.url
            if next_page_url:
                page_url = response.urljoin(i)
                print("Страница: ", page_url)
                yield scrapy.Request(url=page_url, callback=self.parse_cards)

    def parse_cards(self,response):
        card_page_url = response.xpath("//div[@class='n-cat__card']//a[@class='n-cat__card-title']/@href").getall()
        for i in card_page_url:
            if i:
                page_url = response.urljoin(i)
                yield scrapy.Request(url=page_url, callback=self.parse_item)

    def parse_item(self,response):

        global title, art, price
        title = response.xpath('//*[@id="content"]/article/h1/text()').get()
        price = response.xpath('//dl[@class="cost"]//dd/text()').get()
        ul = response.xpath("//div[@id ='tab2']/ul/li/text()").getall()
        ves = []
        size = []
        productivity = []
        temp = []
        dav = []
        for li in ul:
            if "кг" in li:
                a = li.split(' ')
                if a[-1] == "кг":
                    ves.append(a[-2]+" кг")
                else:
                    ves.append('')
            elif "Масса" in li:
                a = re.findall(r"\d+[.,]\d+|\d+","li")
                if len(a) == 0:
                    ves.append('')
                if len(a) == 1:
                    ves.append(a[0]+" кг")

        for li in ul:
            if "размер" in li:
                b = re.findall(r'\d+\х\d+\х\d+',li.lower())
                if len(b) == 1:
                    size.append(b[0]+" мм")
                if len(b) == 0:
                    size.append('')
            elif "Габар" in li:
                b = re.findall(r'\d+\х\d+',li.lower())
                if len(b) == 1:
                    size.append(b[0]+" мм")
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
                a = re.findall(r"\d+[.,]\d+|\d+",li)
                if len(a) == 1:
                    temp.append(a[0] + " °С")
                elif len(a) >= 2:
                    temp.append(max(a) + " °С")
                elif len(a) == 0:
                    temp.append('')


        for li in ul:
            if "атм." in li:
                a = re.findall(r"\d+[.,]\d+|\d+",li)
                if len(a) == 1:
                    dav.append(a[0]+" атм.")
                elif len(a) >= 2:
                    dav.append(max(a)+" атм.")
                else:
                    dav.append('')

        if "12 л" in title:
            obem = "12 л"
        elif "8 л" in title:
            obem = "8 л"
        else:
            obem =""

        for li in ul:
            if "Артикул" in li:
                art = li.strip("Артикул: ")
        # data = {"Наименование":title, "Вес": ves,"Габариты (В х Ш х Г)": size, 'Производительность': productivity, "Температура": temp, 'Давление': dav}
        # yield data


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
            'Краткое описание': '',
            'Наклейка': '',
            'Статус': '',
            'Тип товаров': '',
            'Теги': '',
            'Облагается налогом': '',
            'Заголовок': '',
            'META Keywords': '',
            'META Description': '',
            'Ссылка на витрину': '',
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
        yield data
        # self.parse_img(response)





    def parse_img(self, response):
        try:
            b_url = 'https://shop.geizer.com/'
            img = response.xpath('//div[@class="photo"]//img/@src').get()
            r = requests.get(b_url+str(img))
            out = open(f'D:\\Geizer\\gotovye_resheniya\\{title}.jpg','wb')
            out.write(r.content)
            out.close()
        except:
            pass