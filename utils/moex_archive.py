import pandas as pd

from bisect import bisect_left
from pathlib import Path
from datetime import datetime
from utils.date_utils import daterange

TICKER = 'Code'
FREE_FLOAT = "Free-float factor"
SHARES_COUNT = "Number of issued shares"
RESTRICTING_COEF = "Restricting coefficient"

class MoexArchive:
  def __init__(self, statuses_path: Path):
    self.statuses_path = statuses_path
    self.update_dates = self.extract_index_update_dates()
    self.opened_statuses = dict()

  def extract_index_update_dates(self):
    update_dates = []
    for filename in self.statuses_path.iterdir():
      if ".csv" not in str(filename.name):
        continue
      date = str(filename.name)[:-4]
      date = datetime.strptime(date, "%d_%m_%Y")
      update_dates.append(date)
    
    update_dates.sort()
    
    return update_dates
      
  def open_all_statuses(self, start, end):
    for date in daterange(start, end):
      actual_date = self.get_actual_date(date)
      filename = self.statuses_path  / (actual_date.strftime("%d_%m_%Y") + ".csv")
      self.opened_statuses[filename] = pd.read_csv(filename, sep=',')

  def get_actual_date(self, date: datetime):
    actual_date = bisect_left(self.update_dates, date) - 1
    if actual_date < 0:
      return None

    return self.update_dates[actual_date]

  def get_moex_status(self, date: datetime):
    actual_date = self.get_actual_date(date)
    filename = self.statuses_path / (actual_date.strftime("%d_%m_%Y") + ".csv")
    if filename not in self.opened_statuses:
      self.opened_statuses[filename] = pd.read_csv(filename, sep=',')

    return self.opened_statuses[filename]

  def get_moex_list(self, date):
    moex_status = self.get_moex_status(date)
    
    return list(moex_status[TICKER])

  def get_free_float(self, ticker, date):
    moex_status = self.get_moex_status(date)
    free_float_coef = moex_status.loc[moex_status[TICKER] == ticker, FREE_FLOAT].iloc[0]
    shares_count = moex_status.loc[moex_status[TICKER] == ticker, SHARES_COUNT].iloc[0]

    return free_float_coef * shares_count

  def get_coef(self, ticker, date):
    moex_status = self.get_moex_status(date)

    return moex_status.loc[moex_status[TICKER] == ticker, RESTRICTING_COEF].iloc[0]
