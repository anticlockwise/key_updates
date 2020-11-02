import urllib3
from pyquery import PyQuery as pq
from .models import GroupBuyItem, USER_AGENT

URL = 'https://cannonkeys.com/pages/group-buy-status'


d = pq(URL)

gb_status_div = d('div.rte')
children = gb_status_div.contents()
for child in children:
    if str(child).strip():
        if child.tag == 'h4':
            print(pq(child).text())
        elif child.tag == 'p':
            title_elem = pq(child).find('strong')
            if title_elem:
                print(title_elem.text())
