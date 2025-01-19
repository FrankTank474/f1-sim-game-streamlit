import streamlit as st
from utils.state import navigate_back

def show():
    # Add back button at the top
    if st.button("← Back"):
        navigate_back()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="big-title">New Game</h1>', unsafe_allow_html=True)
    
    # Display game information
    st.write(f"Game Name: {st.session_state.game_name}")
    st.write(f"Game ID: {st.session_state.game_id}")
    
    st.markdown('</div>', unsafe_allow_html=True)