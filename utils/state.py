import streamlit as st

def init_session_state():
    if 'page_history' not in st.session_state:
        st.session_state.page_history = ['login']
    
    if 'game_name' not in st.session_state:
        st.session_state.game_name = None
        
    if 'game_id' not in st.session_state:
        st.session_state.game_id = None
        
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
        
    if 'user' not in st.session_state:
        st.session_state.user = None
        
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

def navigate_to(page: str):
    st.session_state.page_history.append(page)
    st.session_state.page = page
    st.rerun()

def navigate_back():
    if len(st.session_state.page_history) > 1:
        st.session_state.page_history.pop()  # Remove current page
        st.session_state.page = st.session_state.page_history[-1]  # Go to previous page
        st.rerun()

def logout():
    st.session_state.user = None
    st.session_state.is_logged_in = False
    st.session_state.page_history = ['login']
    st.session_state.page = 'login'
    st.rerun()