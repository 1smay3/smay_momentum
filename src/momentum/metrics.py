def infer_frequency(df):
    td = df.index[1] - df.index[0]
    freq = td.days
    return 252 / freq


def cumulative_ret(dataframe, column_name):
    return (1 + dataframe[column_name]).cumprod() - 1


def annualised_return(df, daily_ret_col):
    ann_factor = len(df.index) / (infer_frequency(df))
    df['cum_ret'] = cumulative_ret(df, daily_ret_col)
    total_return = (df['cum_ret'].iloc[-1] - df['cum_ret'].iloc[0]) + 1
    return (total_return ** (1 / ann_factor)) - 1


def annualised_vol(df, daily_ret_col):
    ann_factor = len(df.index) / (infer_frequency(df))
    vol_factor = 252 / ann_factor
    return df[daily_ret_col].std() * (vol_factor ** 0.5)


def sharpe_ratio(df, daily_ret_col):
    return annualised_return(df, daily_ret_col) / annualised_vol(df, daily_ret_col)
