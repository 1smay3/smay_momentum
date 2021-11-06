from arctic import Arctic
from config import *
import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='momentum.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

store = Arctic('localhost')
read_library = store['US.EOD.CALC']
write_library = store['US.EOD.MOM']

test = ['AAPL_EOD_CALC']

repoed_testfile  = read_library.read(*test)
repoed_testfile.data.to_excel("testfile.xlsx")

for symbol in test: #read_library.list_symbols():
    # Load data from local DB
    try:
        df = read_library.read(symbol)
        data = df.data
        for signal in signals:
            data['ma_' + str(signal)] = data['adjClose'].rolling(window=signal).mean().shift(1)
    except:
            logging.error('%s raised an error', symbol)
