from common import *

"""
    begins the game by placing a stone anywhere on the board. Then, starting
with Blue, players take turns placing a stone which forms exactly one enemy
connection and no friendly connections.

The last player to place a stone wins
"""


def forms_friendly_connection(tour: Player, cellule_gopher: Cell, grid: Environment) -> bool:
    """checks if playing in a given cell, forms a friendly connection"""
    for cell in voisins(cellule_gopher, grid):
        if grid[cell] == tour:
            return True
    return False


def forms_enemy_connection(tour: Player, cellule_gopher: Cell, grid: Environment) -> int:
    """checks if playing in a given cell, how many enemy connections that moves creates"""
    adv: Player = adversaire(tour)
    var: int = 0
    for cell in voisins(cellule_gopher, grid):
        if grid[cell] == adv:
            var += 1
    return var


def to_discard(tour: Player, cellule_gopher: Cell, grid: Environment) -> bool:
    """checks if it's a friendly cell or an enemy cell that already has an enemy connection
    if that's true, we discard it, no need to check if we can play around it or not"""
    if grid[cellule_gopher] == tour:  # it's a friendly cell
        return True
    else:  # grid[cellule_gopher_adv] == adversaire(tour) // it's an enemy cell
        for cell in voisins(cellule_gopher, grid):
            if grid[cell] == tour:
                return True
    return False


def voisins_libres_gopher(cellule_gopher_jouable: Cell, tour: Player, grid: Environment) -> list[Cell]:
    """
    takes a non discarded cell as input, regarde ses voisins
    parmi les voisins du cellule, elle retourne les cellules où on peut jouer
    """
    result: list[Cell] = []
    for cell in voisins(cellule_gopher_jouable, grid):
        if (not (forms_friendly_connection(tour, cellule_gopher_jouable, grid))
                and (forms_enemy_connection(tour, cellule_gopher_jouable, grid) == 1)):
            result.append(cell)
    return result


def legals_gopher(state: State, tour: Player) -> list[ActionGopher]:
    res: list[ActionGopher] = []
    grid: Environment = state_to_environnement(state)
    for cell in grid:
        if not (to_discard(tour, cell, grid)):
            res += voisins_libres_gopher(cell, tour, grid)

    return res


def final_gopher(state: State, tour: Player) -> bool:
    res: list[ActionGopher] = legals_gopher(state, tour)
    if len(res) == 0:
        return True
    return False

def score_gopher(state: State, tour:Player) -> Score:
    if final_gopher(state, tour):
        if tour == 1:  #joueur1 a perdu
            return -1
        else: #joueur1 a gagné
            return 1


def play_gopher(state: State, action: ActionGopher, tour: Player) -> State:
    if action not in legals_gopher(state, tour):
        print("erreur: action non légale")
        return state
    else:
        grid = state_to_environnement(state)
        grid[action] = tour
    return environnement_to_state(grid)
