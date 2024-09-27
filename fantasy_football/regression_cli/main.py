import pandas as pd
import train_model

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

df['Opps_g'] = (df.Rushing_Att + df.Receiving_Tgt) / df.Games_G
df['ScrmYds_g'] = (df.Rushing_Yds + df.Receiving_Yds) / df.Games_G
df['Rushing_Att_g'] = df.Rushing_Att / df.Games_G
df['Catches_g'] = df.Receiving_Rec / df.Games_G
df['Fantasy_PPR_g'] = df.Fantasy_PPR / df.Games_G

model_dict = train_model.get_ff_model()

# add projection column, referencing model_dict
df['PPR_Projection'] = df.apply(lambda row: model_dict[row.FantPos].predict([[row.Rushing_Att_g, row.Catches_g, row.ScrmYds_g]]) if row.FantPos in model_dict.keys() else None, axis=1)
df.loc[:, 'PPR_Projection'] = df['PPR_Projection'].astype(float)
def main():
    running = True
    while running:
        print('''
        MODES:
        1. Single Projection
        2. Set my lineup
        3. Assess waivers
        4. Generate trade suggestions    
        ''')
        print('')
        choice = input('Select your mode (enter a number): ')

        if choice == '1': 
            names = input('Enter the name(s) of your player(s) separated by commas: ')
            names = [name.title() for name in names.split(', ')]
            print(df.loc[df.Player.isin(names), ['Player', 'FantPos', 'Rushing_Att_g', 'Catches_g', 'ScrmYds_g', 'PPR_Projection']].sort_values(by=['FantPos', 'PPR_Projection'], ascending=[True, False]))
            exit = input('Exit program? (Y/N) ')
            if exit.upper() == 'Y':
                running = False
        elif choice == '2': 
            pass
        elif choice == '3': 
            pass
        elif choice == '4': 
            pass
        else:
            print('Wrong choice')
    
if __name__ == '__main__':
    main()

