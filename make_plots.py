import numpy as np
import pandas as pd
import time
from datetime import datetime
import json
import requests
import os
from tqdm import tqdm
from pathlib import Path
import matplotlib.dates as mdates
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
TOP_DIR='/Users/tylermartin/Documents/programming/london_weather'

def apply_mdates(ax, freq):
    if freq == "4hour":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H"))
        ax.xaxis.set_major_locator(mdates.HourLocator(np.arange(0, 24, 4)))
        ax.xaxis.set_minor_locator(mdates.HourLocator())
    if freq == "hour":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %H"))
        ax.xaxis.set_major_locator(mdates.HourLocator(np.arange(0, 24)))
        ax.xaxis.set_minor_locator(mdates.HourLocator())
    if freq == "day":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator())
    if freq == "week":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(0))
        ax.xaxis.set_minor_locator(mdates.DayLocator(0))
    if freq == "month":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator([0, 15]))
    if freq == "month_no_year":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_minor_locator(mdates.DayLocator([0, 15]))
    if freq == "year":
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_minor_locator(mdates.MonthLocator([1,4,7,10]))
    return ax
