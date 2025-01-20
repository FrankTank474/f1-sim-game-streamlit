import streamlit as st
from components.styles import get_css
from utils.state import init_session_state
from views import welcome, new_game, login, game_start, results, select_drivers, pre_season

def main():
    """
    Main entry point for the F1 Simulator application.
    Handles page configuration, routing, and session state.
    """
    # Configure the basic page settings
    st.set_page_config(
        page_title="F1 Simulator",
        layout="centered"    # Centers all content on the page
    )
    
    # Load and apply our custom CSS styles
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)

    # Initialize session state variables (like user login status, current page, etc.)
    init_session_state()

    # Route to appropriate page based on session state
    if st.session_state.page == 'login':
        # Show login page if we're on the login page
        login.show()
    elif not st.session_state.is_logged_in:
        # If user isn't logged in, redirect to login page
        st.session_state.page = 'login'
        st.rerun()
    elif st.session_state.page == 'welcome':
        # Show welcome page (list of games)
        welcome.show()
    elif st.session_state.page == 'new_game':
        # Show new game page (team selection)
        new_game.show()
    elif st.session_state.page == 'select_drivers':
        # Show driver selection page
        select_drivers.show()
    elif st.session_state.page == 'pre_season':
        # Show pre-season development page
        pre_season.show()
    elif st.session_state.page == 'game_start':
        # Show game start page (final lineup and start button)
        game_start.show()
    elif st.session_state.page == 'results':
        # Show results page (championship winners)
        results.show()

# This is the entry point of the application
if __name__ == "__main__":
    main()