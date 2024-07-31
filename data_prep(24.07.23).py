#%%
import pandas as pd
# %%
# df1 = pd.read_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig')
df2 = pd.read_excel('관측소 정보 (1).xlsx')
# %%
df1.drop(columns=['index'], inplace=True)
# %%
df1.head()
# %%
# df1.drop(columns=['level_0'], inplace=True)
# # %%
# df1.drop(columns=['개수'], inplace=True)
# %%
df1.info()
# %%
df1.rename(columns={"관측소":"OBVP_NM", "관측일":"OBVP_DATE", "수층":"OBVP_DEPT",
                    "평균 수온(℃)":"MEAN_TEMP", "최고 수온(℃)":"HIGH_TEMP",
                    "최저 수온(℃)":"LOW_TEMP", "중앙 수온(℃)":"MID_TEMP",
                    "표준편차(℃)":"STD_TEMP"}, inplace=True)
# %%
print(df1.columns)
# %%
# df1.to_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig', index=False)
# %%
df1.head()
#%%
columns_to_merge = ['위도(°N)', '경도(°E)']
df3 = pd.merge(df1, df2[columns_to_merge], left_on= df1['OBVP_NM'], right_on=df2['관측소'])
# %%
df1.replace({"영덕(byd8a)":"영덕", "기장(bgj8a)":"기장", "삼척(bsc87)":"삼척"}, inplace=True)
# %%
df3.head(10)
# %%
df3.columns
# %%
df3.drop('key_0', axis='columns', inplace=True)
# %%
df3
# %%
df3.rename(columns={'위도(°N)':'OBVP_LAT', '경도(°E)':'OBVP_LON'}, inplace=True)
# %%
df3.info()
# %%
df3.replace({"영덕(byd8a)":"영덕", "기장(bgj8a)":"기장", "삼척(bsc87)":"기장"}, inplace=True)
# %%



#%%
df3.to_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig', index=False)
# %%
df11 = pd.read_csv('기장관측정보.csv')
df22 = pd.read_csv('삼척관측정보.csv')
df33 = pd.read_csv('영덕관측정보.csv')
# %%
df1 = pd.concat([df11, df22, df33])
# %%
df1.sort_values(by=['관측일'], inplace=True)
# %%
columns_to_merge = ['위도(°N)', '경도(°E)']

df3 = pd.merge(df1, df2[columns_to_merge], left_on=df1['관측소'], right_on=df2['관측소'])
# %%
df3.head(10)
# %%
df3.info()
# %%
df3.drop(columns=['key_0', '개수'], inplace=True)

# %%
df3.to_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig', index=False)
# %%
pd.to_datetime(df3['관측일'])
# %%
df3
# %%
df3.info()
# %%
df3.to_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig', index=False)
# %%
df3.rename(columns={'관측소':'OBVP_NM', '관측일':'OBVP_DATE', '수층':'OBVP_DEPT',
'평균 수온(℃)':'MEAN_TEMP'}, inplace=True )
# %%
df3.rename(columns={'최고 수온(℃)':'MAX_TEMP', '중앙 수온(℃)':'MID_TEMP', '표준편차(℃)':'STD_TEMP',
'위도(°N)':'OBVP_LON', '경도(°E)':'OBVP_LAT'}, inplace=True )
# %%
df3.to_csv('2013-2023_동해관측정보.csv', encoding='utf-8-sig', index=False)
# %%
