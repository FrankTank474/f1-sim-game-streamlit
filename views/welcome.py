import streamlit as st
from game.manager import GameManager
from utils.state import navigate_to

def show():
    try:
        # Initialize game manager
        game_manager = GameManager()

        # Main welcome container
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Title section
        st.markdown('<h1 class="big-title">Welcome to the F1 Simulator</h1>', unsafe_allow_html=True)

        # New game creation section
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Game name input
            game_name = st.text_input(
                "Game Name",
                placeholder="Game Name", 
                key="game_name_input",
                label_visibility="collapsed"
            )
            
            # Create new game button
            if st.button("New Game", key="new_game_button", type="primary", use_container_width=True):
                if game_name:
                    try:
                        new_game = game_manager.create_game(game_name, st.session_state.user)
                        st.session_state.game_name = game_name
                        st.session_state.game_id = new_game['id']
                        navigate_to('new_game')
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
                st.markdown('<h2 class="sub-title">Existing Games</h2>', unsafe_allow_html=True)

                # Add column headers
                header_cols = st.columns([2, 1, 1, 1])
                with header_cols[0]:
                    st.markdown('<p class="table-header">Name</p>', unsafe_allow_html=True)
                with header_cols[1]:
                    st.markdown('<p class="table-header">Created</p>', unsafe_allow_html=True)
                with header_cols[2]:
                    st.markdown('<p class="table-header"></p>', unsafe_allow_html=True)
                with header_cols[3]:
                    st.markdown('<p class="table-header"></p>', unsafe_allow_html=True)
                
                # Display each game with actions
                for game in existing_games:
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{game['name']}**")
                    with col2:
                        st.write(f"{game['created_at'][:10]}")
                    with col3:
                        if st.button("Join", key=f"join_{game['id']}", type="secondary", use_container_width=True):
                            try:
                                game = game_manager.join_game(game['id'], st.session_state.user)
                                st.session_state.game_name = game['name']
                                st.session_state.game_id = game['id']
                                navigate_to('new_game')
                            except ValueError as e:
                                st.error(str(e))
                    with col4:
                        if st.button("Delete", key=f"delete_{game['id']}", type="primary", use_container_width=True):
                            game_manager.delete_game(game['id'])
                            st.rerun()

        except Exception as e:
            st.error(f"Error loading existing games: {str(e)}")

    except Exception as e:
        st.error(f"Error in welcome view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line