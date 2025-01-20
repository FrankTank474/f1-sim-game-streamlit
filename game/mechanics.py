import random
from typing import Dict, List
import json
from pathlib import Path
from datetime import datetime

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
        # Get all teams that are in play (both player and AI)
        teams = []
        for player in players:
            if player['team']:
                teams.append({
                    'name': player['team'],
                    'is_ai': False,
                    'player': player['username']
                })
        
        # Fill remaining slots with AI teams
        available_teams = set([
            "Red Bull Racing", "Mercedes", "McLaren", "Ferrari", 
            "Aston Martin", "Alpine", "Williams", "Visa Cash App RB", 
            "Kick Sauber", "Haas F1"
        ]) - set(team['name'] for team in teams)
        
        for team in available_teams:
            teams.append({
                'name': team,
                'is_ai': True,
                'player': f"AI_{team}"
            })
            
        # Randomly select winners
        driver_champion = random.choice(teams)
        constructor_champion = random.choice(teams)
        
        # Create result for this season
        result = {
            'timestamp': datetime.now().isoformat(),
            'drivers_championship': {
                'winner': driver_champion['name'],
                'is_ai': driver_champion['is_ai'],
                'player': driver_champion['player']
            },
            'constructors_championship': {
                'winner': constructor_champion['name'],
                'is_ai': constructor_champion['is_ai'],
                'player': constructor_champion['player']
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