from datetime import datetime, timedelta
import json

import pandas as pd
from bs4 import BeautifulSoup
import requests

from config.config import url, nb_days, save


def extract_medal_from_html(html: str, date: str) -> list:
    """
    Get the number of medals per country and per sport
    """
    soup = BeautifulSoup(html, 'lxml')
    json_div_id = "__NEXT_DATA__"  # div containing countries
    json_div = soup.find(id=json_div_id)

    # Get the json containing medals stats
    json_str = str(json_div).split(">")[1].split("<")[0]
    json_data = json.loads( json_str )
    medals_table = json_data['props']['pageProps']['initialMedals']['medalStandings']['medalsTable']

    # Init
    data = []
    for table in medals_table:
        current_table = {}
        current_table['date'] = f'{date[:4]}-{date[4:6]}-{date[6:]}'

        # Country name
        current_table['country'] = table['description']

        # Number of medals (total, men, women)
        init_col = ['men_gold', 'men_silver', 'men_bronze', 'total_gold', 'total_silver',
                    'total_bronze', 'women_gold', 'women_silver', 'women_bronze', ]

        nb_medals = [ elt for elt in table['medalsNumber'] if elt['type'] in ['Men','Women','Total'] ] # Handle when it's 'open'
        nb_medals.sort( key=lambda x: x['type'])
        total_medals, total_men, total_women = 0, 0, 0

        for i, medal_col in enumerate(init_col):
            if table['description'] == 'France':
                a = 1
            medal_type = medal_col.split('_')[1]
            idx = i // 3
            try:
                current_table[medal_col] = nb_medals[idx][medal_type]

                # Update total counts
                total_men = nb_medals[idx]['total'] if idx == 0 else total_men
                total_medals = nb_medals[idx]['total'] if idx == 1 else total_medals
                total_women = nb_medals[idx]['total'] if idx == 2 else total_women
            except IndexError as e:
                current_table[medal_col] = 0

        current_table['total_medals'], current_table['men_total'], current_table['women_total'] = (total_medals,
                                                                                                   total_men, total_women)

        # Medals per sport
        disciplines = table['disciplines']
        for d in disciplines:
            current_table[ d['name'] ] = ( d['gold'], d['silver'], d['bronze'] )


        data.append( current_table )

    return data


def request_medal_page(date: str, url: str) -> bytes:
    """
    Return the olympic medals page at a certain date
    """

    url = f"https://web.archive.org/web/{date}/{url}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.content


def extract_dataset(url: str, nb_day: int = 10) -> list:
    """
    Main
    """

    dataset = []
    current_date = datetime.strptime("2024-07-28", "%Y-%m-%d")

    for i in range(13):
        formatted_date = current_date.strftime('%Y%m%d')
        html = request_medal_page(formatted_date, url)
        data = extract_medal_from_html(html, formatted_date)
        dataset += data

        current_date += timedelta(days=1)
        print(f"..Day{i}, done!")

    return dataset


if __name__ == "__main__":
    d = extract_dataset(url, nb_days)
    df = pd.DataFrame( d )
    print("..Done\n", df.head())

    if save:
        tdy = datetime.now().strftime('%Y%m%d')
        df.to_csv(f'datasets/{tdy}_olympics_paris_medals.csv')