import streamlit as st
from utils.state import navigate_to, navigate_back
from game.manager import GameManager, GamePhase
from game.data import TEAMS

def get_button_text(team_name: str, game_state: dict) -> str:
    """Get the text to display on the team button"""
    # Find if current user has this team in this specific game
    player = next((p for p in game_state['players'] 
                  if p['username'] == st.session_state.user), None)
    if player and player['team'] == team_name:
        return f"{team_name} - Player {st.session_state.user}"
    return team_name

def init_game_state():
    """Initialize all game-related session state variables"""
    if "game_state" not in st.session_state:
        st.session_state.game_state = None

def select_team(team: str):
    """Handle team selection for the current player"""
    try:
        game_manager = GameManager()
        game = game_manager.select_team(
            st.session_state.game_id,
            st.session_state.user,
            team
        )
        st.session_state.game_state = game
        st.rerun()
    except ValueError as e:
        st.error(str(e))

def show():
    """Display the new game view"""
    # Initialize state and manager
    init_game_state()
    game_manager = GameManager()
    
    # Always get fresh game state
    try:
        # Get current game state
        game = game_manager.get_game(st.session_state.game_id)
        st.session_state.game_state = game
    except Exception as e:
        st.error(f"Error loading game: {e}")
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
    
    # Get list of taken teams in this specific game
    taken_teams = {p['team'] for p in game_players if p['team']}
    
    # Get current user's team in this game
    current_player = next((p for p in game_players if p['username'] == st.session_state.user), None)
    current_team = current_player['team'] if current_player else None
    
    # Left column teams
    with cols[0]:
        for team in TEAMS[:5]:
            is_selected = current_team == team.name
            is_taken = team.name in taken_teams and not is_selected
            
            if is_taken:
                # Show who has taken this team
                player = next(p for p in game_players if p['team'] == team.name)
                st.button(
                    f"{team.name} - Player {player['username']}", 
                    key=f"left_{team.name}",
                    use_container_width=True,
                    disabled=True
                )
            else:
                if st.button(
                    get_button_text(team.name, st.session_state.game_state), 
                    key=f"left_{team.name}", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    select_team(team.name)
    
    # Right column teams
    with cols[1]:
        for team in TEAMS[5:]:
            is_selected = current_team == team.name
            is_taken = team.name in taken_teams and not is_selected
            
            if is_taken:
                # Show who has taken this team
                player = next(p for p in game_players if p['team'] == team.name)
                st.button(
                    f"{team.name} - Player {player['username']}", 
                    key=f"right_{team.name}",
                    use_container_width=True,
                    disabled=True
                )
            else:
                if st.button(
                    get_button_text(team.name, st.session_state.game_state), 
                    key=f"right_{team.name}", 
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    select_team(team.name)

    # Add Start button when all human players have selected teams
    all_players_ready = all(p['team'] is not None for p in game_players)
    if all_players_ready:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Game!", type="primary", use_container_width=True):
            # Update game phase
            game_manager.update_game_phase(st.session_state.game_id, GamePhase.DRIVER_SELECTION)
            # Clear any previous driver selections
            if 'driver_selections' in st.session_state:
                del st.session_state.driver_selections
            navigate_to('select_drivers')
    
    st.markdown('</div>', unsafe_allow_html=True)