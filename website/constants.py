import numpy as np

call_put = ["OI", "CHNG_IN_OI", "VOLUME", "IV", "LTP", "CHNG", "BID_QTY", "BID", "ASK", "ASK_QTY", "STRIKE",
            "BID_QTY", "BID", "ASK", "ASK_QTY", "CHNG", "LTP", "IV", "VOLUME", "CHNG_IN_OI", "OI"]

URL_OPTION_CHAIN = "https://www.nseindia.com/option-chain"
URL_MIDCAP = 'https://www.nseindia.com/api/option-chain-indices?symbol=MIDCPNIFTY'
URL_FINNIFTY = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
URL_BANKNIFTY = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
URL_NIFTY = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/125.0.6422.60 Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}

convert_dict = {'IV': np.float64, 'LTP': np.float64,
                'CHNG': np.float64, 'BID': np.float64,
                'ASK': np.float64
}

convert_int = {'OI': np.int32, 'CHNG_IN_OI': np.int32,
                'VOLUME': np.int32, 'IV': np.float64,
                'LTP': np.float64, 'CHNG': np.float64,
                'BID_QTY': np.int32, 'BID': np.float64,
                'ASK': np.float64, 'ASK_QTY': np.int32, 'STRIKE': np.float64,
}

SELECT_ROWS = 12
