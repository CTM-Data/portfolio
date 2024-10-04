def get_ff_model(): 
    import pandas as pd
    import warnings
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    warnings.filterwarnings('ignore') 

    positions = [
        ('QB', ['PassAtt_g', 'PassYds_g', 'RushAtt_g', 'ScrmYds_g']), 
        ('RB', ['RushAtt_g', 'Targets_g', 'Catches_g', 'ScrmYds_g']), 
        ('WR', ['Targets_g', 'Catches_g', 'ScrmYds_g']), 
        ('TE', ['Targets_g', 'Catches_g', 'ScrmYds_g'])
    ]
    
    df = pd.read_csv('./training_data/ff_training_2017_2023.csv')
    df['PassAtt_g'] = df.Passing_Att / df.Games_G
    df['PassYds_g'] = df.Passing_Yds / df.Games_G
    df['RushAtt_g'] = df.Rushing_Att / df.Games_G
    df['Targets_g'] = df.Receiving_Tgt / df.Games_G
    df['Catches_g'] = df.Receiving_Rec / df.Games_G
    df['ScrmYds_g'] = (df.Rushing_Yds + df.Receiving_Yds) / df.Games_G
    df['PPR_g'] = df.Fantasy_PPR / df.Games_G
    #TODO: need to find a way to remove NAs from select columns given the position.
    models = {}
    for pos, cols in positions:
        x = df.loc[df.FantPos == pos, cols].reset_index(drop=True)
        y = df.loc[df.FantPos == pos, 'PPR_g'].reset_index(drop=True)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42)

        models[pos] = LinearRegression()
        models[pos].fit(X_train, y_train)
        print(f'R-squared for {pos}: {model_dict[pos].score(X_train, y_train)}')
    return model_dict