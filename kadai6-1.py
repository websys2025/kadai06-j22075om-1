import requests

import pandas as pd

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

# 統計データからデータ部取得
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# JSONからDataFrameを作成
df = pd.DataFrame(values)

# メタ情報取得
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

# 統計データのカテゴリコードを意味のある名称に置換
for class_obj in meta_info:
    
    # メタ情報の「@id」の先頭に'@'を付与した文字列が、統計データの列名と対応している
    col = '@' + class_obj['@id']
    
    
    # 統計データの列名を「@code」から「@name」に置換するディクショナリを作成
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']

    # ディクショナリを用いて、指定した列の要素を置換
    df[col] = df[col].replace(id_to_name_dict)

# 統計データの列名を変換するためのディクショナリを作成
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

# ディクショナリに従って、列名を置換する
new_columns = []
for col in df.columns:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)

df.columns = new_columns

print(df)

# 【データ名称】毎月勤労統計調査-全国調査（e-Stat）
# 【概要】支給労働者１人平均支給額の統計データ
# 【エンドポイント】http://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
# 【機能】全国の情報通信業の2013～2015年の事業所規模別夏季賞与の平均支給額を表示
# 【使い方】APIのパラメータに地域や年次を指定してGETリクエストでデータ取得可能
