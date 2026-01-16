import pandas as pd
import numpy as np
from pathlib import Path
from mapping import TICKER_MAPPING

DATA_PATH = Path("/home/chereshnya/Me/Finance/MOEX_with_no_companies/data")
PRICES = DATA_PATH / "prices.csv"
MOEX_STATUSES = DATA_PATH / "moex_statuses"

PREPROCESSED_DATA_PATH = Path(
    "/home/chereshnya/Me/Finance/MOEX_with_no_companies/preprocessed_data"
)

TICKER = "TICKER"
LOW_PRICE = "<LOW>"
HIGH_PRICE = "<HIGH>"
AVG_PRICE = "<PRICE>"
CLOSE = "<CLOSE>"

UNUSED_PRICES_COLUMNS = [
    "<PER>",
    "<TIME>",
    "<OPEN>",
    "<HIGH>",
    "<LOW>",
    "<AMOUNT>",
    "<CLOSE>",
    "<VOLUME>",
]


def get_trimmed_column_names(df):
    new_columns = []

    for column in df.columns:
        new_columns.append(column[1:-1])

    return new_columns


def main():
    prices = pd.read_csv(PRICES, delimiter=";")
    for company_prices in (DATA_PATH / "companies_prices").iterdir():
        company = pd.read_csv(company_prices, delimiter=";")
        prices = pd.concat([prices, company], join='inner')

    prices[AVG_PRICE] = prices[CLOSE]
    prices = prices.drop(columns=UNUSED_PRICES_COLUMNS)
    prices.columns = get_trimmed_column_names(prices)
    prices[TICKER].replace(TICKER_MAPPING, inplace=True)
    
    prices.to_csv(PREPROCESSED_DATA_PATH / "prices.csv", sep=";", index=False)


if __name__ == "__main__":
    main()
