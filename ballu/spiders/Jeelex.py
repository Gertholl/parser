import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader

import time
import requests
import re



# class AbiturLoader(ItemLoader):
#     default_output_processor = Identity()


class AbiturlistSpider(CrawlSpider):
    name = "pumps"
    # allowed_domains = ["https://www.jeelex-pumps.ru/shop/pumps/*"]
    start_urls = ['https://www.jeelex-pumps.ru/shop/pumps/',
                  'https://www.jeelex-pumps.ru/shop/pumps/page-2/',
                  'https://www.jeelex-pumps.ru/shop/pumps/page-3/',
                  'https://www.jeelex-pumps.ru/shop/pumps/page-4/',
                  'https://www.jeelex-pumps.ru/shop/pumps/page-5/',
                  'https://www.jeelex-pumps.ru/shop/pumps/page-6/',
                  'https://www.jeelex-pumps.ru/shop/pumps/page-7/',
                ]
    links = []
    rules = {
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="item-title"]/a'), allow="https://www.jeelex-pumps.ru/shop/pumps/*"), follow=True,callback="parse_item"),
    }

    def parse_item(self,response):
            global title
            title = response.xpath('//h1/text()').get()
            if title != '':
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
                         'Дополнительные параметры','Производитель',
                         'Вид','Конструкция насоса','Материал корпуса','Доп. Функции','Максимальный напор','Габариты (В х Ш х Г)',
                         'Напряжение','Класс пылевлагозащищенности','Диаметр присоединения','Допустимая температура, ºС','Мощность','Емкость гидроаккумулятора',
                         'Максимальная высота всасывания','Длина кабеля','Глубина погружения','Уровень шума (дБ)','Производительность (л/мин)','Допустимый диаметр твёрдых частиц'
                         ]
                harks = [title,'','',
                         '','','',
                         '','','',
                         '','','',
                         '','','',
                         '','','',
                         '','','',
                         '', '', '','Jeelex'
                         ]


                s = response.xpath('//td[@class="char_name"]/span/text()').getall()


                z = response.xpath('//td[@class="char_value"]/span/text()').getall()

                name_and_harks = dict(zip(s,z))
                try:
                #Вид
                    if name_and_harks['Тип погружного насоса'] == 'колодезный':
                        harks.append('Для колодца')
                    elif  name_and_harks['Тип погружного насоса'] == 'дренажный':
                        harks.append('Дренажные')
                    elif name_and_harks['Тип погружного насоса'] == 'скважинный':
                        harks.append('Для скважины')
                    elif name_and_harks['Тип погружного насоса'] == 'фекальный':
                        harks.append('Фекальные')
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                try:
                #Конструкция насоса
                    if name_and_harks['Механизм насоса'] == 'центробежный':
                        harks.append('Центробежные')
                    elif name_and_harks['Механизм насоса'] == 'вибрационный':
                        harks.append('Вибрационные')
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                try:
                #Материал корпуса
                    if name_and_harks['Материал корпуса насоса'] == 'нержавеющая сталь':
                        harks.append('Нержавеющая сталь')
                    elif name_and_harks['Материал корпуса насоса'] == 'пластик':
                        harks.append('Пластик')
                    elif name_and_harks['Материал корпуса насоса']== 'чугун':
                        harks.append('Чугун')
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                try:
                #Дополнительные функции
                    if name_and_harks['Дополнительные функции'] == 'защита от сухого хода':
                        harks.append('Защита от сухого хода')
                    elif name_and_harks['Дополнительные функции'] == 'плавный пуск':
                        harks.append('')
                    elif name_and_harks['Дополнительные функции'] == 'повышение давления':
                        harks.append('Высокого давления')
                    elif name_and_harks['Дополнительные функции'] == 'защита от перегрева':
                        harks.append('Защита от перегрева')
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                try:
                    harks.append(name_and_harks['Максимальный напор'])
                except KeyError:
                    harks.append('')
                #Габариты
                try:
                    harks.append(name_and_harks['Высота'].strip('\nмм') + ' х ' + name_and_harks['Ширина'].strip('\nмм') + ' х ' + name_and_harks['Длина'].strip('\nмм') + ' мм')
                except KeyError:
                    harks.append('')
                #Напряжение
                try:
                    harks.append('220 В')
                except KeyError:
                    harks.append('')

                #Класс пылевлагозащищенности
                try:
                    if name_and_harks['Уровень защиты']:
                        harks.append(name_and_harks['Уровень защиты'])
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                #Диаметр присоединения
                try:
                    if name_and_harks['Подсоединительный размер у насоса'] == '1 дюйм':
                        harks.append('1" (25 мм)')
                    elif name_and_harks['Подсоединительный размер у насоса'] == '1 1/4 дюйма':
                        harks.append('1 1/4" (32 мм)')
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                #Допустимая температура, ºС
                try:
                    harks.append(name_and_harks['Температура перекачиваемой воды'].strip('от').strip(' °C').replace('до','—').replace('+',''))
                except KeyError:
                    harks.append('')

                #Мощность потребляемая
                try:
                    if name_and_harks['Мощность потребляемая']:
                        harks.append(name_and_harks['Мощность потребляемая'])
                    else:
                        harks.append('')
                except KeyError:
                    harks.append('')
                #Емкость гидроаккумулятора
                try:
                    if name_and_harks['Емкость гидроаккумулятора']:
                        harks.append(re.findall(r'\d\w',name_and_harks['Емкость гидроаккумулятора'])[0])
                    else:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')
                #Максимальная глубина всасывания
                try:
                    try:
                        if name_and_harks['Максимальная глубина всасывания']:
                             harks.append(re.findall(r'\d\w', name_and_harks['Максимальная глубина всасывания'])[0]+' м')
                    except IndexError:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')
                #Длина кабеля
                try:
                    try:
                        if name_and_harks['Длина кабеля']:
                            harks.append(re.findall(r'\d\w', name_and_harks['Длина кабеля'])[0]+' м')
                    except IndexError:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')
                #Глубина погружения
                try:
                    try:
                        if name_and_harks['Глубина погружения под воду']:
                            harks.append(re.findall(r'\d\w', name_and_harks['Глубина погружения'])[0]+' м')
                    except IndexError:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')
                #Уровень шума
                try:
                    try:
                        if name_and_harks['Уровень шума']:
                            harks.append(re.findall(r'\d\w', name_and_harks['Уровень шума'])[0])
                    except IndexError:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')
                try:
                    try:
                        if name_and_harks['Максимальный расход']:
                            harks.append(re.findall(r'\d\w', name_and_harks['Максимальный расход'])[0]+ ' л')
                    except IndexError:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')
                try:
                    try:
                        if name_and_harks['Размер фильтруемых частиц']:
                            harks.append(name_and_harks['Размер фильтруемых частиц'])
                    except IndexError:
                        harks.append('')
                except KeyError or IndexError:
                    harks.append('')

                n_h = dict(zip(names,harks))

                try:
                    self.parse_img(response)
                except:
                    pass
                yield n_h

    def parse_img(self, response):
        b_url = 'https://www.jeelex-pumps.ru/'
        img = response.xpath('//div[@class="slides"]/li[@id="photo-0"]//img/@src').get()
        print(img)
        r = requests.get(b_url+str(img))
        out = open(f'C:\\Users\\gerth\\OneDrive\\Документы\\DATABASE\\Jeelex\\Nas\\{title}.jpg','w')
        out.write(r.content)
        out.close()