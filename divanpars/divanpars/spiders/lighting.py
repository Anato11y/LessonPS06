import scrapy
import csv

class LightingSpider(scrapy.Spider):
    name = "lighting"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/irkutsk/category/svetilniki"]

    def __init__(self, *args, **kwargs):
        super(LightingSpider, self).__init__(*args, **kwargs)
        # Открываем CSV файл для записи данных
        self.file = open('lighting.csv', mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        # Записываем заголовки столбцов
        self.writer.writerow(['Name', 'Price', 'URL'])

    def parse(self, response):
        # Парсим блоки с товарами
        divans = response.css('div._Ud0k')
        for divan in divans:
            # Извлечение данных с проверкой на наличие информации
            name = divan.css('div.lsooF span::text').get()
            price = divan.css('div.pY3d2 span::text').get()
            url = divan.css('a').attrib.get('href')

            if name and price and url:
                # Очищаем данные от лишних пробелов
                name = name.strip()
                price = price.strip()
                url = response.urljoin(url)

                # Записываем данные в CSV файл
                self.writer.writerow([name, price, url])

        # Пагинация: проверяем наличие следующей страницы и продолжаем парсинг
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def close(self, reason):
        # Закрываем файл после завершения работы паука
        self.file.close()
