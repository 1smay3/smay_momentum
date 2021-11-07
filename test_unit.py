import numpy as np
import pandas as pd

from metrics import *

np.random.seed(13)
dist = np.random.normal(0.002, 0.01, 260)

df = pd.DataFrame(dist, columns=['dist'], index=pd.date_range(start='1/1/2000', periods=260, freq='D'))


def test_sharpe_answer():
    assert sharpe_ratio(df, 'dist') == 2.469658655822973
