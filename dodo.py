from common import *
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


def evaluation_state_dodo(state: State) -> float:  # à faire
    """fonction d'évaluation de l'état d'un jeu DODO"""
    res: int = 0
    return res


# stratégie alpha-beta
def alphabeta_dodo(grid: State, tour: Player, alpha: float = -1000, beta: float = 1000) -> float:
    """ alphabeta pour le jeu dodo pour un depth illimité"""
    if final_dodo(grid, tour):
        return score_dodo(grid)
    if tour == maximizing_player:
        value = -10000
        for action in legals_dodo(grid, maximizing_player):
            value = max(value,
                        alphabeta_dodo(play_dodo(grid, action, maximizing_player), minimizing_player, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 10000
        for action in legals_dodo(grid, minimizing_player):
            value = min(value,
                        alphabeta_dodo(play_dodo(grid, action, minimizing_player), maximizing_player, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def alphabeta_dodo_depth(grid: State, tour: Player, depth: int, alpha: float, beta: float) -> float:
    """ alphabeta pour le jeu dodo pour un depth limité"""
    if final_dodo(grid, tour):
        return score_dodo(grid)
    elif depth == 0:
        return evaluation_state_dodo(grid)
    else:
        if maximizing_player:
            value = -10000
            for action in legals_dodo(grid, maximizing_player):
                value = max(value, alphabeta_dodo_depth(play_dodo(grid, action, maximizing_player), minimizing_player,
                                                        depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:  # minimizing player
            value = 10000
            for action in legals_dodo(grid, minimizing_player):
                value = min(value, alphabeta_dodo_depth(play_dodo(grid, action, minimizing_player), maximizing_player,
                                                        depth - 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value


def alphabeta_action_dodo(grid: State, tour: Player, alpha=-100, beta=100) -> tuple[float, Action]:
    """alphabeta avec action avec depth illimité"""
    if final_dodo(grid, tour):
        return score_dodo(grid), (3, 3)
    if tour == maximizing_player:
        best_action: Action = legals_dodo(grid, tour)[0]
        best_score: float = -10000
        for action in legals_dodo(grid, tour):
            bla = alphabeta_dodo(play_dodo(grid, action, tour), minimizing_player, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: Action = legals_dodo(grid, tour)[0]
        best_score: float = 10000
        for action in legals_dodo(grid, tour):
            bla = alphabeta_dodo(play_dodo(grid, action, tour), maximizing_player, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


def alphabeta_action_dodo_depth(grid: State, tour: Player, alpha=-100, beta=100) -> tuple[float, Action]:
    """alphabeta avec action avec depth limité"""
    if final_dodo(grid, tour):
        return score_dodo(grid), (3, 3)
    if tour == maximizing_player:
        best_action: Action = legals_dodo(grid, tour)[0]
        best_score: float = -10000
        for action in legals_dodo(grid, tour):
            bla = alphabeta_dodo_depth(play_dodo(grid, action, tour), minimizing_player, 10, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: Action = legals_dodo(grid, tour)[0]
        best_score: float = 10000
        for action in legals_dodo(grid, tour):
            bla = alphabeta_dodo_depth(play_dodo(grid, action, tour), maximizing_player, 10, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


def strategy_alphabeta_dodo(grid: State, tour: Player) -> Action:
    best_score, best_action = alphabeta_action_dodo(grid, tour)
    return best_action
