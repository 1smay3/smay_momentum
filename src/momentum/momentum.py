import logging

import numpy as np
import pandas as pd
from arctic import Arctic

from src.momentum.config import *
from src.momentum.metrics import *

logging.basicConfig(filename='../../logs/momentum.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

store = Arctic('localhost')
read_library = store['US.EOD.CALC']
write_library = store['US.EOD.MOM']

test = ['AAPL_EOD_CALC']

repoed_testfile = read_library.read(*test)
repoed_testfile.data.to_excel("testfile.xlsx")


def momentum_signal(dataframe, short, long):
    if dataframe[short] < dataframe[long]:
        val = -1
    elif dataframe[short] > dataframe[long]:
        val = 1
    else:
        val = 0
    return val


for symbol in test:  # read_library.list_symbols():
    # Load data from local DB
    try:
        # Read data for given symbol
        df = read_library.read(symbol)
        data = df.data
        data.index = pd.to_datetime(data.index)
    except:
        logging.error('%s raised an error', symbol)

    # Calculate moving averages and label accordingly
    for key, value in signal_dict.items():
        data[key] = data['adjClose'].rolling(window=value).mean().shift(1)
        plot_data = data.drop(columns=['open', 'high', 'low', 'close', 'volume', 'unadjustedVolume', 'change',
                                       'vwap'])

    # Calculate signals given moving averages
    for i in range(int(len(signal_dict) / 2)):
        st = 'st_' + str((i + 1))
        lt = 'lt_' + str((i + 1))
        plot_data['ts_' + str((i + 1))] = plot_data.apply(momentum_signal, args=(st, lt), axis=1)

    # Average moving average signals for position sizing
    signal_cols = [col for col in plot_data if col.startswith('ts_')]
    plot_data['ts_avg'] = plot_data[signal_cols].mean(axis=1)

    # Calculate returns for given signal
    plot_data['signal_return'] = np.zeros(len(plot_data['ts_avg']))
    for x in range(1, len(plot_data['ts_avg'])):
        if plot_data['ts_avg'][x] == plot_data['ts_avg'][x - 1]:
            plot_data['signal_return'][x] = plot_data['ts_avg'][x] * plot_data['total_day_ret'][x]
        else:
            # Here, signals have changed so take intraday return and deduct trading cost
            plot_data['signal_return'][x] = (plot_data['ts_avg'][x] * plot_data['intra_day_ret'][x]) - trading_cost

    plot_data['ts_ret'] = cumulative_ret(plot_data, "signal_return")

    # fig = returns_plot(plot_data, "ts_avg", "long_only_cum_ret", "ts_ret")
    # fig.show()

print(sharpe_ratio(plot_data, "signal_return"))
