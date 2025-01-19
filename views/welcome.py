import streamlit as st
from game.manager import GameManager

import streamlit as st
from game.manager import GameManager
from utils.state import navigate_to

def show():
    try:
        # Initialize game manager
        game_manager = GameManager()

        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="big-title">Welcome to the F1 Simulator</h1>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            game_name = st.text_input(
                "Game Name",
                placeholder="Game Name", 
                key="game_name_input",
                label_visibility="collapsed"
            )
            
            if st.button("New Game", key="new_game_button"):
                if game_name:
                    try:
                        new_game = game_manager.create_game(game_name)
                        st.session_state.game_name = game_name
                        st.session_state.game_id = new_game['id']
                        navigate_to('new_game')  # Changed from 'next_page' to 'new_game'
                    except Exception as e:
                        st.error(f"Error creating game: {str(e)}")
                else:
                    st.warning("Please enter a game name")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Existing games section
        try:
            existing_games = game_manager.get_all_games()
            if existing_games:
                st.markdown("---")
                st.markdown("### Existing Games")
                for game in existing_games:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{game['name']}**")
                    with col2:
                        st.write(f"Created: {game['created_at'][:10]}")
                    with col3:
                        if st.button("Delete", key=f"delete_{game['id']}"):
                            game_manager.delete_game(game['id'])
                            st.rerun()
        except Exception as e:
            st.error(f"Error loading existing games: {str(e)}")

    except Exception as e:
        st.error(f"Error in welcome view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line