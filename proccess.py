import sys
from typing import List

import pandas as pd

from config.config import dataset_path, url, nb_days, nb_col_before_sports
from extract import extract_dataset


def get_dataset(country: str = 'all') -> pd.DataFrame:
    """
    Get Paris Olympic dataset

    ### Parameters
        country (str): Name of the country you want to get the data
                        If set to 'all' get the whole dataset - default='all'

    ### Return
        df (DataFrame): Filtered dataset
    """

    df = pd.read_csv(dataset_path) if dataset_path else extract_dataset(url, nb_days)

    if country == "all":
        return df

    try:
        return df[df['country'] == country]
    except KeyError as e:
        sys.exit(f"Error: There is no data for the country {e}.")


def get_medals_evolution(df: pd.DataFrame, sex: str = 'all', type_: str = 'total',
                         cumul: bool = False) -> pd.DataFrame:
    """
    Get the evolution of the number of medals over the olympics
    """

    # Get the right index
    if sex != "all":
        col_name = f"{sex}_{type_}"
    else:
        col_name = f"total_{type_}" if type_ != 'total' else 'total_medals'

    filtered_df = df[['date', col_name, 'country']]

    if cumul:
        filtered_df[col_name] = filtered_df.groupby('country')[col_name].cumsum()

    return filtered_df, col_name

def get_ranking(df: pd.DataFrame, date_ = str):
    """
    Get the official Paris Olympics medals ranking
    """

    res = df[ df['date'] == date_ ][['country', 'total_gold', 'total_silver', 'total_bronze','total_medals']]
    res.sort_values(by=['total_gold','total_silver','total_bronze'])
    res = res.reset_index()

    return res

def get_medals_per_sport(df: pd.DataFrame, sports: List) -> pd.DataFrame:
    """
    Build a dataset containing the total number of medals by sport and country

    ### Parameters
        df (DataFrame): Original dataset

    ### Return
        (DataFrame)
    """

    no_sport_col = df.columns[nb_col_before_sports:].tolist()
    no_sport_col.remove('country')

    return df.groupby(['country']).sum().drop(labels=no_sport_col)[sports]


def nb_sports_with_medals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get a ranking of the country having most sports with medals

    ### Parameters
        df (DataFrame): Original dataset

    ### Return
        (DataFrame)
    """

    sports = df.columns[nb_col_before_sports:].tolist()
    df_ = df[df['date'] == max(df['date'])][['country'] + sports].reset_index()  # keep data from the last day
    df_['sports_with_medals'] = df_[sports].notna().sum(axis=1)  # count not NaN columns: Number of sports with medals

    res = df_[['country', 'sports_with_medals']]
    res = res.sort_values(by=['sports_with_medals'], ascending=False)

    return res


def sports_with_medals(df: pd.DataFrame, country) -> List[str]:
    """
    Get sports with medals for a country

    ### Parameters
        df (DataFrame): Original dataset

    ### Return
        (List)
    """

    sports = df.columns[nb_col_before_sports:].tolist()
    df_ = df[df['date'] == max(df['date'])][['country'] + sports].reset_index()  # keep data from the last day

    country_row = df_[df_['country'] == country]

    if country_row.empty:
        return []

    non_nan_columns = country_row.loc[:, country_row.notna().iloc[0]].columns.tolist()
    non_nan_columns.remove('index')
    non_nan_columns.remove('country')
    return non_nan_columns


if __name__ == "__main__":
    df = get_dataset()
    df_ = get_medals_evolution(df, 'all', 'total', True)
