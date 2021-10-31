from arctic import Arctic
from config import *
import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='momentum.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

store = Arctic('localhost')
read_library = store['US.EOD.CALC']
write_library = store['US.EOD.MOM']

test = ['AAPL_EOD_CALC']
for symbol in test: #read_library.list_symbols():
    # Load data from local DB
    try:
        df = read_library.read(symbol)
        data = df.data
        data['st_mom1'] = data['adjClose'].rolling(window=st_1).mean().shift(1)
        data['st_mom2'] = data['adjClose'].rolling(window=st_2).mean().shift(1)
        data['st_mom3'] = data['adjClose'].rolling(window=st_3).mean().shift(1)

        data['lt_mom1'] = data['adjClose'].rolling(window=lt_1).mean().shift(1)
        data['lt_mom2'] = data['adjClose'].rolling(window=lt_2).mean().shift(1)
        data['lt_mom3'] = data['adjClose'].rolling(window=lt_3).mean().shift(1)

        data[['adjClose', 'st_mom1', 'st_mom2', 'st_mom3', 'lt_mom1', 'lt_mom2', 'lt_mom3']].plot()
        plt.show()
    except:
            logging.error('%s raised an error', symbol)
