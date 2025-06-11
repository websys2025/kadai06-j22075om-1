import requests

APP_ID = "fb46893eae42240089b3e9c083392e6060cd07be"

API_URL = "http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0003138226",  # 夏季賞与（毎月勤労統計）
    "cdArea": "00000",            # 全国
    "cdCat01": "G",           # 情報通信業コード
    "cdTime": "2013000000,2014000000,2015000000", #年次　2013,2014,2015年
    "cdTab": "1101",             # 支給額
    "cdEstablishment": "0,1,2,3",# 規模計, 30人未満, 30-99人, 100人以上
    "lang": "J",
}

response = requests.get(API_URL, params=params)
data = response.json()
print(data)
