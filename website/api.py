import time
import json
import requests
import math
import numpy as np
import pandas as pd
from .constants import *
import yfinance as yf

sess = requests.Session()
cookies = dict()


def set_cookie():
    request = sess.get(URL_OPTION_CHAIN, headers=HEADERS)
    cookies = dict(request.cookies)
    # print("cookies set successfully")


def get_data(url):
    set_cookie()
    response = sess.get(url, headers=HEADERS, cookies=cookies)
    if response.status_code == 200:
        # print("get_data successfully")
        return response.text
    print("error in get_data")


def get_level_5min(index):
    yca = yf.Ticker(index)
    data = yca.history(interval="5m")
    # print(data)
    return math.floor(data['Close'].values[-1])


def required_data_index(data, required_data_index, expiry_date):
    for i in range(len(data['records']['data'])):
        expiryDate = data['records']['data'][i]
        if expiry_date == expiryDate['expiryDate']:
            required_data_index.append(i)


def final_required_data(required_data_index, required_data):
    final_data_array = []
    for i in required_data_index:
        final_data_sub_array = []
        if (required_data[i].get('CE') is not None) and (required_data[i].get('PE') is not None):
            final_data_sub_array.append(required_data[i]['CE']["openInterest"])
            final_data_sub_array.append(required_data[i]['CE']["changeinOpenInterest"])
            final_data_sub_array.append(required_data[i]['CE']["totalTradedVolume"])
            final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["impliedVolatility"], 2))
            final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["lastPrice"], 2))
            final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["change"], 2))
            final_data_sub_array.append(required_data[i]['CE']["bidQty"])
            final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["bidprice"], 2))
            final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["askPrice"], 2))
            final_data_sub_array.append(required_data[i]['CE']["askQty"])
            final_data_sub_array.append(required_data[i]['PE']["strikePrice"])
            final_data_sub_array.append(required_data[i]['PE']["bidQty"])
            final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["bidprice"], 2))
            final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["askPrice"], 2))
            final_data_sub_array.append(required_data[i]['PE']["askQty"])
            final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["change"], 2))
            final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["lastPrice"], 2))
            final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["impliedVolatility"], 2))
            final_data_sub_array.append(required_data[i]['PE']["totalTradedVolume"])
            final_data_sub_array.append(required_data[i]['PE']["changeinOpenInterest"])
            final_data_sub_array.append(required_data[i]['PE']["openInterest"])
        else:
            if required_data[i].get('CE') != None:
                final_data_sub_array.append(required_data[i]['CE']["openInterest"])
                final_data_sub_array.append(required_data[i]['CE']["changeinOpenInterest"])
                final_data_sub_array.append(required_data[i]['CE']["totalTradedVolume"])
                final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["impliedVolatility"], 2))
                final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["lastPrice"], 2))
                final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["change"], 2))
                final_data_sub_array.append(required_data[i]['CE']["bidQty"])
                final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["bidprice"], 2))
                final_data_sub_array.append("%.2f" % round(required_data[i]['CE']["askPrice"], 2))
                final_data_sub_array.append(required_data[i]['CE']["strikePrice"])
                for j in range(10):
                    final_data_sub_array.append("-")
            else:
                for j in range(9):
                    final_data_sub_array.append("-")
                final_data_sub_array.append(required_data[i]['PE']["strikePrice"])
                final_data_sub_array.append(required_data[i]['PE']["bidQty"])
                final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["bidprice"], 2))
                final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["askPrice"], 2))
                final_data_sub_array.append(required_data[i]['PE']["askQty"])
                final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["change"], 2))
                final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["lastPrice"], 2))
                final_data_sub_array.append("%.2f" % round(required_data[i]['PE']["impliedVolatility"], 2))
                final_data_sub_array.append(required_data[i]['PE']["totalTradedVolume"])
                final_data_sub_array.append(required_data[i]['PE']["changeinOpenInterest"])
                final_data_sub_array.append(required_data[i]['PE']["openInterest"])
        final_data_array.append(final_data_sub_array)
    return final_data_array


