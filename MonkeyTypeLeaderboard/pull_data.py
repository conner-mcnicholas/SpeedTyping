from time import sleep,time
import requests
import pandas as pd
import os
from dotenv import load_dotenv

MODE2 = 60
url = "https://api.monkeytype.com/leaderboards"

load_dotenv()
ape_key = os.getenv('APE_KEY')
headers = {
    'Authorization': f'ApeKey {ape_key}'
}

params = {
    "mode": "time",
    "language": "english",
    "mode2": MODE2,
    "pageSize":200
}

df_leaderboard = pd.DataFrame()

stime = time()

i=0
while True:
    params["page"] = i
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data['data']['entries']==[]:
        break  # Exit the loop if there are no more entries
    df_data = pd.DataFrame(data['data']['entries'])[['rank','name','wpm','raw','acc','consistency','timestamp']]
    df_leaderboard = pd.concat([df_leaderboard, df_data], ignore_index=True)
    sleep(2.01)  #30 API requests per minute max

    # Every 10 pages of records, print out progress and save down everything we've go so far
    if i//10 == i/10:
        lastrec = df_data.iloc[-1][['rank']].to_list()[0]
        etime = time()-stime
        pctfin = 100*lastrec/data['data']['count']
        estremain = (etime/pctfin)*(100-pctfin)
        print(f"record # {lastrec} scraped")
        print(f"{int(etime//3600)}:{int((etime%3600)//60)}:{int(etime%60)} spent scraping:")
        print(f"\t{lastrec} rows ({pctfin:.2f}% of total)")
        print(f"{int(estremain//3600)}:{int((estremain%3600)//60)}:{int(estremain%60)} remains\n")
        df_leaderboard.to_csv('data/leaderboard_{MODE2}s.csv', index=False)
    i+=1    

# Save the DataFrame to a CSV file                  
df_leaderboard = df_leaderboard.drop_duplicates(subset=['name'], keep='last')
df_leaderboard['datetime']=pd.to_datetime(df_leaderboard['timestamp']*.001, unit='s', errors='coerce')
df_leaderboard=df_leaderboard[['rank','name','wpm','raw','acc','consistency','datetime']]
df_leaderboard.to_csv('data/leaderboard_{MODE2}s.csv', index=False)