import requests, json

base_url = "https://api.gemini.com/v2"
response = requests.get(base_url + "/candles/lrceth/15m")
candle_data = response.json()

print(candle_data)
