import streamlit as st

print("intro: ",st.session_state.login)
print("intro: ",type(st.session_state.login))

if st.session_state.login:
    print('pass')

if st.session_state.login==False:
    print('stop')
    st.warning("You must log-in to see the content of this sensitive page! Head over to the log-in page.")
    st.stop()  # App won't run anything after this line

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

st.write("# Welcome to Streamlit! 👋")
st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.

    **👈 Select a demo from the dropdown on the left** to see some examples
    of what Streamlit can do!

    ### Want to learn more?

    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
    forums](https://discuss.streamlit.io)

    ### See more complex demos

    - Use a neural net to [analyze the Udacity Self-driving Car Image
    Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)