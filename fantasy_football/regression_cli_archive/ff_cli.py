import pandas as pd


year = 2024
url = rf'https://www.pro-football-reference.com/years/{year}/fantasy.htm#fantasy'
df = pd.read_html(url, skiprows=0)[0]

df['Year'] = year
df.columns = [f'{tup[0]}_{tup[1]}' if 'Unnamed' not in tup[0] else f'{tup[1]}' for tup in df.columns]
df.Player = df.Player.str.replace('*', '').str.replace('+', '')

mask = df.loc[df['Rk'] == 'Rk'].index
df = df.drop(labels=mask)

numeric_cols = [col for col in df.columns if col not in ['Player', 'Tm', 'FantPos']]
for col in numeric_cols: 
    df.loc[:, col] = pd.to_numeric(df[col])
df = df.loc[df.Games_G != 0].reset_index(drop=True)

# model_dict = train_ff_model()

# add projection column, referencing model_dict
df['PPR_Projection'] = df.apply(lambda row: model_dict[row.FantPos].predict([[row.Opps_g, row.ScrmYds_g]]) if row.FantPos in model_dict.keys() else None, axis=1)
print(df[['Opps_g', 'ScrmYds_g', 'PPR_Projection']])

def main():
    pass
    



# if __name__ == '__main__':
#     main()

