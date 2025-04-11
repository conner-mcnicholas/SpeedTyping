from time import sleep,time
import requests
import pandas as pd

url = "https://api.monkeytype.com/leaderboards"
params = {
    "mode": "time",
    "language": "english",
    "mode2": 60,
    "pageSize":200
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

df_leaderboard = pd.DataFrame()

stime = time()

i=90

while True:
    params["page"] = i
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data['data']['entries']==[]:
        break  # Exit the loop if there are no more entries
    df_data = pd.DataFrame(data['data']['entries'])[['rank','name','wpm','raw','acc','consistency','timestamp']]
    df_leaderboard = pd.concat([df_leaderboard, df_data], ignore_index=True)
    lastrec = df_data.iloc[-1][['rank']].to_list()[0]
    sleep(7.2)  # Sleep for 1 second to avoid overwhelming the server
    if i//10 == i/10:
        etime = 2669+(time()-stime)
        pctfin = 100*lastrec/data['data']['count']
        estremain = (etime/pctfin)*(100-pctfin)
        print(f"{int(etime//3600)}:{int((etime%3600)//60)}:{int(etime%60)} spent scraping:")
        print(f"\t{18000+(200*(i-90))} rows ({pctfin:.2f}% of total)")
        print(f"{int(estremain//3600)}:{int((estremain%3600)//60)}:{int(estremain%60)} remains\n")
        df_leaderboard.to_csv('leaderboard_t15_from18k.csv', index=False)
    i+=1    

# Save the DataFrame to a CSV file                  
df_leaderboard = df_leaderboard.drop_duplicates(subset=['name'], keep='last')
df_leaderboard['datetime']=pd.to_datetime(df_leaderboard['timestamp']*.001, unit='s', errors='coerce')
df_leaderboard=df_leaderboard[['rank','name','wpm','raw','acc','consistency','datetime']]
df_leaderboard.to_csv('leaderboard_t15_from18k.csv', index=False)