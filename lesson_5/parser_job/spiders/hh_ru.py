import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://vladivostok.hh.ru/search/vacancy?area=22&area=88&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=Python&from=suggest_post"
    ]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)

        print('\n***********************\n%s\n***********************\n'%response.url)

    def parse_vacancy(self, response:HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        vacancy_url = response.url

        print('\n#######################\n%s\n#######################\n'%response.url)

        yield ParserJobItem(
            name=vacancy_name,
            salary=vacancy_salary,
            url=vacancy_url
        )
