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



st.set_page_config(page_title="Plotting Demo", page_icon="π", layout="wide")

st.markdown("# μ μ‘°μκ° λΆμ test version")
st.sidebar.header("νμΌ μλ‘λ")
st.write(
    """....μ μ‘°μκ° λΆμ WEB page νμ€νΈ λ²μ  μλλ€...."""
)



with st.sidebar:
    amount_unit = st.radio(" ", options=('λ¬Όλ', 'μλ'), label_visibility='hidden', key='amount_unit', horizontal=True)
    uploaded_file = st.file_uploader("μμ νμΌμ μλ‘λν΄μ£ΌμΈμ", type="xlsx")
    

if uploaded_file is not None:
    
    df_info = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', engine='openpyxl', sheet_name='info', header=None, index_col=0)
    team_name = [value for value in df_info.loc['ν',:].values if value is not np.nan][0]
    prod_family = [value for value in df_info.loc['κ΅¬λΆ',:].values if value is not np.nan]

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
        df_trend_PY.drop(['λ¨μ'], inplace=True, axis=1)

        df_trend_CY = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', sheet_name=f'Trend_{prod_family[idx]}', engine='openpyxl', header=11, nrows=9, index_col=1)
        df_trend_CY.dropna(how='all', inplace=True)
        df_trend_CY.fillna(0, inplace=True)
        df_trend_CY.drop(['λ¨μ'], inplace=True, axis=1)
        

        print(df_trend_PY)

        if amount_unit == 'λ¬Όλ':
            df_trend_PY.loc['μμ°λ',:] = df_trend_PY.loc['μμ°λ¬Όλ', :]
            df_trend_CY.loc['μμ°λ',:] = df_trend_CY.loc['μμ°λ¬Όλ', :]

        if amount_unit == 'μλ':
            df_trend_PY.loc['μμ°λ',:] = df_trend_PY.loc['μμ°μλ', :]
            df_trend_CY.loc['μμ°λ',:] = df_trend_CY.loc['μμ°μλ', :]

        df_trend_PY.loc['μΈμλΉ μμ°μ±',:] = df_trend_PY.loc['μμ°λ', :] / (df_trend_PY.loc['μμ¬_Mhr', :] + df_trend_PY.loc['μΈμ£Ό_Mhr', :])
        df_trend_CY.loc['μΈμλΉ μμ°μ±',:] = df_trend_CY.loc['μμ°λ', :] / (df_trend_CY.loc['μμ¬_Mhr', :] + df_trend_CY.loc['μΈμ£Ό_Mhr', :])

        print(df_trend_CY)

        
        
        with tabs[idx]:
            lst_Y = ['κ·Έλν','λΉμ','λκ³']
            tabs_Y = st.tabs(lst_Y)


            ### λΉμ λΆμ TAB ###
            with tabs_Y[1]:
                
                col_month_slider= st.columns(4)

                with col_month_slider[0]:

                    len_month = len(df_BW_CY.loc[['μμ°μ‘']].values[0])
                    selected_month = st.select_slider(
                        'λΆμ μ μ μ ννμΈμ',
                        options=[f'{i}μ' for i in range(1, len_month+1)], key=f'selected_month_{prod_family[idx]}',
                        value=f'{len_month}μ'
                        ),

                    st.write('μ ν μ: ', selected_month[0][0:-1])
                    num_selected_month = int(selected_month[0][0:-1])
                    print(num_selected_month)




                #### μμ°μ‘: Column A ####
                col_a1, col_a2, col_a3, col_a4, col_a_empty3 = st.columns([4, 4, 4, 4, 1], gap="small")

                with col_a1:

                    if num_selected_month == 1:
    
                        value_1 = format(round(df_BW_PY.loc[['μμ°μ‘'], ['12μ']].values[0][0]/100_000_000, 1), ',f')
                    else:
                        value_1 = format(round(df_BW_CY.loc[['μμ°μ‘'], [f'{num_selected_month-1}μ']].values[0][0]/100_000_000, 1), ',f')
                    value_2 = format(round(df_BW_CY.loc[['μμ°μ‘'], [f'{num_selected_month}μ']].values[0][0]/100_000_000, 1), ',f')

                    fvalue_1 = float(value_1)
                    fvalue_2 = float(value_2)

                    differ = fvalue_2/fvalue_1 - 1
                    ndiffer = fvalue_2 - fvalue_1                    
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ μ', x=['μ μ'], y=[value_1],
                        text=[f'{fvalue_1:,.1f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ μ: %{y:.1f}<extra></extra>',
                        ),

                        go.Bar(name='λΉμ', x=['λΉμ'], y=[value_2],
                        text=[f'{fvalue_2:,.1f}' if differ >=0 else f'{fvalue_2}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉμ: %{y:.1f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μμ°μ‘_λΉμ",
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
                            yaxis_title="<b>μμ°μ‘(μ΅μ)</b>",
                            
                            annotations=[dict(
                                x='λΉμ',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.1f}<br>(+{differ:.1%})</b>' if differ >=0 else f'<b>{ndiffer:,.1f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                            
                            
                            )

                    # fig.update_annotations(
                    #     x="λΉμ",
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
    
                        value_1 = round(df_trend_PY.loc[['μμ°λ'], ['12μ']].values[0][0]/1_000, 0)
                    else:
                        value_1 = round(df_trend_CY.loc[['μμ°λ'], [f'{num_selected_month-1}μ']].values[0][0]/1_000, 0)
                        print(value_1)
                        print(type(value_1))
                    value_2 = round(df_trend_CY.loc[['μμ°λ'], [f'{num_selected_month}μ']].values[0][0]/1_000, 0)

                    fvalue_1 = float(value_1)
                    fvalue_2 = float(value_2)

                    differ = fvalue_2/fvalue_1 - 1
                    ndiffer = fvalue_2 - fvalue_1


                    fig = go.Figure(data=[
                        go.Bar(name='μ μ', x=['μ μ'], y=[value_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ μ: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='λΉμ', x=['λΉμ'], y=[value_2],
                        text=[f'{fvalue_2:,.0f}' if differ >=0 else f'{fvalue_2}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉμ: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μμ°λ_λΉμ",
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
                            yaxis_title="<b>μμ°λ(ν€)</b>",
                            
                            annotations=[dict(
                                x='λΉμ',
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
                    #     x="λΉμ",
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
    
                        value_1 = round(df_trend_PY.loc[['μ μ‘°μκ°μ¨'], ['12μ']].values[0][0], 3)
                    else:
                        value_1 = round(df_trend_CY.loc[['μ μ‘°μκ°μ¨'], [f'{num_selected_month-1}μ']].values[0][0], 3)
                        print(value_1)
                        print(type(value_1))
                    value_2 = round(df_trend_CY.loc[['μ μ‘°μκ°μ¨'], [f'{num_selected_month}μ']].values[0][0], 3)

                    fvalue_1 = float(value_1)
                    fvalue_2 = float(value_2)

                    differ = fvalue_2 - fvalue_1



                    fig = go.Figure(data=[
                        go.Bar(name='μ μ', x=['μ μ'], y=[value_1],
                        text=[f'{fvalue_1:,.1%}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ μ: %{y:.1%}<extra></extra>',
                        ),

                        go.Bar(name='λΉμ', x=['λΉμ'], y=[value_2],
                        text=[f'{fvalue_2:,.1%}' if differ >=0 else f'{fvalue_2:,.1%}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉμ: %{y:.1%}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μ μ‘°μκ°μ¨_λΉμ",
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
                            yaxis_title="<b>μ μ‘°μκ°μ¨(%)</b>",
                            
                            annotations=[dict(
                                x='λΉμ',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'+{differ:.1%}p' if differ >=0 else f'{differ:.1%}p',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                            
                            
                            )

                    # fig.update_annotations(
                    #     x="λΉμ",
                    #     y=75,
                    #     text='TESTTTTTTTTTTT',
                    #     # valign='top',
                    #     )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=True, theme=None)

                with col_a4:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ μ', x=['μ μ'], y=[value_1],
                        text=[f'{fvalue_1:,.1f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ μ: %{y:.1f}<extra></extra>',
                        ),

                        go.Bar(name='λΉμ', x=['λΉμ'], y=[value_2],
                        text=[f'{fvalue_2:,.1f}' if differ >=0 else f'{fvalue_2}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉμ: %{y:.1f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μμ°μ‘_λΉμ",
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
                            yaxis_title="<b>μμ°μ‘(μ΅μ)</b>",
                            
                            annotations=[dict(
                                x='λΉμ',
                                y=max([fvalue_1, fvalue_2])*1.1,
                                text=f'{ndiffer:,.1f}<br>(+{differ:.1%})</b>' if differ >=0 else f'<b>{ndiffer:,.1f}<br>({differ:.1%})',
                                font=dict(color='rgb(0,176,240)' if ndiffer >= 0 else 'red', size=18),
                                showarrow=False,
                                xshift=-60,
                                yshift=15,

                            )]
                            
                            
                            )

                    # fig.update_annotations(
                    #     x="λΉμ",
                    #     y=75,
                    #     text='TESTTTTTTTTTTT',
                    #     # valign='top',
                    #     )
                    fig.update_yaxes()


                    st.plotly_chart(fig, use_container_width=True, theme=None)
                
                df_total = pd.DataFrame(columns=['κ΅¬λΆ','κΈμ‘_μ κΈ°','κ΅¬μ±λΉ_μ κΈ°','κΈμ‘_λΉκΈ°','κ΅¬μ±λΉ_λΉκΈ°','μ¦κ°κΈμ‘','κ΅¬μ±λΉ_μ¦κ°'])
                

                index_total = ['μ€μ§ μμ°μ‘','μμ¬λ£λΉ','μ©κΈ°/ν¬μ₯λΉ','μ λ ₯/μ°λ£λΉ','μΈμ£Όκ°κ³΅λΉ','κΈ°ν','λ³λλΉ κ³',\
                    'μκΈ/κΈλ£','μ μ‘°κ΄λ¦¬ μΈκ±΄λΉ','κ°κ°μκ°λΉ','μλͺ¨/μμ λΉ','κ²½μκ°λ°λΉ','λ°μ νμ°¨','κΈ° ν', 'κ³ μ λΉ κ³','μ μ‘°μκ°']
                df_total['κ΅¬λΆ'] = index_total
                df_total.set_index('κ΅¬λΆ', inplace=True)

                

                if num_selected_month == 1:
                    df_total.loc[:,'κΈμ‘_μ κΈ°'] = np.array(
                        [df_BW_PY.loc['μμ°μ‘', [f'12μ']].values[0],
                        df_BW_PY.loc['μμ¬λ£λΉ', [f'12μ']].values[0] + df_BW_PY.loc['μ¬λ£λΉ:μν', [f'12μ']].values[0],
                        df_BW_PY.loc['μ©κΈ°λΆνλΉ', [f'12μ']].values[0] + df_BW_PY.loc['λ§€μλΆνλΉ', [f'12μ']].values[0] + df_BW_PY.loc['ν¬μ₯λΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['μ λ ₯λΉ', [f'12μ']].values[0] + df_BW_PY.loc['μ°λ£λΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['μΈμ£Όκ°κ³΅λΉ', [f'12μ']].values[0] + df_BW_PY.loc['μ¬μΈ μΈμ£Όκ°κ³΅λΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['μλͺ¨νλΉ', [f'12μ']].values[0] + df_BW_PY.loc['μ¬μ©λ£', [f'12μ']].values[0] + df_BW_PY.loc['μΈκΈκ³Όκ³΅κ³Ό', [f'12μ']].values[0],
                        0,
                        df_BW_PY.loc['κΈλ£', [f'12μ']].values[0] + df_BW_PY.loc['μκΈ', [f'12μ']].values[0]+ df_BW_PY.loc['μμ¬κΈ', [f'12μ']].values[0]+df_BW_PY.loc['ν΄μ§κΈμ¬', [f'12μ']].values[0]+df_BW_PY.loc['λ³΅λ¦¬νμλΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['μ²­μ£Ό.μ μ‘°κ΄λ¦¬-μΈκ±΄λΉ', [f'12μ']].values[0]+df_BW_PY.loc['μ²­μ£Ό.κ°μ  μΈκ±΄λΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['κ°κ°μκ°λΉ', [f'12μ']].values[0]+df_BW_PY.loc['λ¬΄νμκ°λΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['μμ λΉ', [f'12μ']].values[0] + df_BW_PY.loc['μλͺ¨νλΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['κ²½μκ°λ°λΉ', [f'12μ']].values[0],
                        df_BW_PY.loc['κΈ°μ΄ λ°μ ν μ¬κ³ ', [f'12μ']].values[0] + df_BW_PY.loc['νκ³μ  λμ²΄', [f'12μ']].values[0] - df_BW_PY.loc['κΈ°λ§ λ°μ ν μ¬κ³ ', [f'12μ']].values[0],
                        df_BW_PY.loc[['μ¬λΉκ΅ν΅λΉ','ν΅μ λΉ','μλκ΄μ΄λΉ','μμ°¨λ£','μ§κΈμ©μ­λ£','μ°¨λκ΄λ¦¬λΉ','λ³΄νλ£','κ΅μ λΉ','κ΄κ³ λΉ','μ΄λ°λΉ','λμμΈμλΉ','κ΅μ‘νλ ¨λΉ','νμλΉ','μ°κ΅¬λΉ','μ‘λΉ','μ²­μ£Ό.μ μ‘°κ΄λ¦¬-μκ°λΉ','μ²­μ£Ό.μ μ‘°κ΄λ¦¬-κΈ°ν'], [f'12μ']].values.sum(),
                        0,
                        0])/1_000_000
                    
                else:
                    
                    df_total.loc[:,'κΈμ‘_μ κΈ°'] = np.array(
                        [df_BW_CY.loc['μμ°μ‘', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μμ¬λ£λΉ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['μ¬λ£λΉ:μν', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μ©κΈ°λΆνλΉ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['λ§€μλΆνλΉ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['ν¬μ₯λΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μ λ ₯λΉ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['μ°λ£λΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μΈμ£Όκ°κ³΅λΉ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['μ¬μΈ μΈμ£Όκ°κ³΅λΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μ¬μ©λ£', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['μΈκΈκ³Όκ³΅κ³Ό', [f'{num_selected_month-1}μ']].values[0],
                        0,
                        df_BW_CY.loc['κΈλ£', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['μκΈ', [f'{num_selected_month-1}μ']].values[0]+ df_BW_CY.loc['μμ¬κΈ', [f'{num_selected_month-1}μ']].values[0]+df_BW_CY.loc['ν΄μ§κΈμ¬', [f'{num_selected_month-1}μ']].values[0]+df_BW_CY.loc['λ³΅λ¦¬νμλΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μ²­μ£Ό.μ μ‘°κ΄λ¦¬-μΈκ±΄λΉ', [f'{num_selected_month-1}μ']].values[0]+df_BW_CY.loc['μ²­μ£Ό.κ°μ  μΈκ±΄λΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['κ°κ°μκ°λΉ', [f'{num_selected_month-1}μ']].values[0]+df_BW_CY.loc['λ¬΄νμκ°λΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['μμ λΉ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['μλͺ¨νλΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['κ²½μκ°λ°λΉ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc['κΈ°μ΄ λ°μ ν μ¬κ³ ', [f'{num_selected_month-1}μ']].values[0] + df_BW_CY.loc['νκ³μ  λμ²΄', [f'{num_selected_month-1}μ']].values[0] - df_BW_CY.loc['κΈ°λ§ λ°μ ν μ¬κ³ ', [f'{num_selected_month-1}μ']].values[0],
                        df_BW_CY.loc[['μ¬λΉκ΅ν΅λΉ','ν΅μ λΉ','μλκ΄μ΄λΉ','μμ°¨λ£','μ§κΈμμλ£','μ§κΈμ©μ­λ£','μ°¨λκ΄λ¦¬λΉ','λ³΄νλ£','κ΅μ λΉ','κ΄κ³ λΉ','μ΄λ°λΉ','λμμΈμλΉ','κ΅μ‘νλ ¨λΉ','νμλΉ','μ°κ΅¬λΉ','μ‘λΉ','μ²­μ£Ό.μ μ‘°κ΄λ¦¬-μκ°λΉ','μ²­μ£Ό.μ μ‘°κ΄λ¦¬-κΈ°ν','μ²­μ£Ό.κ°μ  κΈ°ν'], [f'{num_selected_month-1}μ']].values.sum(),
                        0,
                        0])/1_000_000

                df_total.loc[:,'κΈμ‘_λΉκΈ°'] = np.array(
                    [df_BW_CY.loc['μμ°μ‘', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μμ¬λ£λΉ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['μ¬λ£λΉ:μν', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μ©κΈ°λΆνλΉ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['λ§€μλΆνλΉ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['ν¬μ₯λΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μ λ ₯λΉ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['μ°λ£λΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μΈμ£Όκ°κ³΅λΉ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['μ¬μΈ μΈμ£Όκ°κ³΅λΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μ¬μ©λ£', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['μΈκΈκ³Όκ³΅κ³Ό', [f'{num_selected_month}μ']].values[0],
                    0,
                    df_BW_CY.loc['κΈλ£', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['μκΈ', [f'{num_selected_month}μ']].values[0]+ df_BW_CY.loc['μμ¬κΈ', [f'{num_selected_month}μ']].values[0]+df_BW_CY.loc['ν΄μ§κΈμ¬', [f'{num_selected_month}μ']].values[0]+df_BW_CY.loc['λ³΅λ¦¬νμλΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μ²­μ£Ό.μ μ‘°κ΄λ¦¬-μΈκ±΄λΉ', [f'{num_selected_month}μ']].values[0]+df_BW_CY.loc['μ²­μ£Ό.κ°μ  μΈκ±΄λΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['κ°κ°μκ°λΉ', [f'{num_selected_month}μ']].values[0]+df_BW_CY.loc['λ¬΄νμκ°λΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['μμ λΉ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['μλͺ¨νλΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['κ²½μκ°λ°λΉ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc['κΈ°μ΄ λ°μ ν μ¬κ³ ', [f'{num_selected_month}μ']].values[0] + df_BW_CY.loc['νκ³μ  λμ²΄', [f'{num_selected_month}μ']].values[0] - df_BW_CY.loc['κΈ°λ§ λ°μ ν μ¬κ³ ', [f'{num_selected_month}μ']].values[0],
                    df_BW_CY.loc[['μ¬λΉκ΅ν΅λΉ','ν΅μ λΉ','μλκ΄μ΄λΉ','μμ°¨λ£','μ§κΈμμλ£','μ§κΈμ©μ­λ£','μ°¨λκ΄λ¦¬λΉ','λ³΄νλ£','κ΅μ λΉ','κ΄κ³ λΉ','μ΄λ°λΉ','λμμΈμλΉ','κ΅μ‘νλ ¨λΉ','νμλΉ','μ°κ΅¬λΉ','μ‘λΉ','μ²­μ£Ό.μ μ‘°κ΄λ¦¬-μκ°λΉ','μ²­μ£Ό.μ μ‘°κ΄λ¦¬-κΈ°ν','μ²­μ£Ό.κ°μ  κΈ°ν'], [f'{num_selected_month}μ']].values.sum(),
                    0,
                    0])/1_000_000

                if num_selected_month == 1:
                    df_total.loc[:,'κ΅¬μ±λΉ_μ κΈ°'] = df_total.loc[:,'κΈμ‘_μ κΈ°'] / df_BW_PY.loc['μμ°μ‘', [f'12μ']].values[0] *100 * 1_000_000
                else:
                    df_total.loc[:,'κ΅¬μ±λΉ_μ κΈ°'] = df_total.loc[:,'κΈμ‘_μ κΈ°'] / df_BW_CY.loc['μμ°μ‘', [f'{num_selected_month-1}μ']].values[0] *100 * 1_000_000
                df_total.loc[:,'κ΅¬μ±λΉ_λΉκΈ°'] = df_total.loc[:,'κΈμ‘_λΉκΈ°'] / df_BW_CY.loc['μμ°μ‘', [f'{num_selected_month}μ']].values[0] *100 * 1_000_000
                df_total.loc[:,'μ¦κ°κΈμ‘'] = df_total.loc[:,'κΈμ‘_λΉκΈ°'] - df_total.loc[:,'κΈμ‘_μ κΈ°']
                df_total.loc[:,'κ΅¬μ±λΉ_μ¦κ°'] = df_total.loc[:,'κ΅¬μ±λΉ_λΉκΈ°'] - df_total.loc[:,'κ΅¬μ±λΉ_μ κΈ°']

                df_total.loc['λ³λλΉ κ³',:] = df_total.loc[['μμ¬λ£λΉ','μ©κΈ°/ν¬μ₯λΉ','μ λ ₯/μ°λ£λΉ','μΈμ£Όκ°κ³΅λΉ','κΈ°ν'],:].sum()
                df_total.loc['κ³ μ λΉ κ³',:] = df_total.loc[['μκΈ/κΈλ£','μ μ‘°κ΄λ¦¬ μΈκ±΄λΉ','κ°κ°μκ°λΉ','μλͺ¨/μμ λΉ','κ²½μκ°λ°λΉ','λ°μ νμ°¨','κΈ° ν'],:].sum()
                df_total.loc['μ μ‘°μκ°',:] = df_total.loc[['λ³λλΉ κ³','κ³ μ λΉ κ³'],:].sum()

                ### μ μ‘°μκ° λΆμ ν ###
                df_anl = pd.DataFrame(columns=['κ΅¬λΆ','ν­λͺ©','μ¦κ°μμΈ','κ°μμμΈ','κ³'])
                df_anl.loc[:,'κ΅¬λΆ'] = ['μ κΈ°', 'μΈλΆμμΈ', '', '', '', '', '', '',\
                    'κ³΅μ₯μμΈ', '', '', '', '', '', '', '', '', 'λΉκΈ°']
                df_anl.loc[:,'ν­λͺ©'] = ['μ κΈ°','μλΆμμ¬','P-Mixμ°¨','κ³ μ λΉμν₯','νκ°μν₯','μΈμ£Όκ°κ³΅λΉ','κΈ°ν','μΈλΆμμΈ μκ³',\
                    'μκ°μ κ°','μΈμ£Όκ°κ³΅λΉ','μΈκ±΄λΉ','μ λ ₯/μ°λ£λΉ','μλͺ¨μμ λΉ','μλͺ¨μμ λΉ','κΈ° ν','κΈ° ν','κ³΅μ₯μμΈ μκ³','λΉκΈ°']

                df_anl.set_index('κ΅¬λΆ', inplace=True)


                ### draw pandas table ###
                # print(df_total)

                # df_total.reset_index().loc[:4].style.set_properties(**{'background-color': 'white',
                #             'color': 'lawngreen',
                #             'border-color': 'white'})
                # st.write("μ¦κ° λΆμ")
                # st.dataframe(df_total.reset_index().style.format({'κ΅¬μ±λΉ_μ κΈ°':'{:,.1f}', 'κ΅¬μ±λΉ_λΉκΈ°':'{:,.1f}', 'κ΅¬μ±λΉ_μ¦κ°':'{:,.1f}', 'κΈμ‘_μ κΈ°':'{:,.0f}', 'κΈμ‘_λΉκΈ°':'{:,.0f}', 'μ¦κ°κΈμ‘':'{:,.0f}'})\
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
                            if (params.data.κ΅¬λΆ ===("μ€μ§ μμ°μ‘")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'rgb(190,200,255)',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'

                                }
                            }
                            if (params.data.κ΅¬λΆ ===("λ³λλΉ κ³") || params.data.κ΅¬λΆ === ("κ³ μ λΉ κ³")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'orange',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'
                                }
                            }
                            if (params.data.κ΅¬λΆ ===("μ μ‘°μκ°")) {
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
                    gb.configure_column("κ΅¬λΆ", width=110, suppressMenu=True, )
                    gb.configure_column("κΈμ‘_μ κΈ°", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.κΈμ‘_μ κΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("κΈμ‘_λΉκΈ°", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.κΈμ‘_λΉκΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("μ¦κ°κΈμ‘", type=["numericColumn",], width=76, suppressMenu=True, valueGetter="data.μ¦κ°κΈμ‘.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("κ΅¬μ±λΉ_μ κΈ°", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.κ΅¬μ±λΉ_μ κΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("κ΅¬μ±λΉ_λΉκΈ°", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.κ΅¬μ±λΉ_λΉκΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("κ΅¬μ±λΉ_μ¦κ°", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.κ΅¬μ±λΉ_μ¦κ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    
                    # gb.configure_column("κΈμ‘_μ κΈ°", editable=True)

                    

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
                            if (params.data.κ΅¬λΆ ===("μ€μ§ μμ°μ‘")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'rgb(190,200,255)',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'

                                }
                            }
                            if (params.data.κ΅¬λΆ ===("λ³λλΉ κ³") || params.data.κ΅¬λΆ === ("κ³ μ λΉ κ³")) {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'orange',
                                    'fontWeight': 'bold',
                                    'font-size': '14px'
                                }
                            }
                            if (params.data.κ΅¬λΆ ===("μ μ‘°μκ°")) {
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
                                        >β</button>
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
                                        >ποΈ</button>
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
                    gb.configure_column("κ΅¬λΆ", width=110, suppressMenu=True,)
                    gb.configure_column("κΈμ‘_μ κΈ°", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.κΈμ‘_μ κΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("κΈμ‘_λΉκΈ°", type=["numericColumn",], width=81, suppressMenu=True, valueGetter="data.κΈμ‘_λΉκΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("μ¦κ°κΈμ‘", type=["numericColumn",], width=76, suppressMenu=True, valueGetter="data.μ¦κ°κΈμ‘.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:0})")
                    gb.configure_column("κ΅¬μ±λΉ_μ κΈ°", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.κ΅¬μ±λΉ_μ κΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("κ΅¬μ±λΉ_λΉκΈ°", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.κ΅¬μ±λΉ_λΉκΈ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    gb.configure_column("κ΅¬μ±λΉ_μ¦κ°", type=["numericColumn",], width=96, suppressMenu=True, valueGetter="data.κ΅¬μ±λΉ_μ¦κ°.toLocaleString('en-US', {style: 'decimal', maximumFractionDigits:1})")
                    
                    # gb.configure_column("κΈμ‘_μ κΈ°", editable=True)

                    

                    gridOptions = gb.build()
                    print(jscode)
                    print(gridOptions)
                    gridOptions['getRowStyle'] = jscode

                    
                    rowspan = JsCode("""                                             
                        function getRowSpan(params) {
                            var rowspan1 = params.api.getModel().getRowCount();
                            var value = params.data.κ΅¬λΆ;
                            if (value === 'μΈλΆμμΈ') {
                                return rowspan1;
                            } else if (value === 'κ³΅μ₯μμΈ') {
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
                            
                            { 'field': 'κ΅¬λΆ', 'rowSpan': rowspan, 'cellClassRules': {'cell-span': "value==='μΈλΆμμΈ' || value==='κ³΅μ₯μμΈ'",}, 'width': 100},
                            { 'field': '', 'cellRenderer': cell_button_add, 'onCellClicked': JsCode(string_to_add_row)},
                            { 'field': 'ν­λͺ©', },
                            { 'field': 'μ¦κ°μμΈ', 'wrapText': True, 'autoHeight': True, 'cellStyle': {'white-space': 'normal', 'textAlign': 'left'},},
                            { 'field': 'κ°μμμΈ' },
                            { 'field': 'κ³' },
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



            ### κ·Έλν TAB ###
            with tabs_Y[0]:

                col_month_slider_accum= st.columns(4)

                with col_month_slider_accum[0]:
                        
                    len_month = len(df_BW_CY.loc[['μμ°μ‘']].values[0])
                    selected_month_range = st.select_slider(
                        'λΆμ μ μ μ ννμΈμ',
                        options=[f'{i}μ' for i in range(1, len_month+1)], key=f'selected_month_{prod_family[idx]}_accum',
                        value=('1μ', f'{len_month}μ')
                        ),

                    st.write(f'μ ν μ: {selected_month_range[0][0]} ~ {selected_month_range[0][1]}')





                #### μμ°μ‘: Column A #### 

                value_1 = df_BW_PY.loc[['μμ°μ‘'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/100_000_000
                print([f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_11', value_1.sum())

                fvalue_1 = value_1.sum()

                value_2 = df_BW_CY.loc[['μμ°μ‘'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/100_000_000
                print([f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_22', value_2.sum())

                fvalue_2 = value_2.sum()
                differ = fvalue_2 / fvalue_1 - 1
                ndiffer = fvalue_2 - fvalue_1

                col_a1, col_a_empty1, col_a2 = st.columns([1,0.5,3])

                with col_a1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ κΈ°', x=['μ κΈ°'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.1f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ κΈ°: %{y:.1f}<extra></extra>',
                        ),

                        go.Bar(name='λΉκΈ°', x=['λΉκΈ°'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.1f}' if differ >=0 else f'{fvalue_2:,.1f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉκΈ°: %{y:.1f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μμ°μ‘_λκ³",
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
                            yaxis_title="<b>μμ°μ‘(μ΅μ)</b>",
                            
                            annotations=[dict(
                                x='λΉκΈ°',
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
                    print(type(df_BW_PY.loc[['μμ°μ‘'], :].values[0]))

                    # fvalue_1 = format(round(df.loc[df['κ΅¬λΆ'] == 'μμ°μ‘', ['μ μ μ€μ ','λΉμ μ€μ ']].values[0][0], 2), ',f')

                    zip_list = list(zip(df_BW_PY.loc[['μμ°μ‘'], :].values[0][:], df_BW_CY.loc[['μμ°μ‘'], :].values[0][:]))
                    
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
                        go.Scatter(name='μ λ μμ°μ‘', x=df_BW_PY.columns[:], y=df_BW_PY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000, mode='lines+markers+text',
                        text=['%.1f'%i for i in df_BW_PY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = 'μ λ: %{y:.1f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='λΉλ μμ°μ‘', x=df_BW_CY.columns[:], y=df_BW_CY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000, mode='lines+markers+text',
                        text=['%.1f'%i for i in df_BW_CY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = 'λΉλ: %{y:.1f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_BW_PY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000, df_BW_CY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000]))*0.7
                    ,max(np.concatenate([df_BW_PY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000, df_BW_CY.loc[['μμ°μ‘'], :].values[0][:]/100_000_000]))*1.3], title_text='μ΅μ')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "μμ°μ‘(μ΅μ)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = '.1f'

                    )

                    st.plotly_chart(fig2, theme=None)

                

                #### μμ°λ: Column B #### 

                value_1 = df_trend_PY.loc[['μμ°λ'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/1_000
                print([f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_11', value_1.sum())

                fvalue_1 = value_1.sum()

                value_2 = df_trend_CY.loc[['μμ°λ'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]/1_000
                print([f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_22', value_2.sum())

                fvalue_2 = value_2.sum()

                differ = fvalue_2/fvalue_1 - 1
                ndiffer = fvalue_2 - fvalue_1

                col_b1, col_b_empty1, col_b2 = st.columns([1,0.5,3])

                with col_b1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ κΈ°', x=['μ κΈ°'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ κΈ°: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='λΉκΈ°', x=['λΉκΈ°'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.0f}' if differ >=0 else f'{fvalue_2:,.0f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉκΈ°: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μμ°λ_λκ³",
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
                            yaxis_title="<b>μμ°λ(ν€,μ²κ°)</b>",
                            
                            annotations=[dict(
                                x='λΉκΈ°',
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
                    zip_list = list(zip(df_trend_PY.loc[['μμ°λ'], :].values[0][:], df_trend_CY.loc[['μμ°λ'], :].values[0][:]))
                    
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
                        go.Scatter(name='μ λ μμ°λ', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['μμ°λ'], :].values[0][:]/1_000, mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_PY.loc[['μμ°λ'], :].values[0][:]/1_000], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = 'μ λ: %{y:,.0f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='λΉλ μμ°λ', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['μμ°λ'], :].values[0][:]/1_000, mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_CY.loc[['μμ°λ'], :].values[0][:]/1_000], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = 'λΉλ: %{y:,.0f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_trend_PY.loc[['μμ°λ'], :].values[0][:]/1_000, df_trend_CY.loc[['μμ°λ'], :].values[0][:]/1_000]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['μμ°λ'], :].values[0][:]/1_000, df_trend_CY.loc[['μμ°λ'], :].values[0][:]/1_000]))*1.3], title_text='μλ')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "μμ°λ(ν€, μ²κ°)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = ','

                    )

                    st.plotly_chart(fig2, theme=None)




                #### μ μ‘°μκ°μ¨: Column C #### 

                value_1 = df_trend_PY.loc[['μ μ‘°μκ°μ¨'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                print([f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_11', value_1.sum())

                BW_cost_1 = df_BW_PY.loc[['λΉκΈ° μ νμ μ‘°μκ°'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                BW_amount_1= df_BW_PY.loc[['μμ°μ‘'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                
                fvalue_1 = BW_cost_1.sum() / BW_amount_1.sum()

                value_2 = df_trend_CY.loc[['μ μ‘°μκ°μ¨'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                print([f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)])
                print('value_22', value_2.sum())

                BW_cost_2 = df_BW_CY.loc[['λΉκΈ° μ νμ μ‘°μκ°'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                BW_amount_2= df_BW_CY.loc[['μμ°μ‘'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                
                fvalue_2 = BW_cost_2.sum() / BW_amount_2.sum()

                differ = fvalue_2 - fvalue_1

                col_c1, col_c_empty1, col_c2 = st.columns([1,0.5,3])

                with col_c1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ κΈ°', x=['μ κΈ°'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.1%}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ κΈ°: %{y:.1%}<extra></extra>',
                        ),

                        go.Bar(name='λΉκΈ°', x=['λΉκΈ°'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.1%}' if differ >=0 else f'{fvalue_2:,.1%}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉκΈ°: %{y:.1%}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': "μ μ‘°μκ°μ¨_λκ³",
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
                            yaxis_title="<b>μ μ‘°μκ°μ¨(%)</b>",
                            yaxis_tickformat = '.0%',
                            
                            annotations=[dict(
                                x='λΉκΈ°',
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
                    zip_list = list(zip(df_trend_PY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:], df_trend_CY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:]))
                    
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
                        go.Scatter(name='μ λ μκ°μ¨', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.1%}' for i in df_trend_PY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:]], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = 'μ λ: %{y:.1%}<extra></extra>',
                        ),
                        
                        go.Scatter(name='λΉλ μκ°μ¨', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.1%}' for i in df_trend_CY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:]], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = 'λΉλ: %{y:.1%}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_trend_PY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:], df_trend_CY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:]]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:], df_trend_CY.loc[['μ μ‘°μκ°μ¨'], :].values[0][:]]))*1.3], title_text='μκ°μ¨')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "μ μ‘°μκ°μ¨(%)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = '.0%'

                    )

                    st.plotly_chart(fig2, theme=None)



                #### μΈμλΉ μμ°μ±: Column D #### 

                # value_1 = df_trend_PY.loc[['μΈμλΉ μμ°μ±'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0] \
                #     / df_trend_PY.loc[['μΈμλΉ μμ°μ±'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                
                trend_volume_1 = df_trend_PY.loc[['μμ°λ'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_inMhr_1 = df_trend_PY.loc[['μμ¬_Mhr'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_outMhr_1 = df_trend_PY.loc[['μΈμ£Ό_Mhr'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
               
                fvalue_1 = trend_volume_1.sum() / (trend_inMhr_1+trend_outMhr_1).sum()

                # value_2 = df_trend_CY.loc[['μΈμλΉ μμ°μ±'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:  -1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                

                trend_volume_2 = df_trend_CY.loc[['μμ°λ'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_inMhr_2 = df_trend_CY.loc[['μμ¬_Mhr'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                trend_outMhr_2 = df_trend_CY.loc[['μΈμ£Ό_Mhr'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]

                fvalue_2 = trend_volume_2.sum() / (trend_inMhr_2+trend_outMhr_2).sum()

                differ = fvalue_2/fvalue_1 - 1
                ndiffer = fvalue_2 - fvalue_1

                col_d1, col_d_empty1, col_d2 = st.columns([1,0.5,3])

                with col_d1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ κΈ°', x=['μ κΈ°'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ κΈ°: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='λΉκΈ°', x=['λΉκΈ°'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.0f}' if differ >=0 else f'{fvalue_2:,.0f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉκΈ°: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': f"μμ°μ±_λκ³",
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
                            yaxis_title="<b>μμ°μ±(ν€,μ²κ° / Mhr)</b>",
                            
                            annotations=[dict(
                                x='λΉκΈ°',
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
                    zip_list = list(zip(df_trend_PY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:], df_trend_CY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:]))
                    
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
                        go.Scatter(name='μ λ μμ°μ±', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_PY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:]], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = 'μ λ: %{y:,.0f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='λΉλ μμ°μ±', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_CY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:]], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = 'λΉλ: %{y:,.0f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[min(np.concatenate([df_trend_PY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:], df_trend_CY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:]]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:], df_trend_CY.loc[['μΈμλΉ μμ°μ±'], :].values[0][:]]))*1.3], title_text='μμ°μ±')
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "μΈμλΉ μμ°μ±(ν€, μ²κ°/Mhr)",
                            'x': 0.45,
                            'xanchor': 'center',
                            'yanchor': 'top',
                        }, title_font_size=18,

                        title_font_family='malgun gothic',
                        hovermode="x unified",
                        yaxis_tickformat = ','

                    )

                    st.plotly_chart(fig2, theme=None)


                #### κ³ κ°λΆλ§: Column E #### 

                value_1 = df_trend_PY.loc[['κ³ κ°λΆλ§'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:-1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                fvalue_1 = value_1.sum()

                value_2 = df_trend_CY.loc[['κ³ κ°λΆλ§'], [f'{i}μ' for i in range(int(selected_month_range[0][0][:  -1]), int(selected_month_range[0][1][:-1])+1)]].values[0]
                fvalue_2 = value_2.sum() 

                differ = fvalue_2 - fvalue_1

                col_e1, col_e_empty1, col_e2 = st.columns([1,0.5,3])

                with col_e1:
                    
                    fig = go.Figure(data=[
                        go.Bar(name='μ κΈ°', x=['μ κΈ°'], y=[fvalue_1],
                        text=[f'{fvalue_1:,.0f}'],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='blue',
                        width=0.5,
                        hovertemplate = 'μ κΈ°: %{y:,.0f}<extra></extra>',
                        ),

                        go.Bar(name='λΉκΈ°', x=['λΉκΈ°'], y=[fvalue_2],
                        text=[f'{fvalue_2:,.0f}' ],
                        textposition='outside',
                        textfont_size=18,
                        marker_color='red',
                        width=0.5,
                        hovertemplate = 'λΉκΈ°: %{y:,.0f}<extra></extra>',
                        )
                    ]
                    )

                    fig.update_yaxes(range=[min([fvalue_1, fvalue_2])*0.5, max([fvalue_1, fvalue_2])*1.3])

                    fig.update_layout(
                        title={
                            'text': f"κ³ κ°λΆλ§_λκ³",
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
                            yaxis_title="<b>κ³ κ°λΆλ§(κ±΄μ)</b>",
                            
                            annotations=[dict(
                                x='λΉκΈ°',
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
                    zip_list = list(zip(df_trend_PY.loc[['κ³ κ°λΆλ§'], :].values[0][:], df_trend_CY.loc[['κ³ κ°λΆλ§'], :].values[0][:]))
                    
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
                        go.Scatter(name='μ λ κ³ κ°λΆλ§', x=df_trend_PY.columns[:], y=df_trend_PY.loc[['κ³ κ°λΆλ§'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_PY.loc[['κ³ κ°λΆλ§'], :].values[0][:]], textposition=fig_text_positions_A,
                        textfont=dict(size=14, color= 'rgb(99,110,250)'),
                        hovertemplate = 'μ λ: %{y:,.0f}<extra></extra>',
                        ),
                        
                        go.Scatter(name='λΉλ κ³ κ°λΆλ§', x=df_trend_CY.columns[:], y=df_trend_CY.loc[['κ³ κ°λΆλ§'], :].values[0][:], mode='lines+markers+text',
                        text=[f'{i:,.0f}' for i in df_trend_CY.loc[['κ³ κ°λΆλ§'], :].values[0][:]], textposition=fig_text_positions_B,
                        textfont=dict(size=14, color= 'rgb(239,85,59)'),
                        hovertemplate = 'λΉλ: %{y:,.0f}<extra></extra>',
                        ),
                    ])

                    fig2.update_yaxes(range=[-0.2 if min(np.concatenate([df_trend_PY.loc[['κ³ κ°λΆλ§'], :].values[0][:], df_trend_CY.loc[['κ³ κ°λΆλ§'], :].values[0][:]]))==0 else min(np.concatenate([df_trend_PY.loc[['κ³ κ°λΆλ§'], :].values[0][:], df_trend_CY.loc[['κ³ κ°λΆλ§'], :].values[0][:]]))*0.7
                    ,max(np.concatenate([df_trend_PY.loc[['κ³ κ°λΆλ§'], :].values[0][:], df_trend_CY.loc[['κ³ κ°λΆλ§'], :].values[0][:]]))*1.3], title_text='κ³ κ°λΆλ§', visible=False)
                    fig2.update_layout(margin=dict(l=50, r=80, t=50, b=20), width=800, height=250)
                    fig2.update_layout(
                        title={
                            'text': "κ³ κ°λΆλ§(κ±΄μ)",
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


            # with st.expander("Data λ³΄κΈ°/μ κΈ°",expanded=True):
            lst_data_tab = ['π ','Data_μ λ','Data_λΉλ']

            tabs_data = st.tabs(lst_data_tab)
            with tabs_data[1]:
                df_BW_PY.dropna(how='all', inplace=True)
                st.dataframe(df_BW_PY.style.format("{:,.0f}"))
            with tabs_data[2]:
                df_BW_CY.dropna(how='all', inplace=True)
                st.dataframe(df_BW_CY.style.format("{:,.0f}"))


  