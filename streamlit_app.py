import streamlit as st
from components.styles import get_css
from utils.state import init_session_state
from views import welcome, new_game

def main():
    st.set_page_config(
        page_title="F1 Simulator",
        layout="centered"
    )
    
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)

    init_session_state()

    if st.session_state.page == 'welcome':
        welcome.show()
    elif st.session_state.page == 'new_game':
        new_game.show()

if __name__ == "__main__":
    main()