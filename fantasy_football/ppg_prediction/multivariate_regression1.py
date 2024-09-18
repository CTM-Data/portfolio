import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore') 

positions = [('RB', 48), ('WR', 60), ('TE', 24)]

def main():
    df = pd.read_csv('./data/fantasy_merged_7_17.csv')
    df['Touch_g'] = (df.RushAtt + df.Tgt) / df.G
    df['PPR_g'] = df.PPR / df.G
    df['Yds_g'] = (df.RushYds + df.RecYds) / df.G

    df_dict = {}
    for pos, cutoff in positions:
        df_dict[pos] = df[(df.FantPos == pos) & (df.PosRk <= cutoff)].reset_index(drop=True)

    model_dict = {}
    for pos, cutoff in positions:
        model_dict[pos] = LinearRegression()
        X = df_dict[pos][['Touch_g', 'Yds_g']]
        y = df_dict[pos][['PPR_g']]
        model_dict[pos].fit(X, y)
        print(f'R-squared for {pos} regression: {model_dict[pos].score(X, y)}')
    print('')
    
    running = True
    while running:
        file = input('Add raw file? (Y/N) ').upper()
        if file == 'Y':
            path = str(input('Enter the full path of the csv file: '))
            players = pd.read_csv(path)
            results = {'Player': [], 'Position': [], 'Projection': []}
            for i in range(players.shape[0]):
                name = players['Player'][i]
                pos = players['Position'][i]
                touches = players['Touches_g'][i]
                yards = players['Yards_g'][i]
                proj = model_dict[pos].predict([[touches, yards]])
                
                results['Player'].append(name)
                results['Position'].append(pos)
                results['Projection'].append(float(proj))
            results = pd.DataFrame(results)
            results = results.sort_values(by=['Position', 'Projection'], ascending=[True, False])
            print(results)
            running = False
        else:
            player_name_input = str(input('What is your player\'s name? ')).title()
            position_input = str(input('Please enter your player\'s position (RB, WR, TE): ').upper())
            touch_g_input = float(input('What is your player\'s touches/g metric? '))
            yds_g_input = float(input('What is your player\'s yds/g metric? '))
            prediction = model_dict[position_input].predict([[touch_g_input, yds_g_input]])
            print(f'Fantasy PPG prediction for {player_name_input} ({position_input}): {prediction}')
            add_another = str(input('Add another player? (Y/N) ')).upper()
            if add_another == 'N':
                running = False


if __name__ == '__main__':
    main()