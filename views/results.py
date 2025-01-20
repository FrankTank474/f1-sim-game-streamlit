import streamlit as st
from utils.state import navigate_to

def show():
    try:
        # Get results from session state
        results = st.session_state.game_results
        
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Title section
        st.markdown('<h1 class="big-title">Season Results!</h1>', unsafe_allow_html=True)
        
        # Drivers Championship
        st.markdown('<h2 class="section-title">Drivers Championship</h2>', unsafe_allow_html=True)
        driver_winner = results['drivers_championship']
        
        if driver_winner['is_ai']:
            st.markdown(
                f'<div class="result-box ai-winner">'
                f'🏆 {driver_winner["driver"]} of {driver_winner["team"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-box player-winner">'
                f'🏆 {driver_winner["driver"]} of {driver_winner["team"]}</div>',
                unsafe_allow_html=True
            )
        
        # Constructors Championship
        st.markdown('<h2 class="section-title">Constructors Championship</h2>', unsafe_allow_html=True)
        constructor_winner = results['constructors_championship']
        
        if constructor_winner['is_ai']:
            st.markdown(
                f'<div class="result-box ai-winner">'
                f'🏆 {constructor_winner["team"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-box player-winner">'
                f'🏆 {constructor_winner["team"]}</div>',
                unsafe_allow_html=True
            )
        
        # Back to welcome button
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Back to Welcome", type="primary", use_container_width=True):
            # Clear game state
            st.session_state.game_id = None
            st.session_state.game_name = None
            st.session_state.game_results = None
            navigate_to('welcome')
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in results view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line