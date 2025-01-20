import streamlit as st
from game.manager import GameManager
from game.mechanics import GameMechanics
from utils.state import navigate_to

def show():
    try:
        # Initialize managers
        game_manager = GameManager()
        game_mechanics = GameMechanics()
        
        # Get current game state
        game = game_manager.get_game(st.session_state.game_id)
        
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Title section
        st.markdown('<h1 class="big-title">Game Ready</h1>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="sub-title">{game["name"]}</h2>', unsafe_allow_html=True)
        
        # Players table
        st.markdown('<h3 class="section-title">Players & Teams</h3>', unsafe_allow_html=True)
        
        # Table headers
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<p class="table-header">Player</p>', unsafe_allow_html=True)
        with col2:
            st.markdown('<p class="table-header">Team</p>', unsafe_allow_html=True)
        
        # Show active players
        for player in game['players']:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(player['username'])
            with col2:
                team = player['team']
                if team:
                    st.write(team)
                    if 'drivers' in game and team in game['drivers']:
                        drivers = game['drivers'][team]
                        st.write(f"Drivers: {', '.join(drivers)}")
                else:
                    st.write("No team selected")
        
        # Show AI players
        taken_teams = {p['team'] for p in game['players'] if p['team']}
        available_teams = [
            team for team in [
                "Red Bull Racing", "Mercedes", "McLaren", "Ferrari", 
                "Aston Martin", "Alpine", "Williams", "Visa Cash App RB", 
                "Kick Sauber", "Haas F1"
            ] if team not in taken_teams
        ]
        
        for i, team in enumerate(available_teams):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"AI_{i+1}")
            with col2:
                st.write(team)
        
        # Start button
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("Start Season!", type="primary", use_container_width=True):
            # Simulate season and get results
            results = game_mechanics.simulate_season(game['id'], game['players'])
            
            # Store results in session state
            st.session_state.game_results = results
            
            # Navigate to results page
            navigate_to('results')
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in game start view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line