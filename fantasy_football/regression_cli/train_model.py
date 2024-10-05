import pandas as pd
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
warnings.filterwarnings('ignore') 

positions = [
    ('QB', 24, ['PassAtt_g', 'PassYds_g', 'RushAtt_g', 'ScrmYds_g']), 
    ('RB', 60, ['RushAtt_g', 'Targets_g', 'Catches_g', 'ScrmYds_g']), 
    ('WR', 72, ['Targets_g', 'Catches_g', 'ScrmYds_g']), 
    ('TE', 24, ['Targets_g', 'Catches_g', 'ScrmYds_g'])
]

past_years = [2017, 2023]
current_year = past_years[-1] + 1

def get_training_data(start_year, end_year):
    years = list(range(start_year, end_year+1))
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
    return df

def train_model():    
    df = get_training_data(past_years[0], past_years[-1])
    df['PassAtt_g'] = df.Passing_Att / df.Games_G
    df['PassYds_g'] = df.Passing_Yds / df.Games_G
    df['RushAtt_g'] = df.Rushing_Att / df.Games_G
    df['Targets_g'] = df.Receiving_Tgt / df.Games_G
    df['Catches_g'] = df.Receiving_Rec / df.Games_G
    df['ScrmYds_g'] = (df.Rushing_Yds + df.Receiving_Yds) / df.Games_G
    df['PPR_g'] = df.Fantasy_PPR / df.Games_G

    models = {}
    for pos, cutoff, cols in positions:
        all_cols = cols + ['PPR_g']
        # df_temp = df.dropna(subset=all_cols, how='any').reset_index(drop=True)
        df_temp = df.fillna(0)
        x = df_temp.loc[(df.FantPos == pos) & (df.Fantasy_PosRank <= cutoff), cols]
        y = df_temp.loc[(df.FantPos == pos) & (df.Fantasy_PosRank <= cutoff), 'PPR_g']
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42)

        models[pos] = LinearRegression()
        models[pos].fit(X_train, y_train)
        print(f'R-squared for {pos}: {models[pos].score(X_train, y_train)}')
    return models

def get_current_data(year):
    url = rf'https://www.pro-football-reference.com/years/{year}/fantasy.htm#fantasy'
    df = pd.read_html(url, skiprows=0)[0]
    df.columns = [f'{tup[0]}_{tup[1]}' if 'Unnamed' not in tup[0] else f'{tup[1]}' for tup in df.columns]
    df.Player = df.Player.str.replace('*', '').str.replace('+', '')
    mask = df.loc[df['Rk'] == 'Rk'].index
    df = df.drop(labels=mask)
    exclude = ['Player', 'Tm', 'FantPos']
    columns = [col for col in df.columns if col not in exclude]
    for col in columns: 
        df.loc[:, col] = pd.to_numeric(df[col])
    df = df.loc[df.Games_G != 0]
    df['Year'] = year
    df['PassAtt_g'] = df.Passing_Att / df.Games_G
    df['PassYds_g'] = df.Passing_Yds / df.Games_G
    df['RushAtt_g'] = df.Rushing_Att / df.Games_G
    df['Targets_g'] = df.Receiving_Tgt / df.Games_G
    df['Catches_g'] = df.Receiving_Rec / df.Games_G
    df['ScrmYds_g'] = (df.Rushing_Yds + df.Receiving_Yds) / df.Games_G
    df['PPR_g'] = df.Fantasy_PPR / df.Games_G
    return df

def make_predictions():
    df_raw = get_current_data(current_year)
    models = train_model()
    df = pd.DataFrame()
    for pos, cutoff, cols in positions:
        df_temp = df_raw.loc[df_raw.FantPos == pos]
        df_temp['Prediction'] = models[pos].predict(df_temp[cols])
        df = pd.concat([df, df_temp])
    return df



        

