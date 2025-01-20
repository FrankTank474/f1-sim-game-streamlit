import streamlit as st
from utils.state import navigate_back, navigate_to
from game.manager import GameManager

# F1 Teams for 2024
F1_TEAMS = [
    "Red Bull Racing",
    "Mercedes",
    "McLaren",
    "Ferrari",
    "Aston Martin",
    "Alpine",
    "Williams",
    "Visa Cash App RB",
    "Kick Sauber",
    "Haas F1"
]

def get_button_text(team: str) -> str:
    """Get the text to display on the team button"""
    if st.session_state.selected_team == team:
        return f"{team} - Player {st.session_state.user}"
    return team

def init_game_state():
    """Initialize all game-related session state variables"""
    if "selected_team" not in st.session_state:
        st.session_state.selected_team = None
    if "game_state" not in st.session_state:
        st.session_state.game_state = None

def select_team(team: str):
    """Handle team selection for a player"""
    try:
        game_manager = GameManager()
        game = game_manager.select_team(
            st.session_state.game_id,
            st.session_state.user,
            team
        )
        st.session_state.selected_team = team
        st.session_state.game_state = game
        st.rerun()
    except ValueError as e:
        st.error(str(e))

def start_game():
    """Transition to game start state"""
    try:
        game_manager = GameManager()
        game = game_manager.update_game_state(st.session_state.game_id, 'started')
        st.session_state.game_state = game
        navigate_to('game_start')
    except Exception as e:
        st.error(f"Error starting game: {e}")

def show():
    """Main view function for the game setup screen"""
    # Initialize state and manager
    init_game_state()
    game_manager = GameManager()
    
    # Load/update game state if needed
    if not st.session_state.game_state:
        try:
            # Join or get current game state
            game = game_manager.join_game(st.session_state.game_id, st.session_state.user)
            st.session_state.game_state = game
            # Set selected team if player has one
            player = next((p for p in game['players'] if p['username'] == st.session_state.user), None)
            if player and player['team']:
                st.session_state.selected_team = player['team']
        except Exception as e:
            st.error(f"Error joining game: {e}")
            return
    
    # Add back button at the top
    if st.button("← Back"):
        navigate_back()
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="big-title">Game Setup</h1>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="sub-title">{st.session_state.game_name}</h2>', unsafe_allow_html=True)
    
    # Players section
    st.markdown('<h3 class="section-title">Players</h3>', unsafe_allow_html=True)
    
    # Create a table for players
    cols = st.columns(5)
    
    # Show active players and AI slots
    game_players = st.session_state.game_state['players']
    
    # Create all 10 slots
    for slot in range(10):
        col_idx = slot % 5
        if col_idx == 0 and slot > 0:
            cols = st.columns(5)
            
        # Find player in this slot if any
        player = next((p for p in game_players if p['slot'] == slot), None)
        
        if player:
            # Show active player
            is_current_user = player['username'] == st.session_state.user
            css_class = "player-slot player-active" if is_current_user else "player-slot player-other"
            cols[col_idx].markdown(
                f'<div class="{css_class}">{player["username"]}</div>',
                unsafe_allow_html=True
            )
        else:
            # Show AI slot
            cols[col_idx].markdown(
                f'<div class="player-slot player-ai">AI {slot+1}</div>',
                unsafe_allow_html=True
            )
    
    # Teams section
    st.markdown('<h3 class="section-title">Teams</h3>', unsafe_allow_html=True)
    cols = st.columns(2)
    
    # Get list of taken teams
    taken_teams = {p['team'] for p in game_players if p['team']}
    
    # Left column teams
    with cols[0]:
        for team in F1_TEAMS[:5]:
            is_selected = st.session_state.selected_team == team
            is_taken = team in taken_teams and not is_selected
            
            if is_taken:
                # Show who has taken this team
                player = next(p for p in game_players if p['team'] == team)
                st.button(
                    f"{team} - Player {player['username']}", 
                    key=f"left_{team}",
                    use_container_width=True,
                    disabled=True
                )
            else:
                if st.button(
                    get_button_text(team), 
                    key=f"left_{team}", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    select_team(team)
    
    # Right column teams
    with cols[1]:
        for team in F1_TEAMS[5:]:
            is_selected = st.session_state.selected_team == team
            is_taken = team in taken_teams and not is_selected
            
            if is_taken:
                # Show who has taken this team
                player = next(p for p in game_players if p['team'] == team)
                st.button(
                    f"{team} - Player {player['username']}", 
                    key=f"right_{team}",
                    use_container_width=True,
                    disabled=True
                )
            else:
                if st.button(
                    get_button_text(team), 
                    key=f"right_{team}", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    select_team(team)
    
    # Add Ready button at the bottom
    st.markdown('<div class="ready-button-container">', unsafe_allow_html=True)
    
    # Only enable Ready button if player has selected a team
    is_ready = st.session_state.selected_team is not None
    if st.button(
        "Ready!", 
        key="ready_button",
        disabled=not is_ready,
        type="primary" if is_ready else "secondary",
        use_container_width=True
    ):
        start_game()
    
    if not is_ready:
        st.info("Please select a team before starting the game")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)