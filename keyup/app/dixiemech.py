from .models import USER_AGENT
from pyquery import PyQuery as pq


BASE_URL = 'https://dixiemech.com'
URL = '{}/news'.format(BASE_URL)


d = pq(URL, headers={'User-Agent': USER_AGENT})
update_links = d("a.BlogList-item-title")
if update_links:
    latest_update_link = pq(update_links[0])
    latest_update_url = '{}{}'.format(BASE_URL, latest_update_link.attr("href"))
    update_doc = pq(latest_update_url, headers={'User-Agent': USER_AGENT})
