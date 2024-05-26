from typing import Union, Callable

# Types de base utilisés par l'arbitre


Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell]  # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Score = int
Time = int
Taille = int
Strategy = Callable[[State, Player], Action]
Environment = dict[Cell, Player]  # Ensemble des données utiles (cache, état de jeu...) pour

# que votre IA puisse jouer (objet, dictionnaire, autre...)


# Environment = dict{tuple(int, int): Player}

# fonctions communs à tt le monde
def initialize(game: str, state: State, player: Player, hex_size: int, total_time: Time) -> Environment:
    '''Cette fonction est lancée au début du jeu.
    Elle dit à quel jeu on joue, le joueur que l'on est et renvoie l'environnement '''
    maximizing_player: Player = player
    if player == 1:
        minimizing_player = 2
    else:
        minimizing_player = 1


def strategy(env: Environment, state: State, player: Player, time_left: Time) -> tuple[Environment, Action]:
    '''Cette fonction est la strategie qu'on utilise pour jouer.
    Cette fonction est lancée à chaque fois que c'est à notre joueur de jouer.'''
    print()


def final_result(state: State, score: Score, player: Player) -> tuple[Player, State, Score]:
    '''Cette fonction est appelée à la fin du jeu
    et renvoie le joueur gagnant, l'état final et le score'''
    print()


'''
TODO:

ISMAT
- fonction qui inverse la position par rapport au couleur
- fonction qui inverse la positions par rapport l'axe vertical
- une fonction qui gère le jeu (le tour des joueurs)
    Dodo(strategy_1, strategy_2) -> Score
    
    
//meme chose pr gopher
    - legals_gopher()
    - final_gopher()
    - score_gopher()
    - play_gopher()
    - alphabeta_gopher()

'''


# Nos fonctions à nous
def state_to_environnement(state: State) -> Environment:
    """gopher et dodo"""
    result: dict = {}
    for item in state:
        result[item[0]] = item[1]
    return result


def environnement_to_state(grid: Environment) -> State:
    """gopher et dodo"""
    result: State = []
    for key, value in grid.items():
        # print(key)
        # print(value)
        result.append((key, value))
    return result


def empty_state(n: Taille) -> State:
    """appliquable pour gopher"""
    result: State = []
    n = n - 1
    for i in range(-n, 1, 1):
        for j in range(-n, 1, 1):
            cell: Cell = (i, j)
            result.append((cell, 0))
    for i in range(0, n + 1, 1):
        for j in range(0, n + 1, 1):
            if i == j == 0:
                pass
            else:
                cell: Cell = (i, j)
                result.append((cell, 0))

    for i in range(2, n):
        result.append(((-1, i), 0))
        result.append(((i, -1), 0))
        result.append(((1, -i), 0))
        result.append(((-i, 1), 0))
    l = n // 2
    for i in range(1, l + 1):
        result.append(((-i, i), 0))
        result.append(((i, -i), 0))

    return result


'''
def voisins(cellule: Cell, grid: Environment) -> list[Cell]:
    """appliquable pour dodo et gopher"""
    result: list[Cell] = []
    cell_mutable = [cellule[0], cellule[1]]

    new_cell = (cell_mutable[0], cell_mutable[1] + 1)
    if new_cell in grid:
        result.append(new_cell)

    new_cell = (cell_mutable[0] + 1, cell_mutable[1])
    if new_cell in grid:
        result.append(new_cell)

    new_cell = (cell_mutable[0] + 1, cell_mutable[1] + 1)
    if new_cell in grid:
        result.append(new_cell)

    new_cell = (cell_mutable[0], cell_mutable[1] - 1)
    if new_cell in grid:
        result.append(new_cell)

    new_cell = (cell_mutable[0] - 1, cell_mutable[1])
    if new_cell in grid:
        result.append(new_cell)

    new_cell = (cell_mutable[0] - 1, cell_mutable[1] - 1)
    if new_cell in grid:
        result.append(new_cell)

    return result
'''

def voisins(cellule: Cell, grid: Environment) -> list[Cell]:
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


def pprint(state: State, size: int):
    """Pretty print the state of the hexagonal grid
    appliquable pour DODO et Gopher"""
    sorted_state = sorted(state, key=lambda x: x[0][1], reverse=True)
    real_size = size - 1
    j: int = 0

    for i in range(real_size, -real_size - 1, -1):
        if i > 0:
            print(i * "_ ", end="")
        while sorted_state[j][0][1] == i:
            print(sorted_state[j][1], end=" ")
            j += 1
            if j > len(sorted_state) - 1:
                break
        if i < 0:
            print(abs(i) * "_ ", end="")
        print("\n")


'''
TO REVIEW/TEST: 
    - hashage de zobrist: amen  //review
    - fonction de hashage: amen //review

TODO:
    AMEN
    - fonction d'évaluation: amen
    
    //on va probablement utiliser ces 2 fonctions avec une profondeur limitée
    -alphabeta_dodo
    -alpha_beta_action
    -strategy_alphabeta_dodo
    

    
    
'''

#seed, une valeur globale initialisé à une valeur random,
#qui permettra la generation de valaurs pseudo-aléatoires
seed: int = 12497846486


def generate_random_value() -> int:
    """une fonction qui génère un nombre pseudo-aléatoire"""
    a: int = 7690753721
    b: int = 9847572537
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
unique_values = state_keys(empty_state(4))


def hash_zobrist(state: State)-> int:
    """ retourne la valeur hashée du state
     cette valeur est à priori unique pour chaque state différent"""
    h = 0
    for item in state:
        if item[1] != 0:
            h ^= unique_values[item]
    return h


def memoize(
        f: Callable[[State, Player], tuple[Score, Action]]
) -> Callable[[State, Player], tuple[Score, Action]]:
    cache = {}  # closure

    def g(state: State, player: Player):
        hashed_value: int = hash_zobrist(state)
        if hashed_value in cache:
            return cache[hashed_value]
        val = f(state, player)
        cache[hashed_value] = val
        return val

    return g

def evaluation_state()->float:
    return 5

def main():
    '''
    state = empty_state()
    print(state)
    print()
    print(initial_state())
    print()
    test = [((1, 0), 0), ((1, 2), 0), ((1, 3), 0)]
    print(test)
    print()
    test2 = state_to_environnement(test)
    print(test2)
    print()
    print(environnement_to_state(test2))'''
    print(empty_state(4), len(empty_state(4)))
    global unique_values
    unique_values = state_keys(empty_state(4))


if __name__ == "__main__":
    main()
