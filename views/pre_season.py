import streamlit as st
from utils.state import navigate_to, navigate_back
from game.manager import GameManager, GamePhase
from game.data import TEAMS

# Pre-season upgrade options and their costs
UPGRADES = {
    "hydraulics": {"cost": 8000000, "description": "Improves car reliability and handling"},
    "aerodynamics": {"cost": 15000000, "description": "Better downforce and straight-line speed"},
    "tyres": {"cost": 5000000, "description": "Better tyre wear and grip"},
    "power_unit": {"cost": 20000000, "description": "More power and better fuel efficiency"},
    "brakes": {"cost": 7000000, "description": "Enhanced braking performance"},
    "driver_fitness": {"cost": 3000000, "description": "Improves driver stamina"},
    "driver_reactions": {"cost": 4000000, "description": "Faster response times"},
    "driver_mentality": {"cost": 2000000, "description": "Better focus and race management"}
}

def save_upgrade(game_id: str, team: str, upgrade: str) -> None:
    """Save the selected upgrade to the game data"""
    game_manager = GameManager()
    game = game_manager.get_game(game_id)
    
    # Initialize upgrades if not present
    if 'upgrades' not in game:
        game['upgrades'] = {}
    
    # Save the team's upgrade choice
    game['upgrades'][team] = upgrade
    
    # Save changes
    game_manager.save_game(game)

def show():
    try:
        # Initialize manager
        game_manager = GameManager()
        
        # Get current game state
        game = game_manager.get_game(st.session_state.game_id)
        
        # Get current user's team
        current_player = next((p for p in game['players'] 
                             if p['username'] == st.session_state.user), None)
        if not current_player or not current_player['team']:
            st.error("No team selected!")
            return
            
        current_team = current_player['team']
        
        # Get team data
        team_data = next(team for team in TEAMS if team.name == current_team)
        
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Title section
        st.markdown('<h1 class="big-title">Pre-Season Development</h1>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="sub-title">{current_team}</h2>', unsafe_allow_html=True)
        
        # Budget information
        st.markdown(f'<h3 class="section-title">Available Budget: ${team_data.budget:,}</h3>', 
                   unsafe_allow_html=True)
        
        # Get current selection
        current_upgrade = game.get('upgrades', {}).get(current_team)
        
        # Upgrade selection section
        st.markdown('<h3 class="section-title">Select One Upgrade</h3>', 
                   unsafe_allow_html=True)
        
        # Create upgrade cards as buttons
        cols = st.columns(2)
        for idx, (upgrade, details) in enumerate(UPGRADES.items()):
            col = cols[idx % 2]
            with col:
                # Check if this upgrade is selected
                is_selected = upgrade == current_upgrade
                # Check if within budget
                can_afford = details['cost'] <= team_data.budget
                
                if is_selected:
                    background_color = "#DC2626"  # Red for selected
                    button_type = "primary"
                    button_text = f"{upgrade.replace('_', ' ').title()} (Selected)"
                elif not can_afford:
                    background_color = "#9CA3AF"  # Gray for unaffordable
                    button_type = "secondary"
                    button_text = f"{upgrade.replace('_', ' ').title()} - ${details['cost']:,}"
                else:
                    background_color = "rgb(45, 160, 88)"  # Green for available
                    button_type = "secondary"
                    button_text = f"{upgrade.replace('_', ' ').title()} - ${details['cost']:,}"
                
                if st.button(
                    button_text,
                    key=f"upgrade_{upgrade}",
                    type=button_type,
                    disabled=not can_afford,
                    use_container_width=True
                ):
                    save_upgrade(st.session_state.game_id, current_team, upgrade)
                    st.rerun()
                
                # Show description under button
                st.markdown(f"<p style='font-size: 0.9em; color: #666;'>{details['description']}</p>", 
                          unsafe_allow_html=True)
        
        # Add Continue button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Continue", type="primary", use_container_width=True):
            if current_upgrade:  # Only proceed if an upgrade is selected
                game_manager.update_game_phase(st.session_state.game_id, GamePhase.SEASON)
                navigate_to('game_start')
            else:
                st.error("Please select an upgrade before continuing")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in pre-season view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line