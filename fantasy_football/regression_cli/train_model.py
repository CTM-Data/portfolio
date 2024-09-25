def get_ff_model(): 
    import pandas as pd
    import warnings
    from sklearn.linear_model import LinearRegression
    warnings.filterwarnings('ignore') 

    positions = [('RB', 60), ('WR', 72), ('TE', 24)]
    df = pd.read_csv('./training_data/ff_training_2017_2023.csv')

    df_dict = {}
    for pos, cutoff in positions:
        df_dict[pos] = df[(df.FantPos == pos) & (df.Fantasy_PosRank <= cutoff)].reset_index(drop=True)

    model_dict = {}
    for pos, cutoff in positions:
        model_dict[pos] = LinearRegression()
        X = df_dict[pos][['Opps_g', 'ScrmYds_g']]
        y = df_dict[pos][['Fantasy_PPR_g']]
        model_dict[pos].fit(X, y)
        print(f'R-squared for {pos} regression: {model_dict[pos].score(X, y)}')
    return model_dict