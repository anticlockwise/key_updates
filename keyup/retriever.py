import urllib3
import json


URL = "http://mechgroupbuys.com/gb-data"


def fetch():
    http = urllib3.PoolManager()
    gb_response = http.request('GET', URL)
    if gb_response.status == 200:
        gb_data = gb_response.data
        gb_items = json.loads(gb_data)
        return gb_items
    return []