import scrapy


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    start_urls = ["https://www.work.ua/jobs-python/"]

    def parse(self, response):
        pass
