from extractors.fetchers import FetchHTTP
from extractors.extentions import CSV

f = FetchHTTP(url='https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv')
csv = CSV(_file=f)
