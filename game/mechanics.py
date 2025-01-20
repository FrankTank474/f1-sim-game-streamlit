import random
from typing import Dict, List
import json
from pathlib import Path

class GameMechanics:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.results_file = self.data_dir / "results.json"
        
    def _save_results(self, results: Dict):
        """Save game results to JSON file"""
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
        
        # Create results
        results = {
            'game_id': game_id,
            'drivers_championship': {
                'winner': driver_champion['name'],
                'is_ai': driver_champion['is_ai'],
                'player': driver_champion['player']
            },
            'constructors_championship': {
                'winner': constructor_champion['name'],
                'is_ai': constructor_champion['is_ai'],
                'player': constructor_champion['player']
            }
        }
        
        # Save results
        self._save_results(results)
        return results