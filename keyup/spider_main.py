from keyup.spiders.cannonkeys import CannonkeysSpider
from keyup.spiders.novelkeys import NovelkeysSpider
from keyup.spiders.tkc import TkcSpider
from keyup.spiders.omnitype import OmnitypeSpider
from keyup.spiders.konostore import KonostoreSpider
from keyup.spiders.mekibo import MekiboSpider

import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(CannonkeysSpider)
    yield runner.crawl(NovelkeysSpider)
    yield runner.crawl(TkcSpider)
    yield runner.crawl(OmnitypeSpider)
    yield runner.crawl(MekiboSpider)
    yield runner.crawl(KonostoreSpider)
    reactor.stop()


crawl()
reactor.run()