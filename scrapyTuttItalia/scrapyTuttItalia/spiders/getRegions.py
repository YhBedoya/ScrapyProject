import scrapy
from scrapy.crawler import CrawlerProcess

class tuttItaliaRegions(scrapy.Spider):
    name = "urlCollecter"
    nameFile = "regionsUrl.csv"

    custom_settings = {
        "FEEDS": {f"./urls/{nameFile}": {"format": "csv",
                                                         'overwrite': True}},
        "DOWNLOAD_DELAY": 0.5
    }

    #rotate_user_agent = True

    start_urls = ["https://www.tuttitalia.it/italia/"]

    def parse(self, response):

        hrefs = response.css("td.kr a")

        for href in hrefs:
                yield {"urls": f"https://www.tuttitalia.it{href.attrib['href']}"}

process = CrawlerProcess()
process.crawl(tuttItaliaRegions)
process.start()