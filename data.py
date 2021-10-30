# Import data from local database
from arctic import Arctic


store = Arctic('localhost')
library = store['US.EOD']

for symbol in library.list_symbols():
    df = library.read(symbol)
    print(df.data)
