#%%
# ! 서버에서 보기 위한 터미널 명령어
# !터미널 - streamlit run .\dashboard(24.07.22).py --server.port 8888
# (py310) C:\Users\YS\240722>
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
st.set_page_config(page_title="2013-2023 동해 해표면 온도", page_icon=":bar_chart:", layout="wide")

st.title("  :bar_chart: 2013-2023 동해 해표면 온도")
st.markdown('<style>jiv.bolck-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

if True:
    # upload_dir = "https://github.com/jaems9510/james9510.git/"
    df1 = pd.read_csv("./2013-2023_동해관측정보.csv", encoding="utf-8-sig")
    df2 = pd.read_csv("./2013-2023년 냉수대속보데이터.csv", encoding="utf-8-sig")
    df3 = pd.read_csv("./2023년_동해관측정보.csv", encoding="utf-8-sig")
    df4 = pd.read_csv("./2023년06월_냉수대속보데이터.csv", encoding="utf-8-sig")


df1['OBVP_DATE'] = pd.to_datetime(df1['OBVP_DATE'], format='ISO8601')

df2['CP_ISSUED_YMD'] = df2['CP_ISSUED_YMD'].astype(str)
df2['CP_WTCH_YMD'] = df2['CP_WTCH_YMD'].astype(str)
df3['OBVP_DATE'] = df3['OBVP_DATE'].astype(str)


df2['CP_ISSUED_YMD'] = df2['CP_ISSUED_YMD'].apply(lambda x: x.split('.')[0])
df2['CP_WTCH_YMD'] = df2['CP_WTCH_YMD'].apply(lambda x: x.split('.')[0])
df3['OBVP_DATE'] = df3['OBVP_DATE'].apply(lambda x: x.split('.')[0])


df2['CP_ISSUED_YMD'] = pd.to_datetime(df2['CP_ISSUED_YMD'], format='%Y%m%d')
df2['CP_WTCH_YMD'] = pd.to_datetime(df2['CP_WTCH_YMD'], format='%Y%m%d')
# df3['OBVP_DATE'] = pd.to_datetime(df3['OBVP_DATE'])

df2['Data_Count'] = df2.groupby('CP_OBVP_NM')['CP_OBVP_NM'].transform('size')

df2['Name_Count_Str'] = df2.apply(lambda row: f"{row['CP_OBVP_NM']} ({row['Data_Count']})", axis=1)

text = df2['Name_Count_Str'].astype(str)
#%%
# * df2 sorting
sar_counts = df2['CP_ISSUED_SAR_NM'].value_counts()
df2['SAR_Count'] = df2['CP_ISSUED_SAR_NM'].map(sar_counts)

# CP_OBVP_NM 값의 개수를 기준으로 정렬
obvp_counts = df2.groupby('CP_ISSUED_SAR_NM')['CP_OBVP_NM'].value_counts()
df2['OBVP_Count'] = df2.apply(lambda x: obvp_counts[x['CP_ISSUED_SAR_NM']][x['CP_OBVP_NM']], axis=1)

# 두 개의 기준으로 정렬
df2 = df2.sort_values(by=['SAR_Count', 'OBVP_Count'], ascending=[False, False])
#%%
# * page_layout
col1, col2, col3 = st.columns((3))

# Getting the min & max date    
startDate = pd.to_datetime(df2["CP_WTCH_YMD"]).min()
endDate = pd.to_datetime(df2["CP_WTCH_YMD"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df2 = df2[(df2["CP_WTCH_YMD"] >= date1) & (df2["CP_WTCH_YMD"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")

# Create for Region
sar = st.sidebar.multiselect("Pick your Sar", df2["CP_ISSUED_SAR_NM"].unique())
if not sar: #didn't select any sar situation
    df22 = df2.copy()

else:
    df22 = df2[df2["CP_ISSUED_SAR_NM"].isin(sar)]

obvp1 = st.sidebar.multiselect("Pick the Observatory", df1["OBVP_NM"].unique())
if not obvp1: #didn't select any observatory
    df222 = df22.copy()
else:
    df222 = df22[df22["CP_OBVP_NM"].isin(obvp1)]
# Create for Observatory
obvp2 = st.sidebar.multiselect("Pick the Observatory", df2["CP_OBVP_NM"].unique())
if not obvp2: #didn't select any observatory
    df222 = df22.copy()
else:
    df222 = df22[df22["CP_OBVP_NM"].isin(obvp2)]


#%%
#  ! Plotly를 사용하여 Mapbox 지도 위에 데이터 시각화(fig1)

col1, col2, col3= st.columns((3))
with col1:
    st.subheader('냉수대 주의보 관측소 위치 및 데이터 시각화')
    fig1 = go.Figure(go.Scattermapbox(
    lat=df222['CP_OBVP_LAT'],
    lon=df222['CP_OBVP_LON'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=df222['Data_Count'],  # 각 관측소에서 발령된 데이터 개수를 크기로 지정
        sizeref=2.0 * max(df2['Data_Count']) / (30 ** 2),
        sizemode='area',
        color=df222['CP_WTEM'],  # 평균 온도에 따라 색상 표시
        colorscale='Inferno',  # 색상 스케일 설정
        opacity=1,  # 원의 투명도 설정
        colorbar=dict(title='최저 온도'),  # 색상 바 설정
        ),
        text=text,  # 각 포인트에 대한 텍스트 정보 설정
        hoverinfo='text',
    ))

    fig1.update_layout(
        mapbox=dict(
            style='carto-positron',
            center=dict(lat=df2['CP_OBVP_LAT'].mean(), lon=df2['CP_OBVP_LON'].mean()-1),  # 지도 중심 설정
            zoom=6.5
                    ),
        margin=dict(l=10, r=150, t=50, b=50),
        autosize=False, width=800, height=1000
    )

    # Plotly 차트를 Streamlit에 표시합니다.
    st.plotly_chart(fig1)

    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
#%%
# ! 실시간 해양수산환경 관측시스템의 10년치 시계열 자료(기장, 삼척, 영덕의 2013-2023년) (fig2, fig3)
with col2:
    st.subheader('2013-2023년 동해 해수면 온도 변화')
    fig2 = make_subplots(rows=1, cols=1)
    color_map = {station: color for station, color in zip(df1['OBVP_NM'].unique(), px.colors.qualitative.Plotly)}

    for station in df1['OBVP_NM'].unique():
        station_data = df1[df1['OBVP_NM'] == station]
        fig2.add_trace(go.Scatter(
            x=station_data['OBVP_DATE'],
            y=station_data['MEAN_TEMP'],
            mode='lines+markers',
            marker=dict(color=color_map[station], opacity=0.5),
            name=station
        ))

    fig2.update_layout(
        xaxis_title='날짜',
        yaxis_title='평균 온도',
        showlegend=True,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1년', step='year', stepmode='backward'),
                    dict(count=3, label='3년', step='year', stepmode='backward'),
                    dict(count=5, label='5년', step='year', stepmode='backward'),
                    dict(step='all'),
                ])
            ),
            rangeslider=dict(visible=True),
            type='date'
        ),
        margin=dict(l=10, r=50, t=50, b=50)
    )

    st.plotly_chart(fig2)
#%%
# ! fig3
# ! 냉수대 속보 발령, 해제 표시(xline)
# ! ㄴ df2 추가 => df4로 진행
with col3:
    fig3 = make_subplots(rows=1, cols=1)

    unique_observation_points = df4['OBVP_NM'].unique()

    for observation_point in unique_observation_points:
        observation_data = df4[df4['OBVP_NM'] == observation_point]
        if not observation_data.empty:
            fig3.add_trace(go.Scatter(
                x=observation_data['OBVP_DATE'],
                y=observation_data['MEAN_TEMP'],
                mode='lines+markers',
                name=observation_point
            ))

    # issuance_types = ['신규발령', '해제']
    # line_colors = {'신규발령': 'blue', '해제': 'red'}

    # for issuance_type in issuance_types:
    #     issuance_dates = df4[df4['CP_ISSUED_SITTN_NM'] == issuance_type]['CP_ISSUED_YMD'].unique()
    #     for issuance_date in issuance_dates:
    #         fig3.add_vline(
    #             x=issuance_date,
    #             line=dict(color=line_colors.get(issuance_type, 'black'), width=2),
    #             annotation_text=issuance_type if issuance_type != '해제' else None,
    #             annotation_position="top right" if issuance_type != '해제' else None
    #         )

    fig3.update_layout(
        xaxis_title="날짜",
        yaxis_title="수온",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    st.plotly_chart(fig3)

    # st.plotly_chart(fig_3)
    # with col3:
    #     df4['OBVP_DATE'] = pd.to_datetime(df4['OBVP_DATE'], format='%Y-%m-%d')
    #     df4['CP_ISSUED_YMD'] = pd.to_datetime(df4['CP_ISSUED_YMD'], format='%Y%m%d')
    #     df4['CP_WTCH_YMD'] = pd.to_datetime(df4['CP_WTCH_YMD'], format='%Y%m%d')

    #     # 서브플롯 생성
    #     fig3 = make_subplots(rows=1, cols=1)

    #     # 관측 지점의 고유값 가져오기
    #     obvp2 = df4['OBVP_NM'].unique()

    #     # 각 관측 지점에 대해 시간 시리즈 데이터 플로팅
    #     for obvp_nm in obvp2:
    #         obvp_df = df4[df4['OBVP_NM'] == obvp_nm]
    #         if not obvp_df.empty:
    #             fig3.add_trace(go.Scatter(x=obvp_df['OBVP_DATE'],
    #                                     y=obvp_df['MEAN_TEMP'],
    #                                     mode='lines+markers',
    #                                     name=obvp_nm))

    #     # 발령 유형 및 색상 정의
    #     issuance_types = ['신규발령', '해제']
    #     line_colors = {'신규발령': 'blue', '확대발령': 'orange', '대체발령': 'green', '해제': 'red'}

    #     # 발령 날짜에 대한 수직선 추가
    #     for issuance_type in issuance_types:
    #         issuance_dates = df4[df4['CP_ISSUED_SITTN_NM'] == issuance_type]['CP_ISSUED_YMD'].unique()
    #         for issuance_date in issuance_dates:
    #             fig3.add_vline(x=issuance_date,
    #                         line=dict(color=line_colors.get(issuance_type, 'black'), width=2),
    #                         annotation_text=issuance_type,
    #                         annotation_position="top right")

    #     # 레이아웃 업데이트
    #     fig3.update_layout(
    #         xaxis_title="날짜",
    #         yaxis_title="수온",
    #         margin=dict(l=50, r=50, t=50, b=50)
    #     )

        # 플롯 표시

#%%
# ! fig4
with col2:
    st.subheader('냉수대 발령 해수면 온도 분포도')

    # 카테고리 별로 히스토그램 생성
    histograms = []
    categories = df2['CP_ISSUED_SAR_NM'].unique()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']

    for i, category in enumerate(categories):
        category_data = df2[df2['CP_ISSUED_SAR_NM'] == category]['CP_WTEM']
        histograms.append(go.Histogram(
            x=category_data,
            name=category,
            marker=dict(color=colors[i]),
            opacity=0.75
        ))

    # 레이아웃 설정
    layout = go.Layout(
        xaxis_title="온도",
        yaxis_title="개수",
        barmode='overlay'
    )

    # Figure 생성
    fig4 = go.Figure(data=histograms, layout=layout)

    # 히스토그램 표시
    st.plotly_chart(fig4)
#%%
# ! fig5
with col3:
    st.subheader('관측소별 관측수온 분포도')

    # 카테고리 별로 박스 플롯 생성
    box_plots = []
    categories = df2['CP_ISSUED_SAR_NM'].unique()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']

    for i, category in enumerate(categories):
        category_data = df2[df2['CP_ISSUED_SAR_NM'] == category]
        box_plots.append(go.Box(
            x=category_data['CP_OBVP_NM'],
            y=category_data['CP_WTEM'],
            name=category,
            marker=dict(color=colors[i]),
            opacity=0.75
        ))

    # 레이아웃 설정
    layout = go.Layout(
        xaxis_title="관측소",
        yaxis_title="수온",
    )

    # Figure 생성
    fig5 = go.Figure(data=box_plots, layout=layout)

    # 박스 플롯 표시
    st.plotly_chart(fig5)








# %%
""" 
#todo 1. 23년 6월 + 속보(xline_(fig3)
#todo 4. colorscale 수정(blue-red, 10-25)(fig1)
"""
# %%
