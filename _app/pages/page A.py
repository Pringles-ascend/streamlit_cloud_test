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
        df = pd.read_excel(uploaded_file, engine='openpyxl', header=17)
        df = df.drop(index=0)
        df.columns = df.columns.str.replace('\n', ' ')
        df.columns = df.columns.str.replace('Unnamed: 0', '구분')
        df['구분'] = df['구분'].str.lstrip()


        st.write(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']])
        fig = px.bar(df.loc[df['구분'] == '생산액', ['전월 실적','당월 실적']], color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig)

