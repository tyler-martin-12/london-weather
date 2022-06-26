import numpy as np
import pandas as pd
import time
from datetime import datetime
import json
import requests
import os
from tqdm import tqdm
from pathlib import Path

TOP_DIR='/Users/tylermartin/Documents/programming/london_weather'
BASE = 'https://api.darksky.net/forecast'

def setup_dirs():
    os.makedirs(f"{TOP_DIR}/data", exist_ok=True)

def read_key():
    with open(f'{TOP_DIR}/key.txt') as f:
        key = f.read()
    return key


def read_latlong():
    with open(f'{TOP_DIR}/latlong.json', 'r') as f:
        latlong = json.load(f)
    return latlong

def ts_to_unix(ts):
    return int(ts.timestamp())

def unix_to_ts(unix):
    return pd.to_datetime(unix, unit='s')


def construct_url(key, lat, lon, ts):
    unix = ts_to_unix(ts)
    url = f'{BASE}/{key}/{lat},{lon},{unix}'
    return url

def response_to_df(response):
    day = json.loads(response.text)
    df = pd.DataFrame(day['hourly']['data'])
    to_drop = 'dewPoint ozone precipType pressure uvIndex windGust'.split()
    to_drop = [c for c in to_drop if c in df.columns]
    df.drop(to_drop, axis=1, inplace=True)
    
    rn={}
    rn['time']='unix'
    rn['temperature']='temp'
    rn['apparentTemperature']='apparent_temp'
    rn['windSpeed']='wind_speed'
    rn['windBearing']='wind_bearing'
    rn['cloudCover']='cloud_cover'
    df.rename(rn, axis=1, inplace=True)
    
    df['ts']=pd.to_datetime(df.unix,unit='s')

    return df

def start_download():
    start = pd.to_datetime('2015 01 01')
    stop = pd.to_datetime('2022 06 26')
    date_range = pd.date_range(start, stop)

    key=read_key()
    lat,lon=read_latlong()['london']

    for day in tqdm(date_range):
        day_str = day.strftime('%Y%m%d')
        save_path = f'{TOP_DIR}/data/{day_str}.parquet'

        if os.path.exists(save_path):
            continue

        url = construct_url(key, lat, lon, day)
        response = requests.get(url)
        if response.status_code != 200:
            print(response.text)
            return
        df = response_to_df(response)
        df.to_parquet(save_path)


def main():
    setup_dirs()
    start_download()


if __name__ == "__main__":
    main()
