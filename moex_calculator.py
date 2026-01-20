import pandas as pd
import json

from datetime import timedelta, datetime
from pathlib import Path
from utils.moex_archive import MoexArchive
from utils.date_utils import daterange

from data_scripts.tickers_mapping import TICKER_TO_ACTUAL_TICKER

TICKER = "TICKER"
DATE = "DATE"
PRICE = "PRICE"


class PriceArchive:
  def __init__(self, prices_path: Path):
    self.prices = pd.read_csv(prices_path, sep=";")

  def get_price(self, ticker, date: datetime):
    date_str = date.strftime("%Y%m%d")

    price = self.prices.loc[
      (self.prices[TICKER] == ticker) & (self.prices[DATE] == int(date_str)), PRICE
    ]
    found_ticker = (self.prices[TICKER] == ticker).sum()
    found_date = (self.prices[DATE] == int(date_str)).sum()
    print(f"{found_ticker=}, {found_date=}, {ticker=}, {date_str=}\n{price=}")

    if not price.empty:
      return price.iloc[0]

    return None

  def get_moex_working_days(self):
    working_days = set(self.prices.loc[self.prices[TICKER] != "PLZL"][DATE])
    return working_days


def calculate_index_coefficient(moex_archive, prices_archive, date):
  moex_list = moex_archive.get_moex_list(date)
  value = 0
  for orig_ticker in moex_list:
    ticker = orig_ticker
    if (
      orig_ticker in TICKER_TO_ACTUAL_TICKER
      and TICKER_TO_ACTUAL_TICKER[orig_ticker] != ""
    ):
      ticker = TICKER_TO_ACTUAL_TICKER[orig_ticker]
    price = prices_archive.get_price(ticker, date)
    if price is None:
      return None
    ff_shares = moex_archive.get_free_float(orig_ticker, date)
    coef = moex_archive.get_coef(orig_ticker, date)

    value += price * ff_shares * coef

  return value


def main():
  START_DATE = datetime(2025, 2, 10)
  END_DATE = datetime(2025, 8, 15)
  MOEX_STATUSES_PATH = Path(
    "/home/chereshnya/Me/Finance/MOEX_with_no_companies/data/moex_statuses"
  )
  PRICES_PATH = Path(
    "/home/chereshnya/Me/Finance/MOEX_with_no_companies/preprocessed_data/prices_by_day.csv"
  )

  moex_archive = MoexArchive(MOEX_STATUSES_PATH)
  prices_archive = PriceArchive(PRICES_PATH)
  moex_archive.open_all_statuses(START_DATE, END_DATE)

  moex = {START_DATE: 3012.39}
  prev_date = START_DATE
  prev_value = calculate_index_coefficient(moex_archive, prices_archive, START_DATE)

  working_days = prices_archive.get_moex_working_days()
  for date in daterange(START_DATE + timedelta(days=1), END_DATE):
    if int(date.strftime("%Y%m%d")) not in working_days:
      continue

    value = calculate_index_coefficient(moex_archive, prices_archive, date)
    if value is None:
      continue
    moex[date] = moex[prev_date] * value / prev_value
    prev_value = value
    prev_date = date

  SAVE_PATH = "/home/chereshnya/Me/Finance/MOEX_with_no_companies/moex_values.json"
  moex = {k.strftime("%d.%m.%Y"): v for k, v in moex.items()}
  with open(SAVE_PATH, "w") as f:
    json.dump(moex, f)


if __name__ == "__main__":
  main()