def get_nifty50():
    # NIFTY
    response_text = get_data(URL_NIFTY)
    data_nifty = json.loads(response_text)
    nifty_expiry_date = data_nifty["records"]["expiryDates"][0]
    nifty_required_data_index = []
    required_data_index(data_nifty, nifty_required_data_index, nifty_expiry_date)
    nifty_required_data = data_nifty['records']['data']
    nifty_required_data = final_required_data(nifty_required_data_index, nifty_required_data)

    df = pd.DataFrame(nifty_required_data, columns=call_put)
    # print(df.dtypes)
    # df.replace('-', 0, inplace=True)

    df = df.astype(convert_dict)

    level = get_level_5min("^NSEI")

    lower = df[df['STRIKE'] >= level]
    uppar = df[df['STRIKE'] <= level]

    uppar = uppar.tail(SELECT_ROWS)
    lower = lower.head(SELECT_ROWS)

    df = pd.concat([uppar, lower], ignore_index=True)

    # Convert only numeric columns to integers
    # numeric_cols = df4.select_dtypes(include=['float64']).columns
    # df['OI'] = df['OI'].astype(np.int32)
    # df = df.astype(convert_int)
    # print(df['OI'])

    main_data = df.values.tolist()
    return level, main_data, nifty_expiry_date


def get_fin_nifty():
    # FINNIFTY
    response_text = get_data(URL_FINNIFTY)
    data_finnifty = json.loads(response_text)
    finnifty_expiry_date = data_finnifty["records"]["expiryDates"][0]
    finnifty_required_data_index = []
    required_data_index(data_finnifty, finnifty_required_data_index, finnifty_expiry_date)
    finnifty_required_data = data_finnifty['records']['data']
    finnifty_required_data = final_required_data(finnifty_required_data_index, finnifty_required_data)

    df = pd.DataFrame(finnifty_required_data, columns=call_put)
    # df4.replace('-', 0, inplace=True)
    df = df.astype(convert_dict)

    level = get_level_5min("NIFTY_FIN_SERVICE.NS")

    lower = df[df['STRIKE'] >= level]
    uppar = df[df['STRIKE'] <= level]

    uppar = uppar.tail(SELECT_ROWS)
    lower = lower.head(SELECT_ROWS)

    df = pd.concat([uppar, lower], ignore_index=True)

    # Convert only numeric columns to integers
    # numeric_cols = df4.select_dtypes(include=['float64']).columns
    # df['OI'] = df['OI'].astype(np.int32)
    # df = df.astype(convert_int)

    main_data = df.values.tolist()
    return level, main_data


def get_midcap_nifty():
    # MIDCAP
    response_text = get_data(URL_MIDCAP)
    data_midcap = json.loads(response_text)
    midcap_expiry_date = data_midcap["records"]["expiryDates"][0]
    midcap_required_data_index = []
    required_data_index(data_midcap, midcap_required_data_index, midcap_expiry_date)
    midcap_required_data = data_midcap['records']['data']
    midcap_required_data = final_required_data(midcap_required_data_index, midcap_required_data)

    df = pd.DataFrame(midcap_required_data, columns=call_put)
    # df4.replace('-', 0, inplace=True)
    df = df.astype(convert_dict)

    level = get_level_5min("NIFTY_MID_SELECT.NS")

    lower = df[df['STRIKE'] >= level]
    uppar = df[df['STRIKE'] <= level]

    uppar = uppar.tail(SELECT_ROWS)
    lower = lower.head(SELECT_ROWS)

    df = pd.concat([uppar, lower], ignore_index=True)

    # Convert only numeric columns to integers
    # numeric_cols = df4.select_dtypes(include=['float64']).columns
    # df['OI'] = df['OI'].astype(np.int32)
    # df = df.astype(convert_int)

    main_data = df.values.tolist()
    return level, main_data


def get_bank_nifty():
    # BANKNIFTY
    response_text = get_data(URL_BANKNIFTY)
    data_banknifty = json.loads(response_text)
    banknifty_expiry_date = data_banknifty["records"]["expiryDates"][0]
    banknifty_required_data_index = []
    required_data_index(data_banknifty, banknifty_required_data_index, banknifty_expiry_date)
    banknifty_required_data = data_banknifty['records']['data']
    banknifty_required_data = final_required_data(banknifty_required_data_index, banknifty_required_data)

    df = pd.DataFrame(banknifty_required_data, columns=call_put)
    df = df.astype(convert_dict)

    level = get_level_5min("^NSEBANK")

    lower = df[df['STRIKE'] >= level]
    uppar = df[df['STRIKE'] <= level]

    uppar = uppar.tail(SELECT_ROWS)
    lower = lower.head(SELECT_ROWS)

    df = pd.concat([uppar, lower], ignore_index=True)

    # Convert only numeric columns to integers
    # numeric_cols = df4.select_dtypes(include=['float64']).columns
    # df['OI'] = df['OI'].astype(np.int32)
    # df = df.astype(convert_int)
    # df.to_csv('bank.csv', index=False)

    # CALLS = df.iloc[:, 0:10]
    # PUTS = df.iloc[:, 10:]

    main_data = df.values.tolist()
    # return level, CALLS, PUTS
    return level, main_data
