import streamlit as st

def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    
    if 'game_name' not in st.session_state:
        st.session_state.game_name = None