from typing import Union, Callable, Tuple, Dict
import random
import csv
import atexit
import json


# Types de base utilisés par l'arbitre


Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell]  # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Score = float
Time = int
Taille = int
Strategy = Callable[[State, Player], Action]
Grid = dict[tuple[int, int], int]
Environment = Union[Dict[int, Tuple[Score, ActionDodo]], Dict[int, Tuple[Score, ActionGopher]]]
maximizing_player: Player
minimizing_player: Player


# Nos fonctions à nous
def state_to_environnement(state: State) -> Grid:
    """gopher et dodo"""
    result: dict = {}
    for item in state:
        result[item[0]] = item[1]
    return result


def environnement_to_state(grid: Grid) -> State:
    """gopher et dodo"""
    result: State = []
    for key, value in grid.items():
        # print(key)
        # print(value)
        result.append((key, value))
    return result


def adversaire(player: Player) -> Player:
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else:
        return 0


def voisins(cellule: Cell, grid: Grid) -> list[Cell]:
    """Applicable for dodo and gopher."""
    result: list[Cell] = []
    x, y = cellule

    # Define the six possible neighbors based on your function's logic
    neighbors = [
        (x, y + 1),
        (x + 1, y),
        (x + 1, y + 1),
        (x, y - 1),
        (x - 1, y),
        (x - 1, y - 1)
    ]

    # Check if each neighbor is within the grid and add to the result
    for new_cell in neighbors:
        if new_cell in grid:
            result.append(new_cell)

    return result


def empty_state(size: int) -> State:
    result: State = []
    size = size - 1  # Adjust size to match the grid indexing

    # Initialize the grid with valid cells only
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            if -size <= i + j <= size:
                cell: Cell = (i, j)
                result.append((cell, 0))

    # Sort the result for consistency (optional)
    result = sorted(result, key=lambda x: (-x[0][1], x[0][0]))

    return result


def pprint(state: State, size: int):
    """Pretty print the state of the hexagonal grid
    appliquable pour DODO et Gopher"""
    sorted_state = sorted(state, key=lambda x: (-x[0][1], x[0][0]))
    real_size = size - 1
    j: int = 0

    for i in range(real_size, -real_size - 1, -1):
        if i > 0:
            print(i * "_ ", end="")
        while sorted_state[j][0][1] == i:
            #print(sorted_state[j][0], sorted_state[j][1], end=" ")
            print(sorted_state[j][1], end=" ")

            j += 1
            if j > len(sorted_state) - 1:
                break
        if i < 0:
            print(abs(i) * "_ ", end="")
        print("\n")



# seed, une valeur globale initialisé à une valeur random,
# qui permettra la generation de valaurs pseudo-aléatoires
seed: int = 2847572934


def generate_random_value() -> int:
    """une fonction qui génère un nombre pseudo-aléatoire"""
    a: int = 1535820267
    b: int = 3892683005
    global seed
    seed = (a * seed + b) % (2 ** 32)
    return seed


def state_keys(state: State):
    """une fonction qui donne à chaque combinaison (Cellule, Player) possible,
    une valeur unique, qu'on peut utiliser pour le hashage  """
    res: dict[tuple[Cell, Player], int] = {}
    for item in state:
        res[(item[0], 1)] = generate_random_value()
        res[(item[0], 2)] = generate_random_value()
    return res


# un dictionnaire contenant la valeur unique de chaque Combinaison (Cellule, Player) possible
UNIQUE_VALUES = state_keys(empty_state(8))


def hash_zobrist(state: State) -> int:
    """ retourne la valeur hashée du state
     cette valeur est à priori unique pour chaque state différent"""
    h = 0
    for item in state:
        if item[1] != 0:
            h ^= UNIQUE_VALUES[item]
    return h


def inverse_vertical_axis(state: State):
    grid = state_to_environnement(state)
    for cellule, valeur in grid.items():
        q, r = cellule
        if abs(q) != abs(r):
            cellule = grid[(q, r)]
            grid[(q, r)] = grid[(r, q)]
            grid[(r, q)] = cellule
    return environnement_to_state(grid)


def inverse_colors(state: State):
    grid = state_to_environnement(state)
    for cellule, valeur in grid.items():
        if valeur == 1:
            grid[cellule] = 2
        if valeur == 2:
            grid[cellule] = 1
    return environnement_to_state(grid)


def symetrie_origine(cellule: Cell):
    q, r = cellule
    return -q, -r


def inverser_positions_par_symetrie_origine(state: State) -> State:
    nouvelles_positions = {}
    grid = state_to_environnement(state)
    for (coord, couleur) in grid.items():
        coord_sym: Cell = symetrie_origine(coord)
        nouvelles_positions[coord_sym] = couleur
    return environnement_to_state(nouvelles_positions)


def generate_symmetric_states(state: State) -> [State]:
    return [state,
            inverse_vertical_axis(state),
            inverse_colors(state),
            inverser_positions_par_symetrie_origine(state)]


# Function to save cache to a file
def save_cache_to_file(cache: Dict[int, Tuple[Score, Action]], filename: str)->None:
    existing_cache = load_cache_from_file(filename)
    existing_cache.update(cache)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in existing_cache.items():
            writer.writerow([key, value[0], json.dumps(value[1])])


# Function to load cache from a file
def load_cache_from_file(filename: str) -> Dict[int, Tuple[Score, Action]]:
    cache = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                key = int(row[0])
                score = float(row[1])
                action = json.loads(row[2])  # Use JSON to parse the action
                if isinstance(action[0], list):
                    action = tuple(tuple(x) for x in action)  # Convert to tuple of tuples if needed
                cache[key] = (score, action)
    except FileNotFoundError:
        pass
    #print("cache loaded")
    return cache



