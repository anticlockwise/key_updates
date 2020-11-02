from pyquery import PyQuery as pq
from .models import GroupBuyItem, USER_AGENT
import json


URL = 'https://novelkeys.xyz/pages/updates'


gb_items = []
d = pq(URL, headers={'User-Agent': USER_AGENT})
update_cells = d(".sc-pkHUE .sc-pkUyL")
for update_cell in update_cells:
    update_cell_pq = pq(update_cell)
    gb_url = update_cell_pq.attr("data-href")
    
    if gb_url:
        title_cell = update_cell_pq('h3.sc-oTLFK .sc-ptSuy')
        title = title_cell.text()

        expected_ship_date_cell = update_cell_pq('.sc-pbYdQ')
        if len(expected_ship_date_cell) == 2:
            expected_ship_date = pq(expected_ship_date_cell[1]).text().strip()

            if expected_ship_date:
                gb_item = GroupBuyItem(title, expected_ship_date)
                gb_items.append(gb_item)
                
for gb_item in gb_items:
    print(json.dumps(gb_item.__dict__()))
