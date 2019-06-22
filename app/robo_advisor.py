
import csv
import json
import os
import datetime

from dotenv import load_dotenv
import requests


load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)


api_key = os.environ.get("ALPHADVANTAGE_API_KEY")
#print(api_key)

def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    #print(type(response))
    #print(response.status_code)
    #print(response.text)
    parsed_response = json.loads(response.text)
    return parsed_response


def transform_response(parsed_response):
    tsd = parsed_response ["Time Series (Daily)"]
    
    rows = []
    for date, daily_prices in tsd.items(): # see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
         row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
         rows.append(row)

    return rows
         


def write_to_csv(rows, csv_filepath):
    # rows should be a list of dictionaries
    # csv_filepath should be a string filepath pointing to where the data should be written

    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)

    return True



if __name__ == "__main__":

    time_now = datetime.datetime.now() #> datetime.datetime(2019, 3, 3, 14, 44, 57, 139564)

    #INFORMATION INPUTS
    
    symbol = input("Please specify a stock symbol (e.g. AMZN) and press enter: ")
#validate input

    options = [symbol]

    if input not in options:
        print("Invalid entry. Please input a valid stock symbol")
        exit()


    parsed_response = get_response(symbol)

    last_refreshed = parsed_response["Meta Data"] ["3. Last Refreshed"]
    
    rows = transform_response(parsed_response)

    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] # list comprehension for mapping purposes!
    low_prices = [row["low"] for row in rows] # list comprehension for mapping purposes!
    recent_high = max(high_prices)
    recent_low = min(low_prices)


    #latest_day = dates[0]
    #latest_close = tsd[latest_day]["4. close"]
    #high_prices = []
    #low_prices =[]

    #for target_list in dates:
       # high_price =tsd[latest_day]["2. high"]
       # high_prices.append(float(high_price))
       # low_price =tsd[latest_day]["3. low"]
       # low_prices.append(float(low_price))
   # recent_high = max(high_prices)
    #recent_low = min(low_prices)

#breakpoint()


    #dates = list(tsd.keys())

    

#breakpoint()
#INFORMATION OUTPUTS

#csv_file_path = "data/prices.csv" # a relative filepath

    #csv_file_path =os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    #csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    #with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
      #  writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
       # writer.writeheader() # uses fieldnames set above
       # for date in dates:
       #     daily_prices = tsd[date]
         #   writer.writerow({
          #      "timestamp": date,
          #      "open": daily_prices["1. open"],
          #      "high": daily_prices["2. high"],
          #      "low": daily_prices["3. low"],
           #     "close": daily_prices["4. close"],
           #     "volume": daily_prices["5. volume"]
          #  })

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

    formatted_time_now = time_now.strftime("%Y-%m-%d %H:%M:%S") #> '2019-03-03 14:45:27'
    csv_file_path = csv_file_path.split("..")[1] #> data/prices.csv


    print("-------------------------")
    print(f"SYMBOL: {symbol}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print(f"REQUEST AT: {formatted_time_now}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: TODO")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

