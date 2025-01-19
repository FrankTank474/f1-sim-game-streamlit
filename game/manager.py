import json
from pathlib import Path
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.games_file = self.data_dir / "games.json"
        self._initialize_data_store()
    
    def _initialize_data_store(self):
        if not self.games_file.exists():
            with open(self.games_file, 'w') as f:
                json.dump([], f)

    def _generate_game_id(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        games = self._load_games()
        suffix = 1
        
        # Handle multiple games created in the same second
        base_id = f"{timestamp}_{suffix}"
        existing_ids = {game['id'] for game in games}
        
        while base_id in existing_ids:
            suffix += 1
            base_id = f"{timestamp}_{suffix}"
            
        return base_id

    def _load_games(self) -> List[Dict]:
        try:
            with open(self.games_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Error reading games file, returning empty list")
            return []

    def _save_games(self, games: List[Dict]):
        with open(self.games_file, 'w') as f:
            json.dump(games, f, indent=2)
    
    def create_game(self, game_name: str, creator: str) -> Dict:
        """Create a new game with the first player"""
        try:
            games = self._load_games()
            
            new_game = {
                'id': self._generate_game_id(),
                'name': game_name,
                'created_at': datetime.now().isoformat(),
                'status': 'active',
                'creator': creator,
                'players': [
                    {
                        'username': creator,
                        'slot': 0,  # Creator always gets first slot
                        'team': None
                    }
                ]
            }
            
            games.append(new_game)
            self._save_games(games)
            
            logger.info(f"Created new game: {new_game}")
            return new_game
            
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            raise

    def join_game(self, game_id: str, username: str) -> Dict:
        """Add a player to an existing game"""
        try:
            games = self._load_games()
            game = next((g for g in games if g['id'] == game_id), None)
            
            if not game:
                raise ValueError(f"Game {game_id} not found")
            
            if any(p['username'] == username for p in game['players']):
                # Player already in game, return game state
                return game
            
            # Find next available slot (max 5 players)
            taken_slots = {p['slot'] for p in game['players']}
            available_slots = set(range(5)) - taken_slots
            
            if not available_slots:
                raise ValueError("Game is full")
            
            next_slot = min(available_slots)
            
            # Add player to game
            game['players'].append({
                'username': username,
                'slot': next_slot,
                'team': None
            })
            
            # Update games list
            self._save_games(games)
            return game
            
        except Exception as e:
            logger.error(f"Error joining game: {e}")
            raise

    def select_team(self, game_id: str, username: str, team: str) -> Dict:
        """Update a player's team selection"""
        try:
            games = self._load_games()
            game = next((g for g in games if g['id'] == game_id), None)
            
            if not game:
                raise ValueError(f"Game {game_id} not found")
            
            # Find player in game
            player = next((p for p in game['players'] if p['username'] == username), None)
            if not player:
                raise ValueError(f"Player {username} not in game {game_id}")
            
            # Check if team is already taken
            if any(p['team'] == team for p in game['players'] if p['username'] != username):
                raise ValueError(f"Team {team} is already taken")
            
            # Update player's team
            player['team'] = team
            
            # Save changes
            self._save_games(games)
            return game
            
        except Exception as e:
            logger.error(f"Error selecting team: {e}")
            raise

    def get_game(self, game_id: str) -> Dict:
        """Get current state of a game"""
        games = self._load_games()
        game = next((g for g in games if g['id'] == game_id), None)
        if not game:
            raise ValueError(f"Game {game_id} not found")
        return game

    def delete_game(self, game_id: str) -> bool:
        """
        Deletes a game by ID
        Returns True if game was deleted, False if game wasn't found
        """
        try:
            games = self._load_games()
            
            # Find the game to delete
            initial_count = len(games)
            games = [game for game in games if game['id'] != game_id]
            
            if len(games) == initial_count:
                logger.info(f"Game {game_id} not found")
                return False
                
            # Save updated games list
            self._save_games(games)
            logger.info(f"Successfully deleted game {game_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting game {game_id}: {e}")
            raise

    def get_all_games(self) -> List[Dict]:
        """Returns all games sorted by creation date descending"""
        try:
            games = self._load_games()
            return sorted(games, key=lambda x: x['created_at'], reverse=True)
        except Exception as e:
            logger.error(f"Error getting games: {e}")
            raise