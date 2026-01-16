import pandas as pd
from tickers_mapping import TICKER_TO_ACTUAL_TICKER
from pathlib import Path

STATUSES_PATH = Path("/home/chereshnya/Me/Finance/MOEX_with_no_companies/data/moex_statuses")
TICKER = 'Code'

for table_name in STATUSES_PATH.iterdir():
  moex_status = pd.read_csv(table_name, delimiter=',')
  tickers = set(moex_status[TICKER])
  for ticker in tickers:
    if ticker in TICKER_TO_ACTUAL_TICKER and TICKER_TO_ACTUAL_TICKER[ticker] != "":
      moex_status.loc[moex_status[TICKER] == ticker, TICKER] = TICKER_TO_ACTUAL_TICKER[ticker]
  
  moex_status.to_csv(table_name, index=False)