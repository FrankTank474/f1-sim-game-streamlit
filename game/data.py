from .models import Driver, Team, Track

# Initialize all teams with initial performance and budget
TEAMS = [
    Team("Red Bull Racing", 95, 150000000),
    Team("Mercedes", 92, 150000000),
    Team("Ferrari", 90, 150000000),
    Team("McLaren", 88, 130000000),
    Team("Aston Martin", 85, 120000000),
    Team("Alpine", 83, 110000000),
    Team("Williams", 80, 100000000),
    Team("Visa Cash App RB", 79, 95000000),
    Team("Kick Sauber", 78, 90000000),
    Team("Haas F1", 77, 85000000)
]

# Initialize all available drivers
DRIVERS = [
    Driver("Lewis Hamilton", 95, 90, 50000000),
    Driver("Max Verstappen", 96, 88, 55000000),
    Driver("Charles Leclerc", 92, 85, 40000000),
    Driver("Lando Norris", 93, 89, 35000000),
    Driver("George Russell", 89, 86, 35000000),
    Driver("Carlos Sainz", 87, 84, 30000000),
    Driver("Fernando Alonso", 90, 88, 25000000),
    Driver("Oscar Piastri", 87, 85, 20000000),
    Driver("Alex Albon", 84, 83, 15000000),
    Driver("Valtteri Bottas", 86, 85, 15000000),
    Driver("Pierre Gasly", 83, 82, 12000000),
    Driver("Kevin Magnussen", 82, 80, 10000000),
    Driver("Yuki Tsunoda", 81, 79, 10000000),
    Driver("Logan Sargeant", 79, 78, 8000000),
    Driver("Zhou Guanyu", 80, 79, 8000000),
    Driver("Daniel Ricciardo", 84, 83, 15000000),
    Driver("Esteban Ocon", 83, 82, 12000000),
    Driver("Nico Hulkenberg", 82, 81, 10000000),
    Driver("Lance Stroll", 81, 80, 10000000),
    Driver("Sergio Perez", 88, 85, 35000000)
]

# Initialize all tracks with their characteristics
TRACKS = [
    Track("Bahrain GP", 75, 60, 70),
    Track("Saudi Arabian GP", 85, 50, 75),
    Track("Australian GP", 70, 65, 65),
    Track("Japanese GP", 80, 70, 60),
    Track("Chinese GP", 75, 75, 70),
    Track("Miami GP", 70, 60, 65),
    Track("Emilia Romagna GP", 80, 80, 75),
    Track("Monaco GP", 95, 85, 95),
    Track("Canadian GP", 75, 75, 70),
    Track("Spanish GP", 70, 65, 75),
    Track("Austrian GP", 75, 70, 65),
    Track("British GP", 85, 80, 70),
    Track("Hungarian GP", 80, 60, 85),
    Track("Belgian GP", 85, 85, 70),
    Track("Dutch GP", 80, 75, 80),
    Track("Italian GP", 75, 60, 60),
    Track("Singapore GP", 90, 80, 85),
    Track("United States GP", 75, 65, 70),
    Track("Mexican GP", 80, 55, 75),
    Track("Brazilian GP", 80, 80, 70),
    Track("Las Vegas GP", 85, 60, 75),
    Track("Abu Dhabi GP", 75, 55, 70)
]

# Helper function to get current driver assignments
def get_default_driver_assignments() -> dict:
    return {
        "Red Bull Racing": ["Max Verstappen", "Sergio Perez"],
        "Mercedes": ["Lewis Hamilton", "George Russell"],
        "Ferrari": ["Charles Leclerc", "Carlos Sainz"],
        "McLaren": ["Lando Norris", "Oscar Piastri"],
        "Aston Martin": ["Fernando Alonso", "Lance Stroll"],
        "Alpine": ["Pierre Gasly", "Esteban Ocon"],
        "Williams": ["Alex Albon", "Logan Sargeant"],
        "Visa Cash App RB": ["Daniel Ricciardo", "Yuki Tsunoda"],
        "Kick Sauber": ["Valtteri Bottas", "Zhou Guanyu"],
        "Haas F1": ["Nico Hulkenberg", "Kevin Magnussen"]
    }

def initialize_season():
    """Initialize teams with their default drivers"""
    # Create a driver lookup by name
    driver_lookup = {driver.name: driver for driver in DRIVERS}
    
    # Get default assignments
    assignments = get_default_driver_assignments()
    
    # Assign drivers to teams
    for team in TEAMS:
        if team.name in assignments:
            for driver_name in assignments[team.name]:
                driver = driver_lookup[driver_name]
                driver.team = team
                team.drivers.append(driver)
    
    return TEAMS, DRIVERS, TRACKS