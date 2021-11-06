from arctic import Arctic
from config import *
import matplotlib.pyplot as plt
import logging
import numpy as np

logging.basicConfig(filename='momentum.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

store = Arctic('localhost')
read_library = store['US.EOD.CALC']
write_library = store['US.EOD.MOM']

test = ['AAPL_EOD_CALC']


def momentum_signal(dataframe, short, long):
    if dataframe[short] <= dataframe[long]:
        val = -1
    elif dataframe[short] >= dataframe[long]:
        val = 1
    else:
        val = 0
    return val


repoed_testfile = read_library.read(*test)
repoed_testfile.data.to_excel("testfile.xlsx")

for symbol in test:  # read_library.list_symbols():
    # Load data from local DB
    try:
        # Read data for given symbol
        df = read_library.read(symbol)
        data = df.data

    except:
        logging.error('%s raised an error', symbol)

    # Calculate moving averages and label accordingly
    for key, value in signal_dict.items():
        data[key] = data['adjClose'].rolling(window=value).mean().shift(1)
        plot_data = data.drop(columns=['open', 'high', 'low', 'close', 'volume', 'unadjustedVolume', 'change',
                                       'vwap', 'intra_day_ret', 'total_day_ret', 'long_only_cum_ret'])

    # Calculate signals given moving averages
    for i in range(int(len(signal_dict) / 2)):
        st = 'st_' + str((i + 1))
        lt = 'lt_' + str((i + 1))
        plot_data['ts_' + str((i + 1))] = plot_data.apply(momentum_signal, args=(str(st), lt), axis=1)

plot_data.plot()
plt.show()
