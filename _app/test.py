import pandas as pd

path = r'M:\Users\LGCARE\Documents\download\SAP5WIRSLW8HK3NZESFI3SJ0H7SK.xls'

df = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', engine='openpyxl', header=17)
df = df.drop(index=0)

print(df)

print(df.columns)
print(type(df.columns))

df.columns = df.columns.str.replace('\n', ' ')
df.columns = df.columns.str.replace('Unnamed: 0', '구분')
df['구분'] = df['구분'].str.lstrip()


print(df)

# print(type(df['구분'][75][0]))
# print(df['구분'][75][1])
# print(df['구분'][1][2])
# print(df['구분'][1][3])
# print(df['구분'][1][4])
# print(df['구분'][1][5])

print(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][0])


df2 = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name='Trend', engine='openpyxl')

print(df2.loc[df2['구분']=='생산액'].values[0])