""" BASICS: module to work with ohlc and generate indicators """

import pandas as pd
import numpy as np
from typing import Tuple
import talib.abstract as ta
from IPython.display import HTML
import random


def hide_toggle(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'Toggle show/hide'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current, 
        toggle_text=toggle_text
    )

    return HTML(html)


# NOT NEEDED ---------------------------------------------
def get_strat_dates(start: int, end: int) -> Tuple[str, str]:
    start = str(pd.Timestamp(start, unit='s').round(freq='D'))
    end = str(pd.Timestamp(end, unit='s').round(freq='D'))

    return (start, end)


# NEEDED IN get_indicators ---------------------------------------------

def typical_price(bars):
    res = (bars['high'] + bars['low'] + bars['close']) / 3.
    return pd.Series(index=bars.index, data=res)


def bollinger_bands(series, window=20, stds=2):
    ma = rolling_mean(series, window=window, min_periods=1)
    std = rolling_std(series, window=window, min_periods=1)
    upper = ma + std * stds
    lower = ma - std * stds

    return pd.DataFrame(index=series.index, data={
        'upper': upper,
        'mid': ma,
        'lower': lower
    })

def rolling_std(series, window=200, min_periods=None):
    min_periods = window if min_periods is None else min_periods
    if min_periods == window and len(series) > window:
        return numpy_rolling_std(series, window, True)
    else:
        try:
            return series.rolling(window=window, min_periods=min_periods).std()
        except Exception as e:  # noqa: F841
            return pd.Series(series).rolling(window=window, min_periods=min_periods).std()


def rolling_mean(series, window=200, min_periods=None):
    min_periods = window if min_periods is None else min_periods
    if min_periods == window and len(series) > window:
        return numpy_rolling_mean(series, window, True)
    else:
        try:
            return series.rolling(window=window, min_periods=min_periods).mean()
        except Exception as e:  # noqa: F841
            return pd.Series(series).rolling(window=window, min_periods=min_periods).mean()


# Principal function ---------------------------------------------

def get_indicators(df_: pd.DataFrame, pair: str, timeset: int, timeframe: str) -> pd.DataFrame:

    df = df_.copy()
    
    # SMA - Simple Moving Average
    df['sma3'] = ta.SMA(df, timeperiod=3)
    df['sma5'] = ta.SMA(df, timeperiod=5)
    df['sma10'] = ta.SMA(df, timeperiod=10)
    df['sma21'] = ta.SMA(df, timeperiod=21)
    df['sma50'] = ta.SMA(df, timeperiod=50)
    df['sma100'] = ta.SMA(df, timeperiod=100)
    
    # RSI
    df['rsi'] = ta.RSI(df)

    # Stochastic RSI
    stoch_rsi = ta.STOCHRSI(df)
    df['fastd_rsi'] = stoch_rsi['fastd']
    df['fastk_rsi'] = stoch_rsi['fastk']

    # MACD
    macd = ta.MACD(df)
    df['macd'] = macd['macd']
    df['macdsignal'] = macd['macdsignal']
    df['macdhist'] = macd['macdhist']

    # Bollinger Bands
    bollinger = bollinger_bands(typical_price(df), window=20, stds=2)
    df['bb_lowerband'] = bollinger['lower']
    df['bb_middleband'] = bollinger['mid']
    df['bb_upperband'] = bollinger['upper']
    df["bb_percent"] = (
        (df["close"] - df["bb_lowerband"]) /
        (df["bb_upperband"] - df["bb_lowerband"])
    )
    df["bb_width"] = (
        (df["bb_upperband"] - df["bb_lowerband"]) / df["bb_middleband"]
    )
        
    return df
