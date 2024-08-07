from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup
import requests

from config.config import url, nb_days, save


def extract_medal_from_html(html: str) -> dict:
    """
    Get the number of medals per country and per sport
    """
    soup = BeautifulSoup(html, 'lxml')
    countries_div = "virtuoso-item-list"  # div containing countries
    tab = soup.find(attrs={"data-test-id": countries_div})
    soup_tab = BeautifulSoup(str(tab), 'lxml')

    idx = 0
    medals_per_country = {}
    country_div = soup_tab.find(attrs={"data-index": idx})

    while country_div:

        medals_count = {}
        soup = BeautifulSoup(str(country_div), 'lxml')
        country_name = str(soup.find(class_="elhe7kv5 emotion-srm-uu3d5n"))

        try:
            country_name = country_name.split('>')[1].split('<')[0]
        except IndexError:
            pass

        medals = soup.find_all(class_="e1oix8v91 emotion-srm-81g9w1")
        medals = list(map(lambda x: str(x).split('>')[1].split('<')[0], medals))

        if medals:
            medals_count['gold'] = medals[0]
            medals_count['silver'] = medals[1]
            medals_count['bronze'] = medals[2]

            medals_per_country[country_name] = medals_count
        idx += 1
        country_div = soup_tab.find(attrs={"data-index": idx})

    return medals_per_country


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

    dataset = dict()
    current_date = datetime.strptime("2024-07-28", "%Y-%m-%d")

    for i in range(10):
        formatted_date = current_date.strftime('%Y%m%d')
        html = request_medal_page(formatted_date, url)
        data = extract_medal_from_html(html)
        dataset[formatted_date] = data

        current_date += timedelta(days=1)
        print(f"..Day{i}, done!")

    return dataset


if __name__ == "__main__":
    d = run(url, nb_days)
    df = pd.DataFrame(d)
    print("..Done\n", df.head())

    if save:
        tdy = datetime.now().strftime('%Y%m%d')
        df.to_csv(f'datasets/{tdy}_olympics_paris_medals.csv')