import numpy as np
import requests
import os
import dateparser
import pytz
import json
import random
import time
import itertools
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config.builder import Builder
from config.config import config
from logs import logger
from presentation.observer import Observable

DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
#CRYPTO = ['BTC','ETH','SOL','DOT','OMI','BAN','MOON']
CRYPTO = ['BTC','ETH','SOL']

def get_dummy_data():
    logger.info('Generating dummy data')

def get_percentage_diff(previous, current):
    try:
        percentage = abs(previous - current)/max(previous, current) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage

def fetch_prices(token, graph_type):
    try:
        days_ago = DATA_SLICE_DAYS
        endtime = int(time.time())
        starttime = endtime - 60*60*24*days_ago
        starttimeseconds = starttime
        endtimeseconds = endtime
        if token == "BTC":
            tokenname = "bitcoin"
        elif token == "ETH":
            tokenname = "ethereum"
        elif token == "SOL":
            tokenname = "solana"
        elif token == "DOT":
            tokenname = "polkadot"
        elif token == "OMI":
            tokenname = "ecomi"
        elif token == "BAN":
            tokenname = "banano"
        elif token == "MOON":
            tokenname = "moon"
        else:
            print("Unknown Token, please add to if statement")
            exit()
        if graph_type == "line":
            geckourlhistorical = "https://api.coingecko.com/api/v3/coins/"+str(tokenname)+"/market_chart/range?vs_currency=usd&from="+str(starttimeseconds)+"&to="+str(endtimeseconds)
        if graph_type == "candle" or graph_type == "renko":
            geckourlhistorical = "https://api.coingecko.com/api/v3/coins/"+str(tokenname)+"/ohlc?days=1&vs_currency=usd"
        logger.info(geckourlhistorical)
        rawtimeseries = requests.get(geckourlhistorical).json()

        if graph_type == "line":
            timeseriesarray = rawtimeseries['prices']
            prices = []
            length=len(timeseriesarray)
            i=0
            while i < length:
                prices.append(timeseriesarray[i][1])
                i+=1    
            liveprice = prices[-1:][0] 
            actual24h = get_percentage_diff(prices[0], liveprice)
        elif graph_type == "candle" or graph_type == "renko":
            prices = [entry[1:] for entry in rawtimeseries] # removing timestamp, we don't need it
            liveprice = prices[-1][3]
            actual24h = get_percentage_diff(prices[0][3], liveprice)

        # Add values to list
        prices.append(liveprice)
        prices.append(actual24h)
        prices.append(token)

        return prices
    except Exception as e:
        logger.info("Unexpected error")
        logger.info(e)
        time.sleep(5)
        return ("null")

def main():
    logger.info('Initialize')

    data_sink = Observable()
    builder = Builder(config)
    builder.bind(data_sink)

    while True:
        for coin in itertools.cycle(CRYPTO):
            try:
                prices = fetch_prices(coin, config.graph_type)
                if prices != "null": 
                    new_prices = [x for x in prices]
                    data_sink.update_observers(new_prices)
                    exit()
                    time.sleep(30)
            except (HTTPError, URLError) as e:
                logger.info(str(e))
                time.sleep(5)
            except Exception as e:
                logger.info(e)
                time.sleep(5)
            except KeyboardInterrupt:
                logger.info('Exit')
                data_sink.close()
                exit()
            
if __name__ == "__main__":
    main()
