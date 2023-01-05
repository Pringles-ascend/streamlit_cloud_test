import yaml
import streamlit as st
# st.set_page_config(layout="wide", initial_sidebar_state="expanded")

import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from streamlit_authenticator.authenticate import Authenticate

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# import code.pages.intro as intro

# hashed_passwords = stauth.Hasher(['123', '456']).generate()
# print(hashed_passwords)

with open('./_app/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
config['credentials'],
config['cookie']['name'],
config['cookie']['key'],
config['cookie']['expiry_days'],
config['preauthorized']
)


# print(authenticator)

authentication_status = None

if authentication_status == None:
    st.markdown('Streamlit is **_really_ cool**.')

    # no_sidebar_style = """
    # <style>
    #     div[data-testid="stSidebarNav"] {display: none;}
    # </style>
    # """
    # st.markdown(no_sidebar_style, unsafe_allow_html=True)

name, authentication_status, username = authenticator.login('Login', 'main')

# print(authentication_status)
st.session_state.login = False

if authentication_status:
    st.session_state.login = True
    with st.sidebar:
        side_col1, side_col2 = st.columns(2)
        
        with side_col1:
            st.write(f'Welcome *{name}*')
        with side_col2:
            authenticator.logout('Logout', 'main')
    
    st.title('Some content')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    # auth_col2.title("TEST PAGES")
    st.warning('Please enter your username and password')

print("auth: ",st.session_state.login)

# aa