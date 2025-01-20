import random
from typing import Dict, List
import json
from pathlib import Path
from datetime import datetime
from game.data import TEAMS, get_default_driver_assignments

class GameMechanics:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.results_file = self.data_dir / "results.json"
        self._initialize_results_file()
        
        # Initialize game manager for archiving
        from game.manager import GameManager
        self.game_manager = GameManager(data_dir)
        
    def _initialize_results_file(self):
        """Initialize results file if it doesn't exist"""
        if not self.results_file.exists():
            with open(self.results_file, 'w') as f:
                json.dump({}, f)  # Empty dict to store results by game_id
                
    def _load_results(self) -> Dict:
        """Load all historical results"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
            
    def _save_results(self, results: Dict):
        """Save all results back to file"""
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
    def simulate_season(self, game_id: str, players: List[Dict]) -> Dict:
        """
        Simulate an entire F1 season and determine champions
        For now, just randomly select winners
        """
        # Get all participating drivers
        game = self.game_manager.get_game(game_id)
        all_drivers = []

        # First add human players' drivers
        for player in players:
            if player['team'] and player['team'] in game.get('drivers', {}):
                team_drivers = game['drivers'][player['team']]
                for driver_name in team_drivers:
                    all_drivers.append({
                        'name': driver_name,
                        'team': player['team'],
                        'is_ai': False
                    })

        # Fill remaining teams with default drivers
        default_assignments = get_default_driver_assignments()
        available_teams = set([team.name for team in TEAMS]) - {p['team'] for p in players if p['team']}
        
        for team in available_teams:
            for driver_name in default_assignments[team]:
                all_drivers.append({
                    'name': driver_name,
                    'team': team,
                    'is_ai': True
                })
            
        # Randomly select winners
        driver_champion = random.choice(all_drivers)
        constructor_champion = random.choice([team.name for team in TEAMS])
        
        # Create result for this season
        result = {
            'timestamp': datetime.now().isoformat(),
            'drivers_championship': {
                'driver': driver_champion['name'],
                'team': driver_champion['team'],
                'is_ai': driver_champion['is_ai']
            },
            'constructors_championship': {
                'team': constructor_champion,
                'is_ai': constructor_champion not in {p['team'] for p in players if p['team']}
            },
            'players': players  # Store final player lineup
        }
        
        # Load existing results and add this one
        all_results = self._load_results()
        all_results[game_id] = result
        
        # Save updated results
        self._save_results(all_results)
        
        # Archive the game
        self.game_manager.archive_game(game_id)
        
        return result
        
    def get_game_results(self, game_id: str) -> Dict:
        """Get historical results for a specific game"""
        results = self._load_results()
        return results.get(game_id)