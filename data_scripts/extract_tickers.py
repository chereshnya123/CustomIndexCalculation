import pandas as pd
import os

STATUSES_PATH = "/home/chereshnya/Me/Finance/MOEX_with_no_companies/data/moex_statuses"

tickers = set()
for csv in os.listdir(STATUSES_PATH):
  moex_status = pd.read_csv(STATUSES_PATH + "/" + csv, delimiter=",")
  CODE = moex_status.columns[1]
  tickers = tickers.union(set(moex_status[CODE].unique()))

print("TICKER_TO_NAME = {")
for ticker in tickers:
  print(f"\"{ticker}\": \"\",")

print("}")