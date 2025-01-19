import streamlit as st

def show():
    # Create a container div for centering
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="big-title">Welcome to the F1 Simulator</h1>', unsafe_allow_html=True)

    # Create columns for centering
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Input field
        game_name = st.text_input("", placeholder="Game Name", label_visibility="collapsed")
        
        # Button
        if st.button("New Game"):
            if game_name:
                st.session_state.game_name = game_name
                st.session_state.page = 'next_page'
                st.rerun()
            else:
                st.warning("Please enter a game name")
    
    # Close the container div
    st.markdown('</div>', unsafe_allow_html=True)