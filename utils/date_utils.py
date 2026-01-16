from datetime import timedelta

def daterange(start, end):
  current = start
  while current <= end:
    current += timedelta(days=1)
    yield current