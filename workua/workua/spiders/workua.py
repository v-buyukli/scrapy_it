import scrapy


def extract_location(response):
    raw_location = response.xpath(
        "//span[@class='glyphicon glyphicon-map-marker text-default glyphicon-large']/following-sibling::text()"
    ).get()
    location = raw_location.strip() if raw_location else None
    return location


def extract_description(response):
    raw_description = response.xpath('//div[@id="job-description"]//text()').getall()
    description = "\n".join(desc.strip() for desc in raw_description)
    return description


def extract_salary(response):
    raw_salary = response.xpath(
        "//span[@class='glyphicon glyphicon-hryvnia text-default glyphicon-large']/following-sibling::b[@class='text-default']/text()"
    ).get()
    salary = (
        (
            raw_salary.replace("\u202f", "")
            .replace("\u2009", "")
            .replace(" грн", "")
            .strip()
        )
        if raw_salary
        else None
    )
    if salary:
        salary_split = salary.split("–")
        salary_min = salary_split[0] if salary_split else None
        salary_max = salary_split[1] if len(salary_split) > 1 else None
    else:
        salary_min = salary
        salary_max = None
    return salary_min, salary_max


class VacanciesSpider(scrapy.Spider):
    name = "vacancies"
    start_urls = ["https://www.work.ua/jobs-python/"]

    def parse(self, response):
        cards_xpath = "/html/body/section/div/div[3]/div[1]/div[3]/div[*]"
        cards = response.xpath(cards_xpath)

        for card in cards:
            vacancy_data = card.xpath("./h2/a")
            if not vacancy_data:
                continue
            vacancy_href = vacancy_data.attrib["href"]
            yield response.follow(vacancy_href, callback=self.parse_vacancy)

        next_page = response.xpath('//ul[has-class("pagination")]/li')
        if next_page:
            try:
                next_page = next_page[-1].xpath("./a").attrib["href"]
                yield response.follow(next_page, callback=self.parse)
            except KeyError:
                return None

    def parse_vacancy(self, response):
        title = response.css("h1::text").get().replace("\ufeff", "")
        url = response.url
        location = extract_location(response)
        salary_min, salary_max = extract_salary(response)
        description = extract_description(response)

        yield {
            "title": title,
            "url": url,
            "location": location,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "description": description,
        }
