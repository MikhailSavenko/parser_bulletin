import scrapy


class BulletinItem(scrapy.Item):
    file_path = scrapy.Field()
    date = scrapy.Field()
