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
        self.archive_file = self.data_dir / "games_archive.json"
        self._initialize_data_stores()
    
    def _initialize_data_stores(self):
        """Initialize both active and archive game stores"""
        if not self.games_file.exists():
            with open(self.games_file, 'w') as f:
                json.dump([], f)
                
        if not self.archive_file.exists():
            with open(self.archive_file, 'w') as f:
                json.dump([], f)

    def _generate_game_id(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        games = self._load_games()
        archived = self._load_archive()
        suffix = 1
        
        # Check both active and archived games for ID uniqueness
        existing_ids = {game['id'] for game in games}
        existing_ids.update({game['id'] for game in archived})
        
        base_id = f"{timestamp}_{suffix}"
        while base_id in existing_ids:
            suffix += 1
            base_id = f"{timestamp}_{suffix}"
            
        return base_id

    def _load_games(self) -> List[Dict]:
        """Load active games"""
        try:
            with open(self.games_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Error reading games file, returning empty list")
            return []
        
    def _load_archive(self) -> List[Dict]:
        """Load archived games"""
        try:
            with open(self.archive_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Error reading archive file, returning empty list")
            return []

    def _save_games(self, games: List[Dict]):
        """Save active games"""
        with open(self.games_file, 'w') as f:
            json.dump(games, f, indent=2)
            
    def _save_archive(self, archived_games: List[Dict]):
        """Save archived games"""
        with open(self.archive_file, 'w') as f:
            json.dump(archived_games, f, indent=2)
    
    def create_game(self, game_name: str, creator: str) -> Dict:
        """Create a new game with the first player"""
        try:
            games = self._load_games()
            
            new_game = {
                'id': self._generate_game_id(),
                'name': game_name,
                'created_at': datetime.now().isoformat(),
                'status': 'draft',  # New games start as drafts
                'creator': creator,
                'players': [
                    {
                        'username': creator,
                        'slot': 0,
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
    
    def archive_game(self, game_id: str):
        """Move a game from active to archive"""
        try:
            # Load both stores
            games = self._load_games()
            archived = self._load_archive()
            
            # Find game to archive
            game = next((g for g in games if g['id'] == game_id), None)
            if not game:
                raise ValueError(f"Game {game_id} not found")
            
            # Update game status and add completion timestamp
            game['status'] = 'completed'
            game['completed_at'] = datetime.now().isoformat()
            
            # Remove from active games
            games = [g for g in games if g['id'] != game_id]
            
            # Add to archive
            archived.append(game)
            
            # Save both stores
            self._save_games(games)
            self._save_archive(archived)
            
        except Exception as e:
            logger.error(f"Error archiving game: {e}")
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
        """Get current state of a game (check both active and archive)"""
        # Check active games first
        games = self._load_games()
        game = next((g for g in games if g['id'] == game_id), None)
        
        if game:
            return game
            
        # If not found, check archive
        archived = self._load_archive()
        game = next((g for g in archived if g['id'] == game_id), None)
        
        if game:
            return game
            
        raise ValueError(f"Game {game_id} not found in active or archived games")

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
        """Returns all active games sorted by creation date descending"""
        try:
            games = self._load_games()
            return sorted(games, key=lambda x: x['created_at'], reverse=True)
        except Exception as e:
            logger.error(f"Error getting games: {e}")
            raise

    def get_archived_games(self) -> List[Dict]:
        """Returns all archived games sorted by completion date descending"""
        try:
            archived = self._load_archive()
            return sorted(archived, key=lambda x: x['completed_at'], reverse=True)
        except Exception as e:
            logger.error(f"Error getting archived games: {e}")
            raise


    def update_game_state(self, game_id: str, new_status: str) -> Dict:
        """
        Updates the game status
        Returns the updated game dictionary
        """
        try:
            games = self._load_games()
            
            # Find the game to update
            game = next((game for game in games if game['id'] == game_id), None)
            if not game:
                raise ValueError(f"Game {game_id} not found")
                
            # Update the status
            game['status'] = new_status
            
            # Save updated games list
            self._save_games(games)
            logger.info(f"Successfully updated game {game_id} status to {new_status}")
            return game
            
        except Exception as e:
            logger.error(f"Error updating game {game_id} status: {e}")
            raise