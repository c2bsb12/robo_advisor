
import csv
import json
import os
import datetime

from dotenv import load_dotenv
import requests


load_dotenv()
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#INFORMATION INPUTS

api_key = os.environ.get("ALPHADVANTAGE_API_KEY")
print(api_key)
symbol ="MSFT"
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)


time_now = datetime.datetime.now() #> datetime.datetime(2019, 3, 3, 14, 44, 57, 139564)


parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"] ["3. Last Refreshed"]

#breakpoint()

tsd = parsed_response ["Time Series (Daily)"]
dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices =[]

for target_list in dates:
    high_price =tsd[latest_day]["2. high"]
    high_prices.append(float(high_price))
    low_price =tsd[latest_day]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#breakpoint()
#INFORMATION OUTPUTS

#csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path =os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

        writer.writerow({
            "timestamp": "TODO",
            "open": "TODO",
            "high": "TODO",
            "low": "TODO",
            "close": "TODO",
            "volume": "TODO"
        })
   
formatted_time_now = time_now.strftime("%Y-%m-%d %H:%M:%S") #> '2019-03-03 14:45:27'


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
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

