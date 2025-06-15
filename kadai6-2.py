
import requests
import pandas as pd

API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/120000.json"
response = requests.get(API_URL)
data = response.json()

dates = data[0]["timeSeries"][0]["timeDefines"][:2]  # 2日分の日付
areas = data[0]["timeSeries"][0]["areas"]

records = []
for area in areas:
    name = area["area"]["name"]
    weathers = area["weathers"][:2]
    for i, date in enumerate(dates):
        records.append({"地域": name, "日付": date[:10], "天気": weathers[i]})

df = pd.DataFrame(records)
print(df)


# 【データ名称】天気予報 API（livedoor 天気互換）
# 【概要】気象庁が出してる日本の地域別天気予報データ（JSON形式）
# 【エンドポイント】https://www.jma.go.jp/bosai/forecast/data/forecast/120000.json
# 【機能】地域ごとの2日間の天気情報が見れる
# 【使い方】GETリクエストでURLにアクセスするとデータが取れる。
