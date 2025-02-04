import os
import pandas as pd
import scipy.stats as stats
import openpyxl
from datetime import datetime as dt

# define globals
file_path = 'rosters.xlsx'
sheet_name = 'my_team'
stat_cols = ['G', 'A', 'PTS', '+/-', 'PPP', 'FOW', 'SOG', 'HIT']
subset_cols = ['G', 'A', 'PTS', 'PPP', 'SOG', 'HIT']
total_subset_cols = [col + ' Total Z' for col in subset_cols]
pos_subset_cols = [col + ' Pos Z' for col in subset_cols]

df = pd.read_excel(file_path, sheet_name=sheet_name)

# ensure expected columns exist
expected_cols = {'Player', 'Position', 'GP', 'G', 'A', 'PTS', '+/-', 'PPP', 'FOW', 'SOG', 'HIT'}
missing_cols = expected_cols - set(df.columns)
if missing_cols:
    raise ValueError(f'Missing columns in the spreadsheet: {missing_cols}')

# drop players with 0 GP to avoid errors
df = df.loc[df['GP'] > 0]

# calculate per game statistics and zscores
for col in stat_cols:
    df[col + ' PG'] = df[col] / df['GP']
    df[col + ' Total Z'] = stats.zscore(df[col + ' PG'])
    df[col + ' Pos Z'] = df.groupby('Position')[col + ' PG'].transform(lambda x: stats.zscore(x))

# sum the zscores
df['Total Score'] = df.filter(like='Total Z').sum(axis=1)
df['Positional Score'] = df.filter(like='Pos Z').sum(axis=1)
df['Total Score Subset'] = df.filter(like='Total Z')[total_subset_cols].sum(axis=1)
df['Positional Score Subset'] = df.filter(like='Pos Z')[pos_subset_cols].sum(axis=1)

# filter out the columns I've added
drop_cols = [col for col in df.columns if 'Z' in col]
df = df.drop(columns=drop_cols)
col_order = ['Player', 'Position', 'Total Score', 'Positional Score', 'Total Score Subset', 'Positional Score Subset'] + [col for col in df.columns if col not in ['Player', 'Position', 'Total Score', 'Positional Score', 'Total Score Subset', 'Positional Score Subset']]
df = df[col_order]

# write resuls to original sheet
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name=sheet_name, index=False)

print('program complete on ', dt.now())