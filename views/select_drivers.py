import streamlit as st
from utils.state import navigate_to, navigate_back
from game.manager import GameManager, GamePhase
from game.data import DRIVERS, TEAMS

def get_available_drivers(selected_drivers: dict) -> list:
    """Get list of drivers that haven't been selected by any team"""
    taken_drivers = [driver for team_drivers in selected_drivers.values() 
                    for driver in team_drivers]
    return [driver.name for driver in DRIVERS 
            if driver.name not in taken_drivers]

def show():
    try:
        # Initialize manager
        game_manager = GameManager()
        
        # Get current game state
        game = game_manager.get_game(st.session_state.game_id)
        
        # Initialize or get driver selections from session state
        if 'driver_selections' not in st.session_state:
            st.session_state.driver_selections = {}
            # Load any existing selections from game data
            if 'drivers' in game:
                st.session_state.driver_selections = game['drivers']
        
        # Get current user's team
        current_player = next((p for p in game['players'] 
                             if p['username'] == st.session_state.user), None)
        if not current_player or not current_player['team']:
            st.error("No team selected!")
            return
            
        current_team = current_player['team']
        
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Title section
        st.markdown('<h1 class="big-title">Select Drivers</h1>', unsafe_allow_html=True)
        st.markdown(f'<h2 class="sub-title">{current_team}</h2>', unsafe_allow_html=True)
        
        # Show available budget
        team_data = next(team for team in TEAMS if team.name == current_team)
        budget = team_data.budget
        
        # Calculate remaining budget
        selected_drivers = st.session_state.driver_selections.get(current_team, [])
        spent_budget = sum(driver.price for driver in DRIVERS 
                         if driver.name in selected_drivers)
        remaining_budget = budget - spent_budget
        
        st.markdown(f'<h3 class="section-title">Budget: ${remaining_budget:,}</h3>', 
                   unsafe_allow_html=True)
        
        # Get list of available drivers
        available_drivers = get_available_drivers(st.session_state.driver_selections)
        
        # Add current team's selected drivers back to available list
        available_drivers.extend(selected_drivers)
        available_drivers = sorted(list(set(available_drivers)))
        
        # Driver selection section
        st.markdown('<h3 class="section-title">Select Your Drivers</h3>', 
                   unsafe_allow_html=True)
        
        # Create two columns for driver selection
        col1, col2 = st.columns(2)
        
        # First driver selection
        with col1:
            driver1_index = 0
            if len(selected_drivers) > 0:
                try:
                    driver1_index = available_drivers.index(selected_drivers[0])
                except ValueError:
                    pass
                    
            driver1 = st.selectbox(
                "First Driver",
                available_drivers,
                index=driver1_index,
                key="driver1"
            )
            
            # Show driver stats
            driver1_data = next(d for d in DRIVERS if d.name == driver1)
            st.write(f"Skill: {driver1_data.skill}")
            st.write(f"Consistency: {driver1_data.consistency}")
            st.write(f"Salary: ${driver1_data.price:,}")
        
        # Second driver selection
        with col2:
            remaining_drivers = [d for d in available_drivers if d != driver1]
            driver2_index = 0
            if len(selected_drivers) > 1:
                try:
                    driver2_index = remaining_drivers.index(selected_drivers[1])
                except ValueError:
                    pass
                    
            driver2 = st.selectbox(
                "Second Driver",
                remaining_drivers,
                index=driver2_index,
                key="driver2"
            )
            
            # Show driver stats
            driver2_data = next(d for d in DRIVERS if d.name == driver2)
            st.write(f"Skill: {driver2_data.skill}")
            st.write(f"Consistency: {driver2_data.consistency}")
            st.write(f"Salary: ${driver2_data.price:,}")
        
        # Calculate total cost
        total_cost = driver1_data.price + driver2_data.price
        if total_cost > budget:
            st.error(f"Total cost ${total_cost:,} exceeds budget ${budget:,}")
        else:
            # Save button
            if st.button("Confirm Drivers", type="primary", use_container_width=True):
                # Save selections to session state and game data
                st.session_state.driver_selections[current_team] = [driver1, driver2]
                
                # Save to games.json through game manager
                game = game_manager.select_drivers(
                    st.session_state.game_id,
                    current_team,
                    [driver1, driver2]
                )
                
                # Check if all players have selected drivers
                all_selections_made = True
                for player in game['players']:
                    if player['team']:
                        if 'drivers' not in game or player['team'] not in game.get('drivers', {}):
                            all_selections_made = False
                            break
                
                if all_selections_made:
                    # Update game phase and move to pre-season
                    game_manager.update_game_phase(st.session_state.game_id, GamePhase.PRE_SEASON)
                    navigate_to('pre_season')
                else:
                    st.success("Drivers selected! Waiting for other players...")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error in driver selection view: {str(e)}")
        st.write("Debug info:", str(e))  # Temporary debug line