import json
import math
import requests
import pandas as pd
import yfinance as yf
from website.constants import *

pd.set_option('display.max_rows', None)
pd.reset_option("max_columns")

midcap = yf.Ticker("NIFTY_MID_SELECT.NS")
closing_price = math.ceil(midcap.history(period="1d")['Close'].to_list()[0])
print(closing_price)

url_oc = "https://www.nseindia.com/option-chain"
url_midcp_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=MIDCPNIFTY'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()


def set_cookie():
    request = sess.get(url_oc, headers=headers)
    cookies = dict(request.cookies)
    # print("cookies set successfully")


def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        # print("get_data successfully")
        return response.text
    print("error in get_data")


def requiredDataIndex(data, requiredDataIndex, expiryDate):
    for i in range(len(data['records']['data'])):
        ExpiryDate = data['records']['data'][i]
        if expiryDate == ExpiryDate['expiryDate']:
            requiredDataIndex.append(i)


def finalRequiredData(requiredDataIndex, requiredData):
    finalDataArray = []
    for i in requiredDataIndex:
        finalDataSubArray = []
        if (requiredData[i].get('CE') is not None) and (requiredData[i].get('PE') is not None):
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["openInterest"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["changeinOpenInterest"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["totalTradedVolume"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["impliedVolatility"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["lastPrice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["change"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["bidQty"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["bidprice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["askPrice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["askQty"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["strikePrice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["bidQty"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["bidprice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["askPrice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["askQty"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["change"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["lastPrice"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["impliedVolatility"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["totalTradedVolume"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["changeinOpenInterest"], 2))
            finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["openInterest"], 2))
        else:
            if requiredData[i].get('CE') != None:
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["openInterest"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["changeinOpenInterest"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["totalTradedVolume"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["impliedVolatility"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["lastPrice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["change"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["bidQty"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["bidprice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["askPrice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['CE']["strikePrice"], 2))
                for j in range(10):
                    finalDataSubArray.append("-")
            else:
                for j in range(9):
                    finalDataSubArray.append("-")
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["strikePrice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["bidQty"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["bidprice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["askPrice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["askQty"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["change"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["lastPrice"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["impliedVolatility"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["totalTradedVolume"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["changeinOpenInterest"], 2))
                finalDataSubArray.append("%.2f" % round(requiredData[i]['PE']["openInterest"], 2))
        finalDataArray.append(finalDataSubArray)
    return finalDataArray


get_data(url_midcp_nf)
response_text = get_data(url_midcp_nf)
data_mnf = json.loads(response_text)

mnfExpiryDate = data_mnf["records"]["expiryDates"][0]

print(mnfExpiryDate)

mnfRequiredDataIndex = []

requiredDataIndex(data_mnf, mnfRequiredDataIndex, mnfExpiryDate)

mnfRequiredData = data_mnf['records']['data']

mnfRequiredData = finalRequiredData(mnfRequiredDataIndex, mnfRequiredData)

print(len(mnfRequiredData))

# Create the pandas DataFrame
df = pd.DataFrame(mnfRequiredData, columns=call_put)
# print(df['STRIKE'].head())
# print(df.iloc[100:119, :13].head())


df["STRIKE"] = pd.to_numeric(df["STRIKE"], errors='coerce')

# df['STRIKE'] = df['STRIKE'].astype(float)

# data = df.iloc[100:119, :]
print(df.iloc[100:130, 8:12])

uppar = closing_price + 200
lower = closing_price - 200
print(uppar)
print(lower)

data = df.loc[(df['STRIKE'] > 12400.0) & (df['STRIKE'] < 12000.0)]

mask = (df['STRIKE'] >= 12400) & (df['STRIKE'] <= 12000)
data1 = df[mask]

df_new = df[(df['STRIKE'] == 12400.0) & (df['STRIKE'] == 12000.0)]
print(df.dtypes)
print(df_new.to_markdown())
