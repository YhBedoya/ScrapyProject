import scrapy
from scrapy.crawler import CrawlerProcess

class tuttItaliaExtracter(scrapy.Spider):
    name = "infoCollector"
    version = 2
    nameFile = f"tuttitalia{version}.csv"

    custom_settings = {
        "FEEDS": {f"./urls/{nameFile}": {"format": "csv",
                                                         'overwrite': True}},
        "DOWNLOAD_DELAY": 2
    }

    rotate_user_agent = True
    sourceFile = f"./urls/citiesUrl{version}.csv"
    with open(sourceFile) as f:
        urls = f.readlines()
        urls = [url[:-1].lower() for url in urls if url != "urls\n"]

    start_urls = urls

    def parse(self, response):

        url = response.url
        region = url.split("/")[3]
        city = response.xpath('//*[@id="ic"]//a[5]//text()').extract_first()

        results = {}

        table1rows = response.xpath('//*[@class="vm"]//tr')
        for row in table1rows:
            year = row.xpath("td[1]//text()").extract_first()
            year = str(year).replace("*", "")
            year = year if not (year == "None") else 0
            if int(year)<2019:
                continue
            results[year] = {"year": year,
                            "saldoMigratorioEstero": row.xpath("td[8]//text()").extract_first(),
                             "saldoMigratorioTotale": row.xpath("td[9]//text()").extract_first()}

        table2rows = response.xpath('//*[@class="ip"]//tr')
        flag = True
        for row in table2rows:
            expression = str(row.xpath("th[7]//text()").extract_first())
            if not expression == "None":
                flag = expression == "Media componenti"
                continue

            if not flag:
                year = row.xpath("td[1]//text()").extract_first()
                year = str(year).replace("*", "")
                year = year if not (year == "None") else 0
                if int(year) < 2019:
                    continue
                results[year]["saldoNaturale"] = row.xpath("td[7]//text()").extract_first()
            else:
                continue

        for item in results:
            yield {"year": results[item]["year"],
                   "region": region,
                   "city": city,
                   "saldo migratorio estero": results[item]["saldoMigratorioEstero"],
                   "saldo migratorio totale": results[item]["saldoMigratorioTotale"],
                   "saldo naturale": results[item]["saldoNaturale"]}


process = CrawlerProcess()
process.crawl(tuttItaliaExtracter)
process.start()