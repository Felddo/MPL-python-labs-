import pandas as pd
from bs4 import BeautifulSoup
import time
import requests


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_ship_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')

    counter = soup.find('div', class_='pagination-totals')
    if not counter or counter.text != '1 судно':
        return None

    ship_link = soup.find('a', class_='ship-link')
    if not ship_link:
        return None
    time.sleep(1)
    ship_url = 'https://www.vesselfinder.com' + ship_link['href']
    ship_page = requests.get(ship_url, headers=HEADERS)
    ship_name = BeautifulSoup(ship_page.text, 'html.parser')

    my_ship = {
        'Название': '',
        'IMO': '',
        'MMSI': '',
        'Тип': ''
    }
    title = ship_name.find('h1', class_='title')
    if title:
        my_ship['Название'] = title.text

    cells = ship_name.find_all('td')
    for i in range(len(cells)):
        cell_text = cells[i].text

        if cell_text == 'MMSI':
            my_ship['MMSI'] = cells[i + 1].text if i + 1 < len(cells) else ''

        elif cell_text == 'IMO / MMSI':
            if i + 1 < len(cells):
                parts = cells[i + 1].text.split('/')
                if len(parts) == 2:
                    my_ship['IMO'] = parts[0].strip()
                    my_ship['MMSI'] = parts[1].strip()

        elif cell_text == 'AIS тип':
            my_ship['Тип'] = cells[i + 1].text if i + 1 < len(cells) else ''

    return my_ship


def main():
    df = pd.read_excel('Links.xlsx')
    links = df['Ссылка'].tolist()
    results = []
    for i, link in enumerate(links):
        print(f'Обрабатываю {i + 1} из {len(links)}: {link}')
        info = get_ship_info(link)
        if info:
            results.append(info)
    if results:
        result_df = pd.DataFrame(results)
        result_df.to_excel('result.xlsx', index=False)
    else:
        print('Ничего не найдено')


if __name__ == '__main__':
    main()
