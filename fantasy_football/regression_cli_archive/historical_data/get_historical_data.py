import pandas as pd

years = list(range(2017, 2024))
min = years[0]
max = years[-1]
df = pd.DataFrame()

for year in years:
    url = rf'https://www.pro-football-reference.com/years/{year}/fantasy.htm#fantasy'
    df_temp = pd.read_html(url, skiprows=0)[0]
    df_temp.columns = [f'{tup[0]}_{tup[1]}' if 'Unnamed' not in tup[0] else f'{tup[1]}' for tup in df_temp.columns]
    df_temp.Player = df_temp.Player.str.replace('*', '').str.replace('+', '')
    mask = df_temp.loc[df_temp['Rk'] == 'Rk'].index
    df_temp = df_temp.drop(labels=mask)
    exclude = ['Player', 'Tm', 'FantPos']
    columns = [col for col in df_temp.columns if col not in exclude]
    for col in columns: 
        df_temp.loc[:, col] = pd.to_numeric(df_temp[col])
    df_temp = df_temp.loc[df_temp.Games_G != 0]
    df_temp['Year'] = year
    df = pd.concat([df, df_temp], ignore_index=True)

df['Opps/g'] = (df.Rushing_Att + df.Receiving_Tgt) / df.Games_G
df['ScrmYds/g'] = (df.Rushing_Yds + df.Receiving_Yds) / df.Games_G
df['Fantasy_PPR/g'] = df.Fantasy_PPR / df.Games_G
df.to_csv(f'../historical_data/ff_historical_{min}_{max}.csv', index=False)