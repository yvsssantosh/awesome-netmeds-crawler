import scrapy
from scrapy.crawler import CrawlerProcess

from medicine import Medicine
from cc import ChemicalComposition
process = CrawlerProcess()
# process.crawl(Medicine)
process.crawl(ChemicalComposition)

process.start()
cc = ChemicalComposition()
cc.start_requests()