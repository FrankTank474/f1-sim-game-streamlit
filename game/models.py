from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Driver:
    name: str
    skill: int  # 1-100
    consistency: int  # 1-100
    price: int
    points: int = 0
    crashes: int = 0
    team: Optional['Team'] = None

    def __repr__(self) -> str:
        return f"Driver(name={self.name}, skill={self.skill}, consistency={self.consistency})"

@dataclass
class Team:
    name: str
    car_performance: int  # 1-100
    budget: int
    drivers: List[Driver] = field(default_factory=list)
    points: int = 0
    prize_money: int = 0

    def __repr__(self) -> str:
        return f"Team(name={self.name}, car_performance={self.car_performance}, drivers={len(self.drivers)})"

@dataclass
class Track:
    name: str
    difficulty: int  # 1-100
    weather_impact: int  # 1-100
    overtaking_difficulty: int  # 1-100

    def __repr__(self) -> str:
        return f"Track(name={self.name})"