import pandas as pd

# define globals
file_path = 'rosters.xlsx'
my_sheet_name = 'my_team'
opp_sheet_name = 'opponent'
stat_cols = ['G', 'A', 'PTS', '+/-', 'PPP', 'FOW', 'SOG', 'HIT']

# read in rosters
my_team = pd.read_excel(file_path, sheet_name=my_sheet_name)
opp_team = pd.read_excel(file_path, sheet_name=opp_sheet_name)

# ensure expected columns exist
expected_cols = {'Player', 'Position', 'GP', 'G', 'A', 'PTS', '+/-', 'PPP', 'FOW', 'SOG', 'HIT'}
missing_cols_my_team = expected_cols - set(my_team.columns)
missing_cols_opp_team = expected_cols - set(opp_team.columns)

if missing_cols_my_team:
    raise ValueError(f'Missing columns in the spreadsheet: {missing_cols_my_team}')
if missing_cols_opp_team:
    raise ValueError(f'Missing columns in the spreadsheet: {missing_cols_opp_team}')

# add per game stats
for col in stat_cols:
    my_team[col + ' PG'] = my_team[col] / my_team['GP']
    opp_team[col + ' PG'] = opp_team[col] / opp_team['GP']

# aggregate total performance statistics 
my_totals = my_team[stat_cols + [col + ' PG' for col in stat_cols]].mean()
opp_totals = opp_team[stat_cols + [col + ' PG' for col in stat_cols]].mean()

category_comparison = pd.DataFrame({
    'Category': stat_cols,
    'My Team PG': my_totals[[col + ' PG' for col in stat_cols]].values,
    'Opp Team PG': opp_totals[[col + ' PG' for col in stat_cols]].values
})
category_comparison['difference'] = category_comparison['My Team PG'] - category_comparison['Opp Team PG']

def get_recommendation(diff):
    if diff > 0.3:
        return 'WAY AHEAD'
    elif 0.1 <= diff <= 0.3:
        return 'REINFORCE'
    elif -0.1 < diff < 0.1:
        return 'CONTEST'
    elif -0.3 <= diff <= -0.1:
        return 'CONSIDER'
    else:
        return 'IGNORE'

category_comparison['recommendation'] = category_comparison['difference'].apply(get_recommendation)
category_comparison = category_comparison.sort_values(by='difference')

# write resuls to original sheet
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    category_comparison.to_excel(writer, sheet_name='comparision', index=False)