import pandas as pd
import train_model

constraints = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'FLEX': 2}
def main():
    df = train_model.make_predictions()
    df['Is_Flex'] = df.FantPos.isin(['RB', 'WR', 'TE'])
    my_team = pd.read_csv('my_team.csv')
    df['My_Team'] = df.Player.isin(my_team.Player.str.title())
    running = True
    while running:
        print('''
        MODES:
        1. Show projection(s)
        2. Set my lineup
        3. Assess waivers
        4. Generate trade suggestions    
        ''')
        choice = input('Select your mode (enter a number): ')

        if choice == '1': 
            names = input('Enter the name(s) of your player(s) separated by commas: ')
            names = [name.title() for name in names.split(', ')]
            res = df.loc[df.Player.isin(names), ['Player', 'FantPos', 'Prediction']].sort_values(by=['FantPos', 'Prediction'], ascending=[True, False]).reset_index(drop=True)
            print(res)
            exit = input('Exit program? (Y/N) ')
            if exit.upper() == 'Y':
                running = False
        elif choice == '2': 
            # choices = df.loc[(df.My_Team == True), ['Player', 'FantPos', 'Prediction']].sort_values(by=['FantPos', 'Prediction'], ascending=[True, False])
            # lineup = {'QB': [], 'RB': [], 'WR': [], 'TE': [], 'FLEX': []}
            # for pos, limit in constraints.items():
            #     count = 0
            #     while count < limit:
            #         lineup[pos].append()
            pass                    
        elif choice == '3': 
            pass
        elif choice == '4': 
            pass
        else:
            print('Wrong choice')
    
if __name__ == '__main__':
    main()

