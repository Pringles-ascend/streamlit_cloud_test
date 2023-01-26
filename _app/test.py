import pandas as pd
import numpy as np

# df2 = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name='Trend', engine='openpyxl', header=1, nrows=4)

# print(df2)

# print(df2.loc[df2['구분']=='생산액'].values[0])

# df3 = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name='Trend', engine='openpyxl', header=8)

# print(df3)

# df_info = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', engine='openpyxl', sheet_name='info', header=None, index_col=0)

# print(df_info)

# print([value for value in df_info.loc['팀',:].values if value is not np.nan])
# print([value for value in df_info.loc['구분',:].values if value is not np.nan])

# lst_p = [value for value in df_info.loc['구분',:].values if value is not np.nan]

# for i in range(len(lst_p)):
#     df = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name=f'BW_{lst_p[i]}', engine='openpyxl', header=1, nrows=75, index_col=0)
#     df.dropna(how='all', inplace=True)

#     print(df.head(10))
#     df.index = df.index.str.lstrip()

#     print(df.loc['급료',:])

    
# team_name = [value for value in df_info.loc['팀',:].values if value is not np.nan][0]
# print(team_name)



ndar1 = np.array([1,2,3,4,5])
ndar2 = np.array([2,3,4,5,6])

ndar3 = ndar1 / ndar2
print(ndar3)