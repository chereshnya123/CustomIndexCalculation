from datetime import timedelta

def daterange(start, end, delta=timedelta(days=1)):
  current = start
  while current <= end:
    current += delta
    yield current