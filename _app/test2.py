import yaml
import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from streamlit_authenticator.authenticate import Authenticate

import test3

# hashed_passwords = stauth.Hasher(['123', '456']).generate()
# print(hashed_passwords)

with open('./config.yaml') as file:
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
auth_col1, auth_col2, auth_col3 = st.columns(3)

if authentication_status == None:
    st.markdown('Streamlit is **_really_ cool**.')

with auth_col2:
    name, authentication_status, username = authenticator.login('Login', 'main')

# print(authentication_status)

if authentication_status:
    
    with st.sidebar:
        side_col1, side_col2 = st.columns(2)
        
        with side_col1:
            st.write(f'Welcome *{name}*')
        with side_col2:
            authenticator.logout('Logout', 'main')
    
    st.title('Some content')
    auth_col1, auth_col2, auth_col3 = st.columns(3)
    auth_col2.empty()
    test3.Paging(name)
elif authentication_status == False:
    auth_col2.error('Username/password is incorrect')
elif authentication_status == None:
    # auth_col2.title("TEST PAGES")
    auth_col2.warning('Please enter your username and password')

# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')