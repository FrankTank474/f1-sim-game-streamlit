import streamlit as st
from components.styles import get_css
from utils.state import init_session_state
from views import welcome

def main():
    # Configure the page
    st.set_page_config(
        page_title="F1 Simulator",
        layout="centered"
    )
    
    # Apply CSS
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)

    # Initialize session state
    init_session_state()

    # Handle different pages
    if st.session_state.page == 'welcome':
        welcome.show()
    elif st.session_state.page == 'next_page':
        st.write(f"Next page (game: {st.session_state.game_name})")

if __name__ == "__main__":
    main()