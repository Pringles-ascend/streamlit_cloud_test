import streamlit as st
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from streamlit_extras.chart_container import chart_container



st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout="wide")

st.markdown("# 제조원가 분석 test version")
st.sidebar.header("파일 업로드")
st.write(
    """....제조원가 분석 WEB page 테스트 버전 입니다...."""
)



with st.sidebar:
    amount_unit = st.radio(" ", options=('물량', '수량'), label_visibility='hidden', key='amount_unit', horizontal=True)
    uploaded_file = st.file_uploader("양식 파일을 업로드해주세요", type="xlsx")
    

if uploaded_file is not None:
    
    df_info = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', engine='openpyxl', sheet_name='info', header=None, index_col=0)
    team_name = [value for value in df_info.loc['팀',:].values if value is not np.nan][0]
    prod_family = [value for value in df_info.loc['구분',:].values if value is not np.nan]

    tabs = st.tabs(prod_family)


    for idx, prod in enumerate(prod_family):
        df_BW_PY = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name=f'BW_{prod_family[idx]}', engine='openpyxl', header=1, nrows=75, index_col=0)
        # df_BW_PY.dropna(how='all', inplace=True)
        df_BW_PY.fillna(0, inplace=True)
        df_BW_PY.index = df_BW_PY.index.str.lstrip()

        df_BW_CY = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name=f'BW_{prod_family[idx]}', engine='openpyxl', header=80, nrows=75, index_col=0)
        # df_BW_CY.dropna(how='all', inplace=True)
        df_BW_CY.fillna(0, inplace=True)
        df_BW_CY.index = df_BW_CY.index.str.lstrip()


        df_trend_PY = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name=f'Trend_{prod_family[idx]}', engine='openpyxl', header=1, nrows=7, index_col=1)
        df_trend_PY.dropna(how='all', inplace=True)
        df_trend_PY.fillna(0, inplace=True)
        df_trend_PY.drop(['단위'], inplace=True, axis=1)

        df_trend_CY = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name=f'Trend_{prod_family[idx]}', engine='openpyxl', header=11, nrows=9, index_col=1)
        df_trend_CY.dropna(how='all', inplace=True)
        df_trend_CY.fillna(0, inplace=True)
        df_trend_CY.drop(['단위'], inplace=True, axis=1)
        

        print(df_trend_PY)

        if amount_unit == '물량':
            df_trend_PY.loc['생산량',:] = df_trend_PY.loc['생산물량', :]
            df_trend_CY.loc['생산량',:] = df_trend_CY.loc['생산물량', :]

        if amount_unit == '수량':
            df_trend_PY.loc['생산량',:] = df_trend_PY.loc['생산수량', :]
            df_trend_CY.loc['생산량',:] = df_trend_CY.loc['생산수량', :]

        df_trend_PY.loc['인시당 생산성',:] = df_trend_PY.loc['생산량', :] / (df_trend_PY.loc['자사_Mhr', :] + df_trend_PY.loc['외주_Mhr', :])
        df_trend_CY.loc['인시당 생산성',:] = df_trend_CY.loc['생산량', :] / (df_trend_CY.loc['자사_Mhr', :] + df_trend_CY.loc['외주_Mhr', :])

        print(df_trend_CY)

        
        
        with tabs[idx]:
            lst_Y = ['그래프','당월','누계']
            tabs_Y = st.tabs(lst_Y)


            ### 당월 분석 TAB ###
            with tabs_Y[1]:
                
                col_month_slider= st.columns(4)

                with col_month_slider[0]:

                    len_month = len(df_BW_CY.loc[['생산액']].values[0])
                    selected_month = st.select_slider(
                        '분석 월 을 선택하세요',
                        options=[f'{i}월' for i in range(1, len_month+1)], key=f'selected_month_{prod_family[idx]}',
                        value=f'{len_month}월'
                        ),

                    st.write('선택 월: ', selected_month[0][0:-1])
                    num_selected_month = int(selected_month[0][0:-1])
                    print(num_selected_month)




                #### 생산액: Column A ####
                col_a1, col_a2, col_a3, col_a4, col_a_empty3 = st.columns([4, 4, 4, 4, 1], gap="small")

                with col_a1:

                    if num_selected_month == 1:
    
                        value_1 = format(round(df_BW_PY.loc[['생산액'], ['12월']].values[0][0]/100_000_000, 1), ',f')
                    else:
                        value_1 = format(round(df_BW_CY.loc[['생산액'], [f'{num_selected_month-1}월']].values[0][0]/100_000_000, 1), ',f')
                    value_2 = format(round(df_BW_CY.loc[['생산액'], [f'{num_selected_month}월']].values[0][0]/100_000_000, 1), ',f')

                    fvalue_1 = float(value_1)
                    fvalue_2 = float(value_2)

                    differ = fvalue_2/fvalue_1 - 1
                    ndiffer = fvalue_2 - fvalue_1                    
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전월', x=['전월'], y=[value_1],
                        text=[f'{fvalue_1:,.1f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전월: %{y:.1f}<extra></extra>',
                        ),

                        go.Bar(name='당월', x=['당월'], y=[value_2],
                        text=[f'{fvalue_2:,.1f}' if differ >=0 else f'{fvalue_2}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당월: %{y:.1f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "생산액_당월",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>생산액(억원)</b>",
                            
                            annotations=[dict(
                                x='당월',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.1f}<br>(+{differ:.1%})</b>' if differ >=0 else f'<b>{ndiffer:,.1f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                            
                            
                            )

                    # fig.update_annotations(
                    #     x="당월",
                    #     y=75,
                    #     text='TESTTTTTTTTTTT',
                    #     # valign='top',
                    #     )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=True, theme=None)


                # with col_a_empty1:
                #     st.empty()

                with col_a2:

                    if num_selected_month == 1:
    
                        value_1 = round(df_trend_PY.loc[['생산량'], ['12월']].values[0][0]/1_000, 0)
                    else:
                        value_1 = round(df_trend_CY.loc[['생산량'], [f'{num_selected_month-1}월']].values[0][0]/1_000, 0)
                        print(value_1)
                        print(type(value_1))
                    value_2 = round(df_trend_CY.loc[['생산량'], [f'{num_selected_month}월']].values[0][0]/1_000, 0)

                    fvalue_1 = float(value_1)
                    fvalue_2 = float(value_2)

                    differ = fvalue_2/fvalue_1 - 1
                    ndiffer = fvalue_2 - fvalue_1


                    fig = go.Figure(data=[
                        go.Bar(name='전월', x=['전월'], y=[value_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전월: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='당월', x=['당월'], y=[value_2],
                        text=[f'{fvalue_2:,.0f}' if differ >=0 else f'{fvalue_2}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당월: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "생산량_당월",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>생산량(톤)</b>",
                            
                            annotations=[dict(
                                x='당월',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.0f}<br>(+{differ:.1%})</b>' if differ >=0 else f'<b>{ndiffer:,.0f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )],
                            yaxis_tickformat = ','
                            
                            )

                    # fig.update_annotations(
                    #     x="당월",
                    #     y=75,
                    #     text='TESTTTTTTTTTTT',
                    #     # valign='top',
                    #     )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=True, theme=None)

                # with col_a_empty2:
                #     st.empty()

                with col_a3:

                    if num_selected_month == 1:
    
                        value_1 = round(df_trend_PY.loc[['제조원가율'], ['12월']].values[0][0], 3)
                    else:
                        value_1 = round(df_trend_CY.loc[['제조원가율'], [f'{num_selected_month-1}월']].values[0][0], 3)
                        print(value_1)
                        print(type(value_1))
                    value_2 = round(df_trend_CY.loc[['제조원가율'], [f'{num_selected_month}월']].values[0][0], 3)

                    fvalue_1 = float(value_1)
                    fvalue_2 = float(value_2)

                    differ = fvalue_2 - fvalue_1



                    fig = go.Figure(data=[
                        go.Bar(name='전월', x=['전월'], y=[value_1],
                        text=[f'{fvalue_1:,.1%}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전월: %{y:.1%}<extra></extra>',
                        ),

                        go.Bar(name='당월', x=['당월'], y=[value_2],
                        text=[f'{fvalue_2:,.1%}' if differ >=0 else f'{fvalue_2:,.1%}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당월: %{y:.1%}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "제조원가율_당월",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>제조원가율(%)</b>",
                            
                            annotations=[dict(
                                x='당월',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'+{differ:.1%}p' if differ >=0 else f'{differ:.1%}p',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                            
                            
                            )

                    # fig.update_annotations(
                    #     x="당월",
                    #     y=75,
                    #     text='TESTTTTTTTTTTT',
                    #     # valign='top',
                    #     )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=True, theme=None)

                with col_a4:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전월', x=['전월'], y=[value_1],
                        text=[f'{fvalue_1:,.1f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전월: %{y:.1f}<extra></extra>',
                        ),

                        go.Bar(name='당월', x=['당월'], y=[value_2],
                        text=[f'{fvalue_2:,.1f}' if differ >=0 else f'{fvalue_2}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당월: %{y:.1f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "생산액_당월",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>생산액(억원)</b>",
                            
                            annotations=[dict(
                                x='당월',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.1f}<br>(+{differ:.1%})</b>' if differ >=0 else f'<b>{ndiffer:,.1f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                            
                            
                            )

                    # fig.update_annotations(
                    #     x="당월",
                    #     y=75,
                    #     text='TESTTTTTTTTTTT',
                    #     # valign='top',
                    #     )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=True, theme=None)
                
                df_total = pd.DataFrame(columns=['구분','금액_전기','구성비_전기','금액_당기','구성비_당기','증감금액','구성비_증감'])
                

                index_total = ['실질 생산액','원재료비','용기/포장비','전력/연료비','외주가공비','기타','변동비 계',\
                    '임금/급료','제조관리 인건비','감가상각비','소모/수선비','경상개발비','반제품차','기 타', '고정비 계','제조원가']
                df_total['구분'] = index_total
                df_total.set_index('구분', inplace=True)

                

                if num_selected_month == 1:
                    df_total.loc[:,'금액_전기'] = np.array(
                        [df_BW_PY.loc['생산액', [f'12월']].values[0],
                        df_BW_PY.loc['원재료비', [f'12월']].values[0] + df_BW_PY.loc['재료비:상품', [f'12월']].values[0],
                        df_BW_PY.loc['용기부품비', [f'12월']].values[0] + df_BW_PY.loc['매입부품비', [f'12월']].values[0] + df_BW_PY.loc['포장비', [f'12월']].values[0],
                        df_BW_PY.loc['전력비', [f'12월']].values[0] + df_BW_PY.loc['연료비', [f'12월']].values[0],
                        df_BW_PY.loc['외주가공비', [f'12월']].values[0] + df_BW_PY.loc['사외 외주가공비', [f'12월']].values[0],
                        df_BW_PY.loc['소모품비', [f'12월']].values[0] + df_BW_PY.loc['사용료', [f'12월']].values[0] + df_BW_PY.loc['세금과공과', [f'12월']].values[0],
                        0,
                        df_BW_PY.loc['급료', [f'12월']].values[0] + df_BW_PY.loc['임금', [f'12월']].values[0]+ df_BW_PY.loc['상여금', [f'12월']].values[0]+df_BW_PY.loc['퇴직급여', [f'12월']].values[0]+df_BW_PY.loc['복리후생비', [f'12월']].values[0],
                        df_BW_PY.loc['청주.제조관리-인건비', [f'12월']].values[0]+df_BW_PY.loc['청주.간접 인건비', [f'12월']].values[0],
                        df_BW_PY.loc['감가상각비', [f'12월']].values[0]+df_BW_PY.loc['무형상각비', [f'12월']].values[0],
                        df_BW_PY.loc['수선비', [f'12월']].values[0] + df_BW_PY.loc['소모품비', [f'12월']].values[0],
                        df_BW_PY.loc['경상개발비', [f'12월']].values[0],
                        df_BW_PY.loc['기초 반제품 재고', [f'12월']].values[0] + df_BW_PY.loc['타계정 대체', [f'12월']].values[0] - df_BW_PY.loc['기말 반제품 재고', [f'12월']].values[0],
                        df_BW_PY.loc[['여비교통비','통신비','수도광열비','임차료','지급용역료','차량관리비','보험료','교제비','광고비','운반비','도서인쇄비','교육훈련비','회의비','연구비','잡비','청주.제조관리-상각비','청주.제조관리-기타'], [f'12월']].values.sum(),
                        0,
                        0])/1_000_000
                    
                else:
                    
                    df_total.loc[:,'금액_전기'] = np.array(
                        [df_BW_CY.loc['생산액', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['원재료비', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['재료비:상품', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['용기부품비', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['매입부품비', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['포장비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['전력비', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['연료비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['외주가공비', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['사외 외주가공비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['사용료', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['세금과공과', [f'{num_selected_month-1}월']].values[0],
                        0,
                        df_BW_CY.loc['급료', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['임금', [f'{num_selected_month-1}월']].values[0]+ df_BW_CY.loc['상여금', [f'{num_selected_month-1}월']].values[0]+df_BW_CY.loc['퇴직급여', [f'{num_selected_month-1}월']].values[0]+df_BW_CY.loc['복리후생비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['청주.제조관리-인건비', [f'{num_selected_month-1}월']].values[0]+df_BW_CY.loc['청주.간접 인건비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['감가상각비', [f'{num_selected_month-1}월']].values[0]+df_BW_CY.loc['무형상각비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['수선비', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['소모품비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['경상개발비', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc['기초 반제품 재고', [f'{num_selected_month-1}월']].values[0] + df_BW_CY.loc['타계정 대체', [f'{num_selected_month-1}월']].values[0] - df_BW_CY.loc['기말 반제품 재고', [f'{num_selected_month-1}월']].values[0],
                        df_BW_CY.loc[['여비교통비','통신비','수도광열비','임차료','지급수수료','지급용역료','차량관리비','보험료','교제비','광고비','운반비','도서인쇄비','교육훈련비','회의비','연구비','잡비','청주.제조관리-상각비','청주.제조관리-기타','청주.간접 기타'], [f'{num_selected_month-1}월']].values.sum(),
                        0,
                        0])/1_000_000

                df_total.loc[:,'금액_당기'] = np.array(
                    [df_BW_CY.loc['생산액', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['원재료비', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['재료비:상품', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['용기부품비', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['매입부품비', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['포장비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['전력비', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['연료비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['외주가공비', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['사외 외주가공비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['사용료', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['세금과공과', [f'{num_selected_month}월']].values[0],
                    0,
                    df_BW_CY.loc['급료', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['임금', [f'{num_selected_month}월']].values[0]+ df_BW_CY.loc['상여금', [f'{num_selected_month}월']].values[0]+df_BW_CY.loc['퇴직급여', [f'{num_selected_month}월']].values[0]+df_BW_CY.loc['복리후생비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['청주.제조관리-인건비', [f'{num_selected_month}월']].values[0]+df_BW_CY.loc['청주.간접 인건비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['감가상각비', [f'{num_selected_month}월']].values[0]+df_BW_CY.loc['무형상각비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['수선비', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['소모품비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['경상개발비', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc['기초 반제품 재고', [f'{num_selected_month}월']].values[0] + df_BW_CY.loc['타계정 대체', [f'{num_selected_month}월']].values[0] - df_BW_CY.loc['기말 반제품 재고', [f'{num_selected_month}월']].values[0],
                    df_BW_CY.loc[['여비교통비','통신비','수도광열비','임차료','지급수수료','지급용역료','차량관리비','보험료','교제비','광고비','운반비','도서인쇄비','교육훈련비','회의비','연구비','잡비','청주.제조관리-상각비','청주.제조관리-기타','청주.간접 기타'], [f'{num_selected_month}월']].values.sum(),
                    0,
                    0])/1_000_000

                if num_selected_month == 1:
                    df_total.loc[:,'구성비_전기'] = df_total.loc[:,'금액_전기'] / df_BW_PY.loc['생산액', [f'12월']].values[0] *100 * 1_000_000
                else:
                    df_total.loc[:,'구성비_전기'] = df_total.loc[:,'금액_전기'] / df_BW_CY.loc['생산액', [f'{num_selected_month-1}월']].values[0] *100 * 1_000_000
                df_total.loc[:,'구성비_당기'] = df_total.loc[:,'금액_당기'] / df_BW_CY.loc['생산액', [f'{num_selected_month}월']].values[0] *100 * 1_000_000
                df_total.loc[:,'증감금액'] = df_total.loc[:,'금액_당기'] - df_total.loc[:,'금액_전기']
                df_total.loc[:,'구성비_증감'] = df_total.loc[:,'구성비_당기'] - df_total.loc[:,'구성비_전기']

                df_total.loc['변동비 계',:] = df_total.loc[['원재료비','용기/포장비','전력/연료비','외주가공비','기타'],:].sum()
                df_total.loc['고정비 계',:] = df_total.loc[['임금/급료','제조관리 인건비','감가상각비','소모/수선비','경상개발비','반제품차','기 타'],:].sum()
                df_total.loc['제조원가',:] = df_total.loc[['변동비 계','고정비 계'],:].sum()

                ### 제조원가 분석 표 ###
                df_anl = pd.DataFrame(columns=['구분','항목','증가요인','감소요인','계'])
                df_anl.loc[:,'구분'] = ['전기', '외부요인', '', '', '', '', '', '',\
                    '공장요인', '', '', '', '', '', '', '', '', '당기']
                df_anl.loc[:,'항목'] = ['전기','원부자재','P-Mix차','고정비영향','판가영향','외주가공비','기타','외부요인 소계',\
                    '원가절감','외주가공비','인건비','전력/연료비','소모수선비','소모수선비','기 타','기 타','공장요인 소계','당기']

                df_anl.set_index('구분', inplace=True)


                ### draw pandas table ###
                # print(df_total)

                # df_total.reset_index().loc[:4].style.set_properties(**{'background-color': 'white',
                #             'color': 'lawngreen',
                #             'border-color': 'white'})
                # st.write("증감 분석")
                # st.dataframe(df_total.reset_index().style.format({'구성비_전기':'{:,.1f}', '구성비_당기':'{:,.1f}', '구성비_증감':'{:,.1f}', '금액_전기':'{:,.0f}', '금액_당기':'{:,.0f}', '증감금액':'{:,.0f}'})\
                #     .set_properties(subset = pd.IndexSlice[[0], :], **{'background-color' : 'rgb(190,200,255)', 'font-weight': 'bold', 'border-color': 'white'}, color="black")\
                #     .set_properties(subset = pd.IndexSlice[[6,14], :], **{'background-color' : 'orange',"font-weight": "bold"}, color="black")\
                #     .set_properties(subset = pd.IndexSlice[[15], :], **{'background-color' : 'green'}, color="black", **{"font-weight": "bold"})\
                #     .set_properties(subset = pd.IndexSlice[[1,2], :], **{'background-color' : 'white'}, color="black", **{"font-weight": "bold"})\
                #     .set_properties(**{'font-size': '25pt'})\
                #     .hide(axis='index'), height=598
                # )
                
                def display_table(df, fit_columns_on_grid_load=False, sidebar=True, height=500, key=None):
                    gb = GridOptionsBuilder.from_dataframe(df)

                    if sidebar:
                        gb.configure_side_bar()
                    
                    gb.configure_grid_options(
                        enableRangeSelection=True,
                        rowSelection='multiple',
                        rowMultiSelectWithClick=True,
                        suppressFieldDotNotation=True, autoSizeAllColumns=True,
                    )
                    
                    jscode = JsCode("""                                             
                        function(params) {
                            if (params.data.구분 ===("실질 생산액")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'rgb(190,200,255)',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'

                                }
                            }
                            if (params.data.구분 ===("변동비 계") || params.data.구분 === ("고정비 계")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'orange',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'
                                }
                            }
                            if (params.data.구분 ===("제조원가")) {
                                return {
                                    'color': 'white',
                                    'backgroundColor': 'green',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'
                                }
                            }                      
                        };               
                        
                    """)

                    custom_css = {
                        ".ag-theme-balham-dark": {"--ag-header-foreground-color": "white"},
                        ".ag-header-cell-label": {"justify-content": "center", "font-size": '12px'},
                        "body": {"text-align": "center"}
                        }



                    gb.configure_default_column(min_column_width=10, headerClass={'header-background-color': 'deeppink'}, cellStyle={'border': '0.000001px groove','border-color':'Silver'}, editable=True, )
                    # gb.configure_default_column(min_column_width=10, headerClass={'align': "ag-center-aligned-header"}, cellStyle={'border': '0.000001px groove'})

                    # gb.configure_columns(column_names=df.columns, initialWidth=100, resizable=True, flex=5)
                    gb.configure_columns(column_names=df.columns, resizable=True,)
                    gb.configure_column("구분", width=110, suppressMenu=True, )
                    gb.configure_column("금액_전기", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.금액_전기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("금액_당기", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.금액_당기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("증감금액", type=["numericColumn",], width=76, suppressMenu=True, valueGetter="data.증감금액.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("구성비_전기", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.구성비_전기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("구성비_당기", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.구성비_당기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("구성비_증감", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.구성비_증감.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    
                    # gb.configure_column("금액_전기", editable=True)

                    

                    gridOptions = gb.build()
                    print(jscode)
                    print(gridOptions)
                    gridOptions['getRowStyle'] = jscode
                    

                    return AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, height=height, fit_columns_on_grid_load=fit_columns_on_grid_load, key=key, allow_unsafe_jscode=True,\
                        theme='balham', update_mode=GridUpdateMode.NO_UPDATE,custom_css=custom_css, reload_data=True)

                    # return AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, width='80%', height=height, fit_columns_on_grid_load=fit_columns_on_grid_load, key=key, allow_unsafe_jscode=True,\
                    #     theme='streamlit', update_mode=GridUpdateMode.NO_UPDATE, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)  

                def display_table2(df, fit_columns_on_grid_load=False, sidebar=True, height=500, key=None):
                    gb = GridOptionsBuilder.from_dataframe(df)

                    if sidebar:
                        gb.configure_side_bar()
                    
                    gb.configure_grid_options(
                        enableRangeSelection=True,
                        rowSelection='multiple',
                        rowMultiSelectWithClick=True,
                        suppressFieldDotNotation=True, autoSizeAllColumns=True,
                    )
                    
                    jscode = JsCode("""                                             
                        function(params) {
                            if (params.data.구분 ===("실질 생산액")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'rgb(190,200,255)',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'

                                }
                            }
                            if (params.data.구분 ===("변동비 계") || params.data.구분 === ("고정비 계")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'orange',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'
                                }
                            }
                            if (params.data.구분 ===("제조원가")) {
                                return {
                                    'color': 'white',
                                    'backgroundColor': 'green',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'
                                }
                            }                      
                        };               
                        
                    """)

                    custom_css = {
                        ".ag-theme-balham-dark": {"--ag-header-foreground-color": "white"},
                        ".ag-header-cell-label": {"justify-content": "center", "font-size": '12px'},
                        "body": {"text-align": "center"},
                        ".cell-span": {"background-color": "#0E1117", 'border-bottom': 'solid 0.5px', 'border-bottom-color':'#303239'},
                        }
                    
                    string_to_add_row = "\n\n function(e) { \n \
                        let api = e.api; \n \
                        let rowIndex = e.rowIndex + 1; \n \
                        api.applyTransaction({addIndex: rowIndex, add: [{}]}); \n \
                        api.deselectAll(); \n \
                        api.refreshCells({force : true}); \n \
                            }; \n \n"

                    cell_button_add = JsCode('''
                        class BtnAddCellRenderer {
                            init(params) {
                                this.params = params;
                                this.eGui = document.createElement('div');
                                this.eGui.innerHTML = `
                                <span>
                                    <style>
                                    .btn_add {
                                    background-color: limegreen;
                                    border: none;
                                    color: white;
                                    text-align: center;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 10px;
                                    font-weight: bold;
                                    height: 2.5em;
                                    width: 2.5em;
                                    cursor: pointer;
                                    }

                                    .btn_add :hover {
                                    background-color: #515754;
                                    }
                                    </style>
                                    <button id='click-button' 
                                        class="btn_add" 
                                        >➕</button>
                                </span>
                            `;
                            }

                            getGui() {
                                return this.eGui;
                            }

                        };
                        ''')


                    string_to_delete = "\n\n function(e) { \n \
                        let api = e.api; \n \
                        let sel = api.getSelectedRows(); \n \
                        api.applyTransaction({remove: sel}); \n \
                        api.refreshCells({force : true}); \n \
                            }; \n \n"

                    cell_button_delete = JsCode('''
                        class BtnCellRenderer {
                            init(params) {
                                console.log(params.api.getSelectedRows());
                                this.params = params;
                                this.eGui = document.createElement('div');
                                this.eGui.innerHTML = `
                                <span>
                                    <style>
                                    .btn {
                                    background-color: #F94721;
                                    border: none;
                                    color: white;
                                    text-align: left;
                                    text-decoration: none;
                                    display: inline-block;
                                    font-size: 10px;
                                    font-weight: none;
                                    height: 2.5em;
                                    width: 3.5em;
                                    cursor: pointer;
                                    }

                                    .btn:hover {
                                    background-color: #FB6747;
                                    }
                                    </style>
                                    <button id='click-button'
                                        class="btn"
                                        >🗑️</button>
                                </span>
                            `;
                            }

                            getGui() {
                                return this.eGui;
                            }

                        };
                        ''')


  


                    ### Checkbox Column ###

                    # checkbox_renderer = JsCode("""
                    #     class CheckboxRenderer{

                    #         init(params) {
                    #             this.params = params;

                    #             this.eGui = document.createElement('input');
                    #             this.eGui.type = 'checkbox';
                    #             this.eGui.checked = params.value;

                    #             this.checkedHandler = this.checkedHandler.bind(this);
                    #             this.eGui.addEventListener('click', this.checkedHandler);
                    #         }

                    #         checkedHandler(e) {
                    #             let checked = e.target.checked;
                    #             let colId = this.params.column.colId;
                    #             this.params.node.setDataValue(colId, checked);
                    #         }

                    #         getGui(params) {
                    #             return this.eGui;
                    #         }

                    #         destroy(params) {
                    #         this.eGui.removeEventListener('click', this.checkedHandler);
                    #         }
                    #     }//end class
                    #     """)
                    #
                    # gb.configure_column('  ', editable=True, width=40,lockPosition='left', headerCheckboxSelection=True, checkboxSelection=True, cellStyle={'padding-left': '10px', 'padding-right': '10px', })

                    gb.configure_column('', headerTooltip='Click on Button to add new row', editable=False, filter=False,\
                        onCellClicked=JsCode(string_to_add_row), cellRenderer=cell_button_add,\
                        autoHeight=True, wrapText=True, lockPosition='left', width=26, suppressMenu=True, cellStyle={'padding-left': '0px', 'padding-right': '0px', })
                    
                    gb.configure_column(' ', headerTooltip='Click on Button to remove row',\
                        editable=False, filter=False, onCellClicked=JsCode(string_to_delete),\
                        cellRenderer=cell_button_delete, autoHeight=True, suppressMovable='true', width=38, suppressMenu=True, cellStyle={'padding-left': '0px', 'padding-right': '0px', })


                    gb.configure_default_column(min_column_width=10,  editable=True, suppressRowTransform=True)
                    # gb.configure_default_column(min_column_width=10, headerClass={'align': "ag-center-aligned-header"}, cellStyle={'border': '0.000001px groove'})

                    # gb.configure_columns(column_names=df.columns, initialWidth=100, resizable=True, flex=5)
                    gb.configure_columns(column_names=df.columns, resizable=True,)
                    gb.configure_column("구분", width=110, suppressMenu=True,)
                    gb.configure_column("금액_전기", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.금액_전기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("금액_당기", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.금액_당기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("증감금액", type=["numericColumn",], width=76, suppressMenu=True, valueGetter="data.증감금액.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("구성비_전기", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.구성비_전기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("구성비_당기", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.구성비_당기.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("구성비_증감", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.구성비_증감.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    
                    # gb.configure_column("금액_전기", editable=True)

                    

                    gridOptions = gb.build()
                    print(jscode)
                    print(gridOptions)
                    gridOptions['getRowStyle'] = jscode

                    
                    rowspan = JsCode("""                                             
                        function getRowSpan(params) {
                            var rowspan1 = params.api.getModel().getRowCount();
                            var value = params.data.구분;
                            if (value === '외부요인') {
                                return rowspan1;
                            } else if (value === '공장요인') {
                                return rowspan1;
                            } else {
                                return 1;
                            }
                            }         
                    """)

                    leftAligned =  {
                        'cellClass': 'ag-center-aligned-cell'
                        }

                    gridOptions = {
                        'suppressRowTransform': 'true',
                        "columnDefs": [
                            
                            { 'field': '구분', 'rowSpan': rowspan, 'cellClassRules': {'cell-span': "value==='외부요인' || value==='공장요인'",}, 'width': 100},
                            { 'field': '', 'cellRenderer': cell_button_add, 'onCellClicked': JsCode(string_to_add_row)},
                            { 'field': '항목', },
                            { 'field': '증가요인', 'wrapText': True, 'autoHeight': True, 'cellStyle': {'white-space': 'normal', 'textAlign': 'left'},},
                            { 'field': '감소요인' },
                            { 'field': '계' },
                            { 'field': ' ' },

                        ],

                        'defaultColDef': {'editable': True,'resizable': True,},
                        'onCellValueChanged': 'onCellValueChanged',
                        }                    
                    
                    print(gridOptions)
                    return AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, height=height, fit_columns_on_grid_load=fit_columns_on_grid_load, key=key, allow_unsafe_jscode=True,\
                        theme='balham', update_mode=GridUpdateMode.NO_UPDATE, custom_css=custom_css, reload_data=True,)


                col_table_1, col_table_empty1, col_table_2 = st.columns([37,5,58])

                with col_table_1:
                    display_table(df_total.reset_index(), fit_columns_on_grid_load=False, sidebar=False, key=f'table_{prod_family[idx]}_1')
                with col_table_empty1:
                    st.empty()
                with col_table_2:
                    display_table2(df_anl.reset_index(), fit_columns_on_grid_load=False, sidebar=False, key=f'table_{prod_family[idx]}_2')
             


                data = pd.DataFrame(columns=['name','age','department','salary'])

                data['name'] = ['Alice','Bpb','Char','DD','Dave','Eve','Frank','Gina','Harry']
                data['age'] = [25,30,35,40,40,45,50,55,60]
                data['department'] = ['Sales', '', '','mark','','','eng','eng','eng']
                data['salary'] = [500,600,700,750,800,900,1000,1100,1200]

                # Build the grid options
                gb = GridOptionsBuilder.from_dataframe(data)
                gb.configure_column("department", header='Dept.', hide=False, allowMerging=True)
                gridOptions = gb.build()


                custom_css = {
                        ".cell-span": {"background-color": "#0E1117", 'border-bottom': 'solid 0.5px', 'border-bottom-color':'#303239'},
                        }

                rowspan = JsCode("""                                             
                    function rowSpan(params) {
                        var dept = params.data.department;
                        if (dept === 'Sales') {
                            return 3;
                        } else if (dept === 'mark') {
                            return 3;
                        } else {
                            return 1;
                        }
                        }             
                """)


                gridOptions = {
                    'suppressRowTransform': 'true',
                    "columnDefs": [
                        {'headerName': 'department', 
                        'children': [
                            { 'field': 'department', 'rowSpan': rowspan, 'cellClassRules': {'cell-span': "value==='Sales' || value==='mark'",}, "headerName": 'Dept.'},
                            { 'field': 'age' }
                        ]
                        }
                    ]
                    }

                # Display the grid
                
                st.header("Employee Details")
                AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.VALUE_CHANGED, width='100%', height=500, key=f'1111_{prod_family[idx]}', allow_unsafe_jscode=True, custom_css=custom_css)

                # import streamlit as st
                # import pandas as pd
                # from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, JsCode

                # # Define the initial data frame
                # df = pd.DataFrame({
                #     'Name': ['John', 'Mark', 'Emily'],
                #     'Age': [32, 45, 28],
                #     'Country': ['USA', 'Canada', 'USA'],
                #     'Occupation': ['Engineer', 'Doctor', 'Teacher']
                # })

                # # Define the grid options
                # gb = GridOptionsBuilder.from_dataframe(df)
                # gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
                # gridOptions = gb.build()

                # # Define the JavaScript code for the row spanning
                # js = JsCode("""
                # function(params) {
                #     var data = params.data;
                #     var span = '<span style="color: red; font-weight: bold">New Row</span>';
                #     if (data.Name.startsWith('New')) {
                #         return {
                #             cssClasses: {
                #                 cellValue: 'new-row'
                #             },
                #             innerHTML: span
                #         };
                #     } else {
                #         return {
                #             cssClasses: {
                #                 cellValue: ''
                #             },
                #             innerHTML: params.value
                #         };
                #     }
                # }
                # """)

                # # Define the Streamlit app
                # st.set_page_config(page_title="Row Spanning Demo", page_icon=":pencil:")
                # st.write("# Row Spanning Demo")

                # # Add the AgGrid component
                # new_row = {"Name": "New Row", "Age": 0, "Country": "", "Occupation": ""}
                # data_return_mode = DataReturnMode.ALWAYS_INSERT_ROW
                # with st.form(key='my_form'):
                #     grid_response = AgGrid(
                #         df,
                #         gridOptions=gridOptions,
                #         enable_enterprise_modules=True,
                #         allow_unsafe_jscode=True,
                #         enable_pagination=True,
                #         pagination_autoPageSize=True,
                #         theme='streamlit',
                #         rowHeight=40,
                #         get_row_style=js,
                #         on_grid_ready=JsCode("""
                #             function(params) {
                #                 window.gridApi = params.api;
                #                 window.gridColumnApi = params.columnApi;
                #             }
                #         """),
                #         key="myGrid",
                #         args={
                #             'suppressColumnsToolPanel': True,
                #             'rowSelection': 'single',
                #             'editType': 'fullRow',
                #             'onCellValueChanged': JsCode("""
                #                 function(params) {
                #                     if (params.oldValue != params.newValue) {
                #                         var rowNode = window.gridApi.getRowNode(params.node.id);
                #                         if (rowNode.data.Name.startsWith('New')) {
                #                             rowNode.setDataValue('Name', 'New ' + params.data.Name);
                #                             rowNode.setDataValue('Age', params.data.Age);
                #                             rowNode.setDataValue('Country', params.data.Country);
                #                             rowNode.setDataValue('Occupation', params.data.Occupation);
                #                             rowNode.setSelected(true);
                #                         }
                #                     }
                #                 }
                #             """),
                #             'onGridSizeChanged': JsCode("""
                #                 function(params) {
                #                     var gridWidth = params.clientWidth;
                #                     var columnsToShow = [];
                #                     var columnsToHide = [];
                #                     var totalColsWidth = 0;
                #                     var allColumns = window.gridColumnApi.getAllColumns();
                #                     for (var i = 0; i < allColumns.length; i++) {
                #                         var colDef = allColumns[i];
                #                         totalColsWidth += colDef.actualWidth;
                #                         if (totalColsWidth > gridWidth) {
                #                             columnsToHide.push(colDef.colId);
                #                         } else {
                #                             columnsToShow.push(colDef.colId);
                #                         }
                #                     }
                #                     window.gridColumn



            ### 그래프 TAB ###
            with tabs_Y[0]:

                col_month_slider_accum= st.columns(4)

                with col_month_slider_accum[0]:
                        
                    len_month = len(df_BW_CY.loc[['생산액']].values[0])
                    selected_month_range = st.select_slider(
                        '분석 월 을 선택하세요',
                        options=[f'{i}월' for i in range(1, len_month+1)], key=f'selected_month_{prod_family[idx]}_accum',
                        value=('1월', f'{len_month}월')
                        ),

                    st.write(f'선택 월: {selected_month_range[0][0]} ~ {selected_month_range[0][1]}')





                #### 생산액: Column A #### 

                value_1 = df_BW_PY.loc[['생산액'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/100_000_000
                print([f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_11', value_1.sum())

                fvalue_1 = value_1.sum()

                value_2 = df_BW_CY.loc[['생산액'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/100_000_000
                print([f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_22', value_2.sum())

                fvalue_2 = value_2.sum()
                differ = fvalue_2 / fvalue_1 - 1
                ndiffer = fvalue_2 - fvalue_1

                col_a1, col_a_empty1, col_a2 = st.columns([1,0.5,3])

                with col_a1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전기', x=['전기'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.1f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전기: %{y:.1f}<extra></extra>',
                        ),

                        go.Bar(name='당기', x=['당기'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.1f}' if differ >=0 else f'{fvalue_2:,.1f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당기: %{y:.1f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "생산액_누계",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>생산액(억원)</b>",
                            
                            annotations=[dict(
                                x='당기',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.1f}<br>(+{differ:.1%})' if differ >=0 else f'{ndiffer:,.1f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]                            
                            
                            )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=False, theme=None)


                with col_a_empty1:
                    st.empty()

                with col_a2:
                    print(type(df_BW_PY.loc[['생산액'], :].values[0]))

                    # fvalue_1 = format(round(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][0], 2), ',f')

                    zip_list = list(zip(df_BW_PY.loc[['생산액'], :].values[0][:], df_BW_CY.loc[['생산액'], :].values[0][:]))
                    
                    fig_text_positions_A = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_A.append('top center')
                        else:
                            fig_text_positions_A.append('bottom center')
                            
                    fig_text_positions_B = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_B.append('bottom center')
                        else:
                            fig_text_positions_B.append('top center')



                    fig2 = go.Figure(data=[
                        go.Scatter(name='전년 생산액', x=df_BW_PY.columns[:], y=df_BW_PY.loc[['생산액'], :].values[0][:]/100_000_000, mode='lines+markers+text',
                        text=['%.1f'%i for i in df_BW_PY.loc[['생산액'], :].values[0][:]/100_000_000], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = '전년: %{y:.1f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='당년 생산액', x=df_BW_CY.columns[:], y=df_BW_CY.loc[['생산액'], :].values[0][:]/100_000_000, mode='lines+markers+text',
                        text=['%.1f'%i for i in df_BW_CY.loc[['생산액'], :].values[0][:]/100_000_000], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = '당년: %{y:.1f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_BW_PY.loc[['생산액'], :].values[0][:]/100_000_000, df_BW_CY.loc[['생산액'], :].values[0][:]/100_000_000]))*0.7
                    ,max(np.concatenate([df_BW_PY.loc[['생산액'], :].values[0][:]/100_000_000, df_BW_CY.loc[['생산액'], :].values[0][:]/100_000_000]))*1.3], title_text='억원')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "생산액(억원)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = '.1f'

                    )

                    st.plotly_chart(fig2, theme=None)

                

                #### 생산량: Column B #### 

                value_1 = df_trend_PY.loc[['생산량'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/1_000
                print([f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_11', value_1.sum())

                fvalue_1 = value_1.sum()

                value_2 = df_trend_CY.loc[['생산량'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/1_000
                print([f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_22', value_2.sum())

                fvalue_2 = value_2.sum()

                differ = fvalue_2/fvalue_1 - 1
                ndiffer = fvalue_2 - fvalue_1

                col_b1, col_b_empty1, col_b2 = st.columns([1,0.5,3])

                with col_b1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전기', x=['전기'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전기: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='당기', x=['당기'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.0f}' if differ >=0 else f'{fvalue_2:,.0f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당기: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "생산량_누계",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>생산량(톤,천개)</b>",
                            
                            annotations=[dict(
                                x='당기',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.0f}<br>(+{differ:.1%})' if differ >=0 else f'{ndiffer:,.0f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]                             
                            
                            )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=False, theme=None)


                with col_b_empty1:
                    st.empty()

                with col_b2:
                    zip_list = list(zip(df_trend_PY.loc[['생산량'], :].values[0][:], df_trend_CY.loc[['생산량'], :].values[0][:]))
                    
                    fig_text_positions_A = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_A.append('top center')
                        else:
                            fig_text_positions_A.append('bottom center')
                            
                    fig_text_positions_B = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_B.append('bottom center')
                        else:
                            fig_text_positions_B.append('top center')



                    fig2 = go.Figure(data=[
                        go.Scatter(name='전년 생산량', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['생산량'], :].values[0][:]/1_000, mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_PY.loc[['생산량'], :].values[0][:]/1_000], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = '전년: %{y:,.0f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='당년 생산량', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['생산량'], :].values[0][:]/1_000, mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_CY.loc[['생산량'], :].values[0][:]/1_000], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = '당년: %{y:,.0f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_trend_PY.loc[['생산량'], :].values[0][:]/1_000, df_trend_CY.loc[['생산량'], :].values[0][:]/1_000]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['생산량'], :].values[0][:]/1_000, df_trend_CY.loc[['생산량'], :].values[0][:]/1_000]))*1.3], title_text='수량')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "생산량(톤, 천개)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = ','

                    )

                    st.plotly_chart(fig2, theme=None)




                #### 제조원가율: Column C #### 

                value_1 = df_trend_PY.loc[['제조원가율'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                print([f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_11', value_1.sum())

                BW_cost_1 = df_BW_PY.loc[['당기 제품제조원가'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                BW_amount_1= df_BW_PY.loc[['생산액'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                
                fvalue_1 = BW_cost_1.sum() / BW_amount_1.sum()

                value_2 = df_trend_CY.loc[['제조원가율'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                print([f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_22', value_2.sum())

                BW_cost_2 = df_BW_CY.loc[['당기 제품제조원가'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                BW_amount_2= df_BW_CY.loc[['생산액'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                
                fvalue_2 = BW_cost_2.sum() / BW_amount_2.sum()

                differ = fvalue_2 - fvalue_1

                col_c1, col_c_empty1, col_c2 = st.columns([1,0.5,3])

                with col_c1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전기', x=['전기'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.1%}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전기: %{y:.1%}<extra></extra>',
                        ),

                        go.Bar(name='당기', x=['당기'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.1%}' if differ >=0 else f'{fvalue_2:,.1%}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당기: %{y:.1%}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "제조원가율_누계",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>제조원가율(%)</b>",
                            yaxis_tickformat = '.0%',
                            
                            annotations=[dict(
                                x='당기',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'+{differ:.1%}p' if differ >=0 else f'{differ:.1%}p',
                                font=dict(color='rgb(0,176,240)' if differ < 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                        )
                    


                    st.plotly_chart(fig, use_container_width=False, theme=None)


                with col_c_empty1:
                    st.empty()

                with col_c2:
                    zip_list = list(zip(df_trend_PY.loc[['제조원가율'], :].values[0][:], df_trend_CY.loc[['제조원가율'], :].values[0][:]))
                    
                    fig_text_positions_A = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_A.append('top center')
                        else:
                            fig_text_positions_A.append('bottom center')
                            
                    fig_text_positions_B = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_B.append('bottom center')
                        else:
                            fig_text_positions_B.append('top center')



                    fig2 = go.Figure(data=[
                        go.Scatter(name='전년 원가율', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['제조원가율'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.1%}' for i in df_trend_PY.loc[['제조원가율'], :].values[0][:]], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = '전년: %{y:.1%}<extra></extra>',
                        ),
                        
                        go.Scatter(name='당년 원가율', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['제조원가율'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.1%}' for i in df_trend_CY.loc[['제조원가율'], :].values[0][:]], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = '당년: %{y:.1%}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_trend_PY.loc[['제조원가율'], :].values[0][:], df_trend_CY.loc[['제조원가율'], :].values[0][:]]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['제조원가율'], :].values[0][:], df_trend_CY.loc[['제조원가율'], :].values[0][:]]))*1.3], title_text='원가율')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "제조원가율(%)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = '.0%'

                    )

                    st.plotly_chart(fig2, theme=None)



                #### 인시당 생산성: Column D #### 

                # value_1 = df_trend_PY.loc[['인시당 생산성'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0] \
                #     / df_trend_PY.loc[['인시당 생산성'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                
                trend_volume_1 = df_trend_PY.loc[['생산량'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_inMhr_1 = df_trend_PY.loc[['자사_Mhr'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_outMhr_1 = df_trend_PY.loc[['외주_Mhr'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
               
                fvalue_1 = trend_volume_1.sum() / (trend_inMhr_1+trend_outMhr_1).sum()

                # value_2 = df_trend_CY.loc[['인시당 생산성'], [f'{i}월' for i in range(int(selected_month_range[0][0][:  -1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                

                trend_volume_2 = df_trend_CY.loc[['생산량'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_inMhr_2 = df_trend_CY.loc[['자사_Mhr'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_outMhr_2 = df_trend_CY.loc[['외주_Mhr'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]

                fvalue_2 = trend_volume_2.sum() / (trend_inMhr_2+trend_outMhr_2).sum()

                differ = fvalue_2/fvalue_1 - 1
                ndiffer = fvalue_2 - fvalue_1

                col_d1, col_d_empty1, col_d2 = st.columns([1,0.5,3])

                with col_d1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전기', x=['전기'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전기: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='당기', x=['당기'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.0f}' if differ >=0 else f'{fvalue_2:,.0f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당기: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': f"생산성_누계",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>생산성(톤,천개 / Mhr)</b>",
                            
                            annotations=[dict(
                                x='당기',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.1f}<br>(+{differ:.1%})' if differ >=0 else f'{ndiffer:,.1f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]                        
                            
                            )


                    st.plotly_chart(fig, use_container_width=False, theme=None)


                with col_d_empty1:
                    st.empty()

                with col_d2:
                    zip_list = list(zip(df_trend_PY.loc[['인시당 생산성'], :].values[0][:], df_trend_CY.loc[['인시당 생산성'], :].values[0][:]))
                    
                    fig_text_positions_A = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_A.append('top center')
                        else:
                            fig_text_positions_A.append('bottom center')
                            
                    fig_text_positions_B = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_B.append('bottom center')
                        else:
                            fig_text_positions_B.append('top center')



                    fig2 = go.Figure(data=[
                        go.Scatter(name='전년 생산성', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['인시당 생산성'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_PY.loc[['인시당 생산성'], :].values[0][:]], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = '전년: %{y:,.0f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='당년 생산성', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['인시당 생산성'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_CY.loc[['인시당 생산성'], :].values[0][:]], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = '당년: %{y:,.0f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_trend_PY.loc[['인시당 생산성'], :].values[0][:], df_trend_CY.loc[['인시당 생산성'], :].values[0][:]]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['인시당 생산성'], :].values[0][:], df_trend_CY.loc[['인시당 생산성'], :].values[0][:]]))*1.3], title_text='생산성')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "인시당 생산성(톤, 천개/Mhr)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = ','

                    )

                    st.plotly_chart(fig2, theme=None)


                #### 고객불만: Column E #### 

                value_1 = df_trend_PY.loc[['고객불만'], [f'{i}월' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                fvalue_1 = value_1.sum()

                value_2 = df_trend_CY.loc[['고객불만'], [f'{i}월' for i in range(int(selected_month_range[0][0][:  -1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                fvalue_2 = value_2.sum() 

                differ = fvalue_2 - fvalue_1

                col_e1, col_e_empty1, col_e2 = st.columns([1,0.5,3])

                with col_e1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='전기', x=['전기'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = '전기: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='당기', x=['당기'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.0f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = '당기: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': f"고객불만_누계",
                            # 'y':0.2,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            
                            }
                            , title_font_size=18,

                            title_font_family="malgun gothic",

                            showlegend=False,
                            margin=dict(l=80, r=80, t=50, b=20),
                            width=400, height=250,
                            yaxis_title="<b>고객불만(건수)</b>",
                            
                            annotations=[dict(
                                x='당기',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'+{differ:.0f}' if differ > 0 else f'{differ:.0f}',
                                font=dict(color='rgb(0,176,240)' if differ < 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]                            
                            
                            )
                    fig.update_yaxes(visible=False)


                    st.plotly_chart(fig, use_container_width=False, theme=None)


                with col_e_empty1:
                    st.empty()

                with col_e2:
                    zip_list = list(zip(df_trend_PY.loc[['고객불만'], :].values[0][:], df_trend_CY.loc[['고객불만'], :].values[0][:]))
                    
                    fig_text_positions_A = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_A.append('top center')
                        else:
                            fig_text_positions_A.append('bottom center')
                            
                    fig_text_positions_B = []
                    for i in zip_list:
                        
                        if i[0] > i[1]:
                            fig_text_positions_B.append('bottom center')
                        else:
                            fig_text_positions_B.append('top center')



                    fig2 = go.Figure(data=[
                        go.Scatter(name='전년 고객불만', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['고객불만'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_PY.loc[['고객불만'], :].values[0][:]], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = '전년: %{y:,.0f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='당년 고객불만', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['고객불만'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_CY.loc[['고객불만'], :].values[0][:]], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = '당년: %{y:,.0f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[-0.2 if min(np.concatenate([df_trend_PY.loc[['고객불만'], :].values[0][:], df_trend_CY.loc[['고객불만'], :].values[0][:]]))==0 else min(np.concatenate([df_trend_PY.loc[['고객불만'], :].values[0][:], df_trend_CY.loc[['고객불만'], :].values[0][:]]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['고객불만'], :].values[0][:], df_trend_CY.loc[['고객불만'], :].values[0][:]]))*1.3], title_text='고객불만', visible=False)
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "고객불만(건수)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = ','

                    )

                    st.plotly_chart(fig2, theme=None)
            
            with tabs_Y[2]:

                st.title("Add and Delete Rows with Checkbox")


            # with st.expander("Data 보기/접기",expanded=True):
            lst_data_tab = ['🟠','Data_전년','Data_당년']

            tabs_data = st.tabs(lst_data_tab)
            with tabs_data[1]:
                df_BW_PY.dropna(how='all', inplace=True)
                st.dataframe(df_BW_PY.style.format("{:,.0f}"))
            with tabs_data[2]:
                df_BW_CY.dropna(how='all', inplace=True)
                st.dataframe(df_BW_CY.style.format("{:,.0f}"))


  