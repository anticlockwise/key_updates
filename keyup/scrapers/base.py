from pyquery import PyQuery as pq
from ..models import USER_AGENT


class Scraper:
    def scrape(self):
        raise NotImplemented("Child class should override this to scrape a given URL")


class PyQueryBasedScraper(Scraper):
    def scrape(self):
        url = self._get_url()
        doc = pq(url, headers={'User-Agent': USER_AGENT})
        return self._scrape(doc)
    
    def _get_url(self):
        raise NotImplemented("Child class should override this to return a URL to scrape")
    
    def _scrape(self, doc):
        raise NotImplemented("Child class should override this to scrape from the given doc")
