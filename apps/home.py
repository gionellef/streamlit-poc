import streamlit as st
import streamlit_authenticator as stauth

def app():
    
    st.title('Home')

    st.write("Welcome to the UP Manila Executive Dashboard")

    names = ['John Smith','Rebecca Briggs']
    usernames = ['jsmith','rbriggs']
    passwords = ['123','456']
    st.markdown("### Enter your login details: ")
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)
    
    name, authentication_status, username = authenticator.login('Login','main')