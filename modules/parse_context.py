from bs4 import BeautifulSoup


def parse_entry(row):
    attributes = []
    for td in row.findAll('td'):
        if td.find('font'):
            attributes.append(td.get_text().strip())
    return attributes



def parse_html(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    contain_pricing = False
    items = []
    for row in soup.table.findAll('tr'):
        row_text = row.get_text().strip()
        if len(row.findAll('td')) == 11 and '金額' not in row_text:
            attrs = parse_entry(row)
            item = {
                'name' :attrs[0],
                'count': int(attrs[1].replace('*','')),
                'price':int(attrs[2])
            }
            items.append(item)
        elif '金額' in row_text:
            contain_pricing = True

    if not contain_pricing:
        assert len(items) == 0

    return items

