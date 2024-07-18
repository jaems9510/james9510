#%%
# ! 서버에서 보기 위한 터미널 명령어
# !터미널 - streamlit run .\dashboard.py --server.port 8888
#%%
import streamlit as st #dash 패키지
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import matplotlib as mpl #시각화 패키지
import matplotlib.pyplot as plt #한글 표기를 위한 패키지
import os
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')
# %%
# * layout 정의 및 dataframe 정의
st.set_page_config(page_title="연안 냉수대 시각화", page_icon=":bar_chart:", layout="wide")

st.title("  :bar_chart: 연안 냉수대 속보 데이터")
st.markdown('<style>jiv.bolck-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(fl, encoding="cp949")
if True:
    upload_dir = r"C:/Users/YS/st"
    df = pd.read_csv("C:/Users/YS/st/2010-2023년 냉수대속보데이터.csv", encoding="cp949")
    # os.chdir(upload_dir)
    df = pd.read_csv("./2010-2023년 냉수대속보데이터.csv", encoding="cp949")

df['CP_ISSUED_YMD'] = df['CP_ISSUED_YMD'].astype(str)
df['CP_WTCH_YMD'] = df['CP_WTCH_YMD'].astype(str)

df['CP_ISSUED_YMD'] = df['CP_ISSUED_YMD'].apply(lambda x: x.split('.')[0])
df['CP_WTCH_YMD'] = df['CP_WTCH_YMD'].apply(lambda x: x.split('.')[0])

df['CP_ISSUED_YMD'] = pd.to_datetime(df['CP_ISSUED_YMD'], format='%Y%m%d')
df['CP_WTCH_YMD'] = pd.to_datetime(df['CP_WTCH_YMD'], format='%Y%m%d')



#%%
col1, col2 = st.columns((2)) #streamlit 상에서 2x2 그래프 layout을 의미함

# Getting the min & max date    
startDate = pd.to_datetime(df["CP_WTCH_YMD"]).min()
endDate = pd.to_datetime(df["CP_WTCH_YMD"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["CP_WTCH_YMD"] >= date1) & (df["CP_WTCH_YMD"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")

# Create for Region
sar = st.sidebar.multiselect("Pick your Sar", df["CP_ISSUED_SAR_NM"].unique())
if not sar: #didn't select any sar situation
    df2 = df.copy()

else:
    df2 = df[df["CP_ISSUED_SAR_NM"].isin(sar)]

# Create for Observatory
obvp = st.sidebar.multiselect("Pick the Observatory", df2["CP_OBVP_NM"].unique())
if not obvp: #didn't select any observatory
    df3 = df2.copy()
else:
    df3 = df2[df2["CP_OBVP_NM"].isin(obvp)]


# %%
# ! 그래프 plot 과정

with col1:
    fig = make_subplots(rows=1, cols=1, subplot_titles=("시계열 그래프"))

    # Loop through selected observatories and plot their time series
    for obvp_nm in obvp:
        obvp_df = df3[df3['CP_OBVP_NM'] == obvp_nm]
        if not obvp_df.empty:
            fig.add_trace(go.Scatter(x=obvp_df['CP_WTCH_YMD'],
                                     y=obvp_df['CP_WTEM'],
                                     mode='lines',
                                     name=obvp_nm))

    # Update layout
    fig.update_layout(title_text="시계열 그래프", xaxis_title="날짜", yaxis_title="수온")
    
    margin=dict(l=50, r=50, t=50, b=50)
    # Render the plot
    st.plotly_chart(fig)

with col2:
    df3['Data_Count'] = df3.groupby('CP_OBVP_NM')['CP_OBVP_NM'].transform('size')

    df3['Name_Count_Str'] = df3.apply(lambda row: f"{row['CP_OBVP_NM']} ({row['Data_Count']})", axis=1)

    text = df3['Name_Count_Str'].astype(str)

# Plotly를 사용하여 Mapbox 지도 위에 데이터 시각화
    fig2 = go.Figure(go.Scattermapbox(
        lat=df3['CP_OBVP_LAT'],
        lon=df3['CP_OBVP_LON'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=df3['Data_Count'],  # 각 관측소에서 발령된 데이터 개수를 크기로 지정
            sizeref=2.0 * max(df3['Data_Count']) / (30 ** 2),
            sizemode='area',
            color=df3['CP_WTEM'],  # 평균 온도에 따라 색상 표시
            colorscale='bluyl_r',  # 색상 스케일 설정 #todo 
            opacity=0.8,  # 원의 투명도 설정
            colorbar=dict(title='최저 온도'),  # 색상 바 설정
        ),
        text=text,  # 각 포인트에 대한 텍스트 정보 설정
        hoverinfo='text',
    ))

    fig2.update_layout(
        title='냉수대 주의보 관측소 위치 및 데이터 시각화',
        mapbox=dict(
            style='carto-positron',
            center=dict(lat=df3['CP_OBVP_LAT'].mean(), lon=df3['CP_OBVP_LON'].mean()-1),  # 지도 중심 설정
            zoom=5
        ),
        margin=dict(l=50, r=50, t=50, b=50),
    )

    # Plotly 차트를 Streamlit에 표시합니다.
    st.plotly_chart(fig2)


# %%
chart1, chart2 = st.columns((2))
n_counts = df3.groupby('CP_ISSUED_SAR_NM')['CP_OBVP_NM'].nunique().reset_index()
with chart1:
    st.subheader('냉수대 발령 해수면 온도 분포도')
    fig3 = go.Figure(go.Histogram(x=df3['CP_WTEM']))

    fig3.update_layout(
        xaxis_title="온도",
        yaxis_title="개수"
    )

    st.plotly_chart(fig3)

with chart2:
    st.subheader('관측소별 관측수온 분포도')
    fig4 = go.Figure(go.Box(x=df3['CP_OBVP_NM'],
                            y=df3["CP_WTEM"],
                            showlegend=False, opacity=0.5))
    st.plotly_chart(fig4)

# %%
