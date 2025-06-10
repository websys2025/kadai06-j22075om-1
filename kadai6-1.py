import requests

APP_ID = "fb46893eae42240089b3e9c083392e6060cd07be"

API_URL = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0003138226",  # 賞与データの統計表ID
    "lang": "J",
}

response = requests.get(API_URL, params=params)
data = response.json()
print(data)
