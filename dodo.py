from common import*
from typing import Union, Callable

# Types de base utilisés par l'arbitre
Environment = ...  # Ensemble des données utiles (cache, état de jeu...) pour
# que votre IA puisse jouer (objet, dictionnaire, autre...)


Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell]  # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Score = int
Time = int
Taille = int

def initial_state_dodo() -> State:
    result: State = []
    # joueur 1
    for i in [-1, -2, -3]:
        for j in [-1, -2, -3]:
            cell: Cell = (i, j)
            result.append((cell, 1))
    for i in [-2, - 3]:
        result.append(((0, i), 1))
        result.append(((i, 0), 1))

    # joueur 2
    for i in [1, 2, 3]:
        for j in [1, 2, 3]:
            cell: Cell = (i, j)
            result.append((cell, 2))
    for i in [2, 3]:
        result.append(((0, i), 2))
        result.append(((i, 0), 2))

    # zone neutre

    for i in [1, -1]:
        result.append(((0, i), 0))
        result.append(((i, 0), 0))
    for i in [1, 2]:
        result.append(((-1, i), 0))
        result.append(((i, -1), 0))
    result.append(((-2, 1), 0))
    result.append(((1, -2), 0))

    # resultat
    return result

def voisins_Dodo(cellule_dodo: tuple[Cell, Player], grid: Environment) -> list[Cell]:
    result: list[Cell] = []
    cell_mutable = [cellule_dodo[0][0], cellule_dodo[0][1]]
    if cellule_dodo == 1:
        new_cell = (cell_mutable[0], cell_mutable[1] + 1)
        if new_cell in grid:
            result.append(new_cell)

        new_cell = (cell_mutable[0] + 1, cell_mutable[1])
        if new_cell in grid:
            result.append(new_cell)

        new_cell = (cell_mutable[0] + 1, cell_mutable[1] + 1)
        if new_cell in grid:
            print(new_cell)
            result.append(new_cell)
        return result

    else:
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


def voisins_libres_dodo(cellule_dodo: tuple[Cell, Player], grid: Environment) -> list[Cell]:
    voisins: list[Cell] = voisins_Dodo(cellule_dodo, grid)
    result: list[Cell] = []
    for cell in voisins:
        if grid(cell) == 0:
            result.append(cell)
    return result


def legals_dodo(state: State, tour: Player) -> list[ActionDodo]:
    result: list[ActionDodo] = []
    for cell in state:
        while cell[1] == tour:
            voisins = voisins_libres_dodo(cell, state_to_environnement(state))
            for voisin in voisins:
                result.append((cell[0], voisin))
    return result


def final_dodo(state: State, tour: Player) -> bool:
    return legals_dodo(state, tour) == 0


def score_dodo(state: State) -> int:
    if final_dodo(state, 1):
        return 1
    elif final_dodo(state, 2):
        return -1


def play_dodo(state: State, action: ActionDodo, tour: Player) -> State:
    if action not in legals_dodo(state, tour):
        print("erreur: action non légale")
        return state
    else:
        grid = state_to_environnement(state)
        grid[action[0]] = 0
        grid[action[1]] = tour
    return state
'''
def alphabeta(node: State, depth: int, a: float,
              b: float, maximizing_player: bool) -> float:
    if depth == 0 or node is a terminal node:
        return the heuristic value of node
    if maximizing_player:
        value = −∞
        for each child of node:
            value = max(value, alphabeta(child, depth − 1, α, β, False))
            α = max(α, value)
            if α ≥ β:
                break # β cut-off
        return value
    else: # minimizing player
        value = +∞
        for each child of node:
            value = min(value, alphabeta(child, depth − 1, α, β, True))
            β = min(β, value)
            if α ≥ β:
                break # α cut-off
        return value

'''
# stratégie alpha-beta
def alphabeta_dodo_joueur1(grid: State, player: Player, alpha: float = -1000, beta: float = 1000) -> float:
    if final_dodo(grid, player):
        return score_dodo(grid)
    if player == 1:
        value = -100
        for action in legals_dodo(grid, player):
            value = max(value, alphabeta_dodo_joueur1(play_dodo(grid, action, player), 2, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 100
        for action in legals_dodo(grid, player):
            value = min(value, alphabeta_dodo_joueur1(play_dodo(grid, action, player), 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def alphabeta_dodo_joueur2(grid: State, player: Player, alpha: float = -1000, beta: float = 1000) -> float:
    if final_dodo(grid, player):
        return score_dodo(grid)
    if player == 2:
        value = -100
        for action in legals_dodo(grid, player):
            value = max(value, alphabeta_dodo_joueur2(play_dodo(grid, action, player), 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 100
        for action in legals_dodo(grid, player):
            value = min(value, alphabeta_dodo_joueur2(play_dodo(grid, action, player), 2, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def alphabeta_action(grid: State, player: Player, alpha=-100, beta=100) -> tuple[float, Action]:
    """alphabeta avec action"""
    if final_dodo(grid, player):
        return score_dodo(grid), (3, 3)
    if player == 1:
        best_action: Action = legals_dodo(grid, player)[0]
        best_score: float = -2
        for action in legals_dodo(grid, player):
            bla = alphabeta_dodo(play_dodo(grid, action, player), 2, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: Action = legals_dodo(grid, player)[0]
        best_score: float = 2
        for action in legals_dodo(grid, player):
            bla = alphabeta_dodo(play_dodo(grid, action, player), 1, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


def strategy_alphabeta(grid: State, player: Player) -> Action:
    best_score, best_action = alphabeta_action(grid, player)
    return best_action


def code_unique_dodo():
    print()
