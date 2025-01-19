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
    
    def create_game(self, game_name: str) -> Dict:
        try:
            games = self._load_games()
            
            new_game = {
                'id': self._generate_game_id(),
                'name': game_name,
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            games.append(new_game)
            self._save_games(games)
            
            logger.info(f"Created new game: {new_game}")
            return new_game
            
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            raise
            
    def get_all_games(self) -> List[Dict]:
        """Returns all games sorted by creation date descending"""
        try:
            games = self._load_games()
            return sorted(games, key=lambda x: x['created_at'], reverse=True)
        except Exception as e:
            logger.error(f"Error getting games: {e}")
            raise

    def delete_game(self, game_id: str) -> bool:
        """
        Deletes a game by ID
        Returns True if game was deleted, False if game wasn't found
        Raises exception if error occurs during deletion
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