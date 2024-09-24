import pandas as pd

years = list(range(2017, 2024))
df = pd.DataFrame()

for year in years:
    url = rf'https://www.pro-football-reference.com/years/{year}/fantasy.htm#fantasy'
    df_temp = pd.read_html(url, skiprows=0)[0]
    df_temp.columns = [f'{tup[0]}_{tup[1]}' for tup in df_temp.columns]
    df_temp['Year'] = year
    df = pd.concat([df, df_temp], ignore_index=True)

df['Opps/g'] = (df.Rushing_Att + df.Receiving_Tgt) / df.Games_G
df['ScrmYds/g'] = (df.Rushing_Yds + df.Receiving_Yds) / df.Games_G
min = years.min()
max = year.max()
df.to_csv(f'../historical_data/ff_historical_{min}_{max}.csv', index=False)