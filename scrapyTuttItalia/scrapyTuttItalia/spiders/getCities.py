import scrapy
from scrapy.crawler import CrawlerProcess

class tuttItaliaRegions(scrapy.Spider):
    name = "urlCollecter"
    nameFile = "citiesUrl2.csv"

    custom_settings = {
        "FEEDS": {f"./urls/{nameFile}": {"format": "csv",
                                                         'overwrite': True}},
        "DOWNLOAD_DELAY": 2
    }

    rotate_user_agent = True
    sourceFile = "./urls/provincesUrl2.csv"
    with open(sourceFile) as f:
        urls = f.readlines()
        urls = [url[:-1].lower() for url in urls if url != "urls\n"]

    start_urls = urls

    def parse(self, response):

        regionAns = response.css("table.uj tr a")
        region = regionAns[0].attrib["href"]
        hrefs = response.css("table.at tr td a")

        for href in hrefs:
                yield {"urls": f"https://www.tuttitalia.it{region[:-1]}{href.attrib['href'][2:]}statistiche/popolazione-andamento-demografico/"}

process = CrawlerProcess()
process.crawl(tuttItaliaRegions)
process.start()