import scrapy
from scrapy.crawler import CrawlerProcess

class tuttItaliaRegions(scrapy.Spider):
    name = "urlCollecter"
    nameFile = "provincesUrl1.csv"

    custom_settings = {
        "FEEDS": {f"./urls/{nameFile}": {"format": "csv",
                                                         'overwrite': True}},
        "DOWNLOAD_DELAY": 0.5
    }

    #rotate_user_agent = True
    sourceFile = "./urls/regionsUrl.csv"
    with open(sourceFile) as f:
        urls = f.readlines()
        urls = [url[:-1].lower() for url in urls if url != "urls\n"]

    start_urls = urls

    def parse(self, response):

        hrefs = response.css("table.ut tr td a")

        for href in hrefs:
                yield {"urls": f"https://www.tuttitalia.it{href.attrib['href']}"}

process = CrawlerProcess()
process.crawl(tuttItaliaRegions)
process.start()