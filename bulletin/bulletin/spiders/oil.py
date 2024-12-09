import scrapy
import re
from pathlib import Path
from bulletin.items import BulletinItem
from scrapy.exceptions import CloseSpider


BASE_DIR = Path(__file__).resolve().parent.parent


class OilSpider(scrapy.Spider):
    name = "oil"
    allowed_domains = ["spimex.com"]
    start_urls = ["https://spimex.com/markets/oil_products/trades/results/"]

    def parse(self, response):
        hrefs = response.css('.accordeon-inner .accordeon-inner__wrap-item .accordeon-inner__header a::attr(href)').re(r'/upload/reports/oil_xls/.*\.xls')
        for href in hrefs:
            yield response.follow(href, callback=self.save_file)

        next_page = response.css('li.bx-pag-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def save_file(self, response):
        pattern = r'oil_xls_(202.)'
        url = response.url
        match = re.search(pattern, url)
        year = match.group(1)
        print(year)

        pattern_date = r'oil_xls_(\d{8})'
        match_date = re.search(pattern_date, url)
        date = match_date.group(1)
        print(date)

        if int(year) >= 2023:
            name = url.split('/')[-1]
            download = BASE_DIR / 'download'
            download.mkdir(exist_ok=True)
            filename = download / name
            with open(filename, mode='wb') as f:
                f.write(response.body)
            yield BulletinItem(file_path=filename, date=date)
        else:
            raise CloseSpider('Year stop')
