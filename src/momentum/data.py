# Import data from local database
import logging

import pandas as pd
from arctic import Arctic

logging.basicConfig(filename='../../logs/data.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

store = Arctic('localhost')

read_library = store['US.EOD']
write_library = store['US.EOD.CALC']

# Add functionality to see if calculations have already been done, and to add new data and run
# calculations in an append fashion
for symbol in read_library.list_symbols():
    # Load data from local DB
    try:
        df = read_library.read(symbol)
        data = df.data
        data.index = pd.to_datetime(data.index)

        # Run calculations
        data['intra_day_ret'] = (data['close'] / data['open']) - 1
        data['total_day_ret'] = data['adjClose'].pct_change()
        data['long_only_cum_ret'] = (1 + data.total_day_ret).cumprod() - 1

        # Save to local write DB
        write_library.write(symbol + "_CALC", data, metadata={'source': 'Financial Modelling Prep'})
    except:
        logging.error('%s raised an error', symbol)
