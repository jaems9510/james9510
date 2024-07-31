#%%
import pandas as pd
import numpy as np
# %%
df1 = pd.read_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig')
df2 = pd.read_csv('2010-2023년 냉수대속보데이터.csv', encoding='utf-8-sig')
# %%
df1.head(5)
df2.head(10)
# %%
df2.info()
# %%
df2['CP_ISSUED_YMD'] = df2['CP_ISSUED_YMD'].astype(str)
df2['CP_WTCH_YMD'] = df2['CP_WTCH_YMD'].astype(str)

df2['CP_ISSUED_YMD'] = df2['CP_ISSUED_YMD'].apply(lambda x: x.split('.')[0])
df2['CP_WTCH_YMD'] = df2['CP_WTCH_YMD'].apply(lambda x: x.split('.')[0])

df2['CP_ISSUED_YMD'] = pd.to_datetime(df2['CP_ISSUED_YMD'], format='%Y%m%d')
df2['CP_WTCH_YMD'] = pd.to_datetime(df2['CP_WTCH_YMD'], format='%Y%m%d')
# %%
# 연도와 월을 추출하여 새로운 컬럼 생성
df2['year_month'] = df2['CP_ISSUED_YMD'].dt.to_period('M')

# 연도-월별 발생 건수 계산
monthly_counts = df2['year_month'].value_counts().sort_index()

# 가장 많이 발생한 연도-월
monthly_counts_df = monthly_counts.reset_index()
monthly_counts_df.columns = ['year_month', 'count']
monthly_counts_df = monthly_counts_df.sort_values(by='count', ascending=False)

# 상위 10개 연도-월 출력
top_10_months = monthly_counts_df.head(10)
print("주의보나 경보가 가장 많이 발생한 상위 10개 연도-월:")
print(top_10_months)
# %%
"""주의보나 경보가 가장 많이 발생한 상위 10개 연도-월:
   year_month  count
11    2013-07    108
46    2023-06     54
35    2020-08     43
25    2018-06     43
41    2022-06     40
43    2022-08     32
47    2023-07     32
3     2010-08     28
42    2022-07     28
12    2013-08     24
"""
#%%
df1['OBVP_NM'].replace({"삼척(bsc87)":"삼척",
"기장(bgj8a):":"기장",
"영덕(byd8a)":"영덕"}, inplace=True)
#%%
df1['OBVP_NM'] = df1['OBVP_NM'].str.replace(r'\(.*\)', '', regex=True).str.strip()
# %%
df1.to_csv("2013-2023_동해관측정보.csv", encoding='utf-8-sig', index=False)
# %%
