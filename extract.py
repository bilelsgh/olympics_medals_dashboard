from datetime import datetime, timedelta
import json

import pandas as pd
from bs4 import BeautifulSoup
import requests

from config.config import url, nb_days, save


def extract_medal_from_html(html: str, date: str) -> dict:
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
    data = {}
    for table in medals_table:
        current_table = {}
        current_table['date'] = date # reformatter la date !!!! todo
        # Number of medals (total, men, women)
        nb_medals = table['medalsNumber']

            # total
        try :
            current_table['total_gold'] = nb_medals[2]['gold']
            current_table['total_silver'] = nb_medals[2]['silver']
            current_table['total_bronze'] = nb_medals[2]['bronze']
        except IndexError as e:
            (current_table['total_gold'], current_table['total_silver'],
             current_table['total_bronze']) = 0, 0, 0

            # men
        try:
            current_table['men_gold'] = nb_medals[0]['gold']
            current_table['men_silver'] = nb_medals[0]['silver']
            current_table['men_bronze'] = nb_medals[0]['bronze']
        except IndexError as e:
            (current_table['men_gold'], current_table['men_silver'],
             current_table['men_bronze']) = 0, 0, 0

            # women
        try:
            current_table['women_gold'] = nb_medals[1]['gold']
            current_table['women_silver'] = nb_medals[1]['silver']
            current_table['women_bronze'] = nb_medals[1]['bronze']
        except IndexError as e:
            (current_table['women_gold'], current_table['women_silver'],
             current_table['women_bronze']) = 0, 0, 0

        # Medals per sport
        disciplines = table['disciplines']
        for d in disciplines:
            current_table[ d['name'] ] = ( d['gold'], d['silver'], d['bronze'] )

        data[table['description']] = current_table

    return data


def request_medal_page(date: str, url: str) -> bytes:
    """
    Return the olympic medals page at a certain date
    """

    url = f"https://web.archive.org/web/{date}/{url}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.content


def run(url: str, nb_day: int = 10) -> dict:
    """
    Main
    """

    dataset = []
    current_date = datetime.strptime("2024-07-28", "%Y-%m-%d")

    for i in range(2):
        formatted_date = current_date.strftime('%Y%m%d')
        html = request_medal_page(formatted_date, url)
        data = extract_medal_from_html(html, formatted_date)
        dataset.append( data )

        current_date += timedelta(days=1)
        print(f"..Day{i}, done!")

    return dataset


if __name__ == "__main__":
    d = run(url, nb_days)
    df = pd.DataFrame( d )
    print("..Done\n", df.head())

    if save:
        tdy = datetime.now().strftime('%Y%m%d')
        df.to_csv(f'datasets/{tdy}_olympics_paris_medals.csv')