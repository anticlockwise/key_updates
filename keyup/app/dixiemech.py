import urllib3
from .models import USER_AGENT
from pyquery import PyQuery as pq


BASE_URL = 'https://dixiemech.com'
URL = '{}/news'.format(BASE_URL)

http = urllib3.PoolManager()
r = http.request('GET', URL, headers={
    'User-Agent': USER_AGENT
})

d = pq(r.data)
update_links = d("a.BlogList-item-title")
if update_links:
    latest_update_link = update_links[0]
    latest_update_url = latest_update_link.attr("href")
    r = http.request('GET', latest_update_url, headers={
        'User-Agent': USER_AGENT
    })

    d = pq(r.data)
