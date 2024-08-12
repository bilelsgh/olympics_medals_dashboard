import sys

import pandas as pd

from config.config import dataset_path, url, nb_days
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
                         cumul: bool=False) -> pd.DataFrame:
    """
    Get the evolution of the number of medals over the olympics
    """

    # Get the right index
    if sex != "all":
        col_name = f"{sex}_{type_}"
    else:
        col_name = f"total_{type_}" if type_ != 'total' else 'total_medals'

    filtered_df = df[ ['date', col_name, 'country'] ]

    if cumul:
        filtered_df[col_name] = filtered_df.groupby('country')[col_name].cumsum()

    return filtered_df, col_name


def get_medals_per_sport(df: pd.DataFrame) -> pd.DataFrame:
    pass

def nb_sports_with_medals(df: pd.DataFrame) -> pd.DataFrame:
    pass


if __name__ == "__main__":
    df = get_dataset()
    df_ = get_medals_evolution(df, 'all', 'total', True)