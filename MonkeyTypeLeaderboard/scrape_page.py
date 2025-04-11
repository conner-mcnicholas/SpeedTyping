from time import sleep,time
import requests
import pandas as pd

url = "https://api.monkeytype.com/leaderboards"
params = {
    "mode": "time",
    "language": "english",
    "mode2": 15,
    "page": 0
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
df_data = pd.DataFrame(data['data']['entries'])[['rank','name','wpm','raw','acc','consistency','timestamp']]
df_data['datetime']=pd.to_datetime(df_data['timestamp']*.001, unit='s', errors='coerce')
df_data=df_data[['rank','name','wpm','raw','acc','consistency','datetime']]
df_data.to_csv('leaderboard_t15_f50.csv', index=False)