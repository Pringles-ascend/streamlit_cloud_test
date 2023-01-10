import streamlit as st
import time
import numpy as np
import plotly.express as px
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

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


    path = r'M:\Users\LGCARE\Documents\download\SAP5WIRSLW8HK3NZESFI3SJ0H7SK.xls'

    df = pd.read_excel(r'M:\Users\LGCARE\Documents\read_test.xlsx', engine='openpyxl', header=17)
    df = df.drop(index=0)

    df.columns = df.columns.str.replace('\n', ' ')
    df.columns = df.columns.str.replace('Unnamed: 0', '구분')
    df['구분'] = df['구분'].str.lstrip()

    print(df)

    print(df['구분'])

    fig = px.bar(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']], color_discrete_sequence=px.colors.sequential.RdBu)

    st.plotly_chart(fig)

