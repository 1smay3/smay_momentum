from arctic import Arctic
from config import *
import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='momentum.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

store = Arctic('localhost')
read_library = store['US.EOD.CALC']
write_library = store['US.EOD.MOM']

test = ['AAPL_EOD_CALC']


def momentum_signal(st, lt, row):
    if row[st] < row[lt]:
        val = -1
    elif row[st] > row[lt]:
        val = 1
    else:
        val = 0
    return val


repoed_testfile = read_library.read(*test)
repoed_testfile.data.to_excel("testfile.xlsx")

for symbol in test:  # read_library.list_symbols():
    # Load data from local DB
    try:
        df = read_library.read(symbol)
        data = df.data
        for key, value in signal_dict.items():
            data[key] = data['adjClose'].rolling(window=value).mean().shift(1)
            plot_data = data.drop(columns=['open', 'high', 'low', 'close', 'volume', 'unadjustedVolume', 'change',
                                           'vwap', 'intra_day_ret', 'total_day_ret', 'long_only_cum_ret'])
    except:
        logging.error('%s raised an error', symbol)
plot_data.plot()
plt.show()