import streamlit as st
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

print("plotting: ", st.session_state.login)

if st.session_state.login==False:
    st.warning("You must log-in to see the content of this sensitive page! Head over to the log-in page.")
    st.stop()  # App won't run anything after this line

else:
    st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout="wide")

    st.markdown("# Plotting Demo")
    st.sidebar.header("Plotting Demo")
    st.write(
        """This demo illustrates a combination of plotting and animation with
    Streamlit. We're generating a bunch of random numbers in a loop for around
    5 seconds. Enjoy!"""
    )

    # progress_bar = st.sidebar.progress(0)
    # status_text = st.sidebar.empty()
    # last_rows = np.random.randn(1, 1)
    # chart = st.line_chart(last_rows)

    # for i in range(1, 101):
    #     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    #     status_text.text("%i%% Complete" % i)
    #     chart.add_rows(new_rows)
    #     progress_bar.progress(i)
    #     last_rows = new_rows
    #     time.sleep(0.05)

    # progress_bar.empty()

    # # Streamlit widgets automatically run the script from top to bottom. Since
    # # this button is not connected to any other logic, it just causes a plain
    # # rerun.
    # st.button("Re-run")


    with st.sidebar:
        uploaded_file = st.file_uploader("Choose a file", type="xlsx")
    if uploaded_file is not None:
        # # To read file as bytes:
        # bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # # To convert to a string based IO:
        # stringio = StringIO(uploaded_file.getvalue().decode("cp949"))
        # st.write(stringio)

        # # To read file as string:
        # string_data = stringio.read()
        # st.write(string_data)

        # # Can be used wherever a "file-like" object is accepted:
        df = pd.read_excel(uploaded_file, engine='openpyxl', header=17, sheet_name='BW')
        df = df.drop(index=0)
        df.columns = df.columns.str.replace('\n', ' ')
        df.columns = df.columns.str.replace('Unnamed: 0', '구분')
        df['구분'] = df['구분'].str.lstrip()


        st.write((df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']]/100000000).style.format("{:.1f}"))
        
        col_a1, col_a2 = st.columns(2)
    
        with col_a1:
            
            
            value_1 = df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][0] / 100000000
            value_2 = df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][1] / 100000000

            fvalue_1 = format(round(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][0], 2), ',f')
            fvalue_2 = format(round(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][1]), ',d')
            differ = df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][1]/df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']].values[0][0] - 1

            fig = go.Figure(data=[
                go.Bar(name='전월', x=['전월'], y=[value_1],
                text=[f'{value_1:,.1f}'],
                textposition='outside',
                textfont_size=18,
                marker_color='blue'
                ),

                go.Bar(name='당월', x=['당월'], y=[value_2],
                text=[f'{value_2:,.1f}<br>(+{differ:.2%})' if differ >=0 else f'{fvalue_2}<br>(-{differ}%)' ],
                textposition='outside',
                textfont_size=18,
                marker_color='red'
                )
            ]

            )
            fig.update_yaxes(range=[min([value_1, value_2])*0.5, max([value_1, value_2])*1.2])
            st.plotly_chart(fig)


        with col_a2:

            value_3 = df.loc[df['구분'] == '생산량', ['전월 실적','당월 실적']].values[0][0] / 1000
            value_4 = df.loc[df['구분'] == '생산량', ['전월 실적','당월 실적']].values[0][1] / 1000

            fig2 = go.Figure(data=[
                go.Bar(name='전월', x=['전월'], y=[value_3],
                text=[f'{value_3:,.1f}'],
                textposition='outside',
                textfont_size=18,
                marker_color='blue'
                ),
                


                go.Bar(name='당월', x=['당월'], y=[value_4],
                text=[f'{value_4:,.1f}<br>(+{differ:.2%})' if differ >=0 else f'{fvalue_2}<br>(-{differ}%)' ],
                textposition='outside',
                textfont_size=18,
                marker_color='red'
                )
            ]

            )
            fig2.update_yaxes(range=[min([value_3, value_4])*0.5, max([value_3, value_4])*1.2])
            st.plotly_chart(fig2)

        df2 = pd.read_excel(uploaded_file, sheet_name='Trend', engine='openpyxl')

        
        fig = go.Figure(data=[
            go.Scatter(name='생산액', x=df2.columns[1:], y=df2.loc[df2['구분'] == '생산액'].values[0][1:], mode='lines+markers+text',
            text=df2.loc[df2['구분'] == '생산액'].values[0][1:], textposition='top center'),
            go.Scatter(name='생산량', x=df2.columns[1:], y=df2.loc[df2['구분'] == '생산량'].values[0][1:], mode='lines+markers'),
        ])

        fig.update_yaxes(range=[0,max(df2.loc[df2['구분'] == '생산량'].values[0][1:])*1.2])
        fig.update_layout(width=1200, height=500)

        st.plotly_chart(fig)

