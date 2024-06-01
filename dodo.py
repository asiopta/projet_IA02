from fonctionscommunes import *


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
        if grid[cell] == 0:
            result.append(cell)
    return result


def legals_dodo(state: State, tour: Player) -> list[ActionDodo]:
    result: list[ActionDodo] = []
    grid: Environment = state_to_environnement(state)
    for cell in state:
        while cell[1] == tour:
            voisins = voisins_libres_dodo(cell, grid)
            for voisin in voisins:
                result.append((cell[0], voisin))
    return result


def final_dodo(state: State, tour: Player) -> bool:
    return legals_dodo(state, tour) == 0


def score_dodo(state: State, tour: Player) -> int:
    if final_dodo(state, tour):
        if tour == 1:
            return 1
        else:
            return -1


def play_dodo(state: State, action: ActionDodo, tour: Player) -> State:
    if action not in legals_dodo(state, tour):
        print("erreur: action non légale")
        return state
    else:
        grid = state_to_environnement(state)
        grid[action[0]] = 0
        grid[action[1]] = tour
    return environnement_to_state(grid)


def evaluation_state_dodo(state: State, tour: Player) -> float:  # à faire
    """fonction d'évaluation de l'état d'un jeu DODO"""
    nb_legals_player: int = len(legals_dodo(state, tour)) - 1
    nb_legals_adversaire: int = len(legals_dodo(state, adversaire(tour)))
    if nb_legals_player == 0:
        return 1
    elif nb_legals_adversaire == 0:
        return -1
    else:
        diff_int = nb_legals_player - nb_legals_adversaire
        return diff_int / 100


# stratégie alpha-beta
def alphabeta_dodo(state: State, tour: Player, alpha: float = -1000, beta: float = 1000) -> float:
    """ alphabeta pour le jeu dodo pour un depth illimité"""
    if final_dodo(state, tour):
        return score_dodo(state, tour)
    if tour == maximizing_player:
        value = -10000
        for action in legals_dodo(state, maximizing_player):
            value = max(value,
                        alphabeta_dodo(play_dodo(state, action, maximizing_player), minimizing_player, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 10000
        for action in legals_dodo(state, minimizing_player):
            value = min(value,
                        alphabeta_dodo(play_dodo(state, action, minimizing_player), maximizing_player, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def alphabeta_dodo_depth(state: State, tour: Player, depth: int, alpha: float, beta: float) -> float:
    """ alphabeta pour le jeu dodo pour un depth limité"""
    if final_dodo(state, tour):
        return score_dodo(state, tour)
    elif depth == 0:
        return evaluation_state_dodo(state, tour)
    else:
        if maximizing_player:
            value = -10000
            for action in legals_dodo(state, maximizing_player):
                value = max(value, alphabeta_dodo_depth(play_dodo(state, action, maximizing_player), minimizing_player,
                                                        depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:  # minimizing player
            value = 10000
            for action in legals_dodo(state, minimizing_player):
                value = min(value, alphabeta_dodo_depth(play_dodo(state, action, minimizing_player), maximizing_player,
                                                        depth - 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value


@memoize
def alphabeta_action_dodo(state: State, tour: Player, alpha=-100, beta=100) -> tuple[float, ActionDodo]:
    """alphabeta avec action avec depth illimité"""
    if final_dodo(state, tour):
        return score_dodo(state, tour), ((4, 4), (4, 4))
    if tour == maximizing_player:
        best_action: Action = legals_dodo(state, tour)[0]
        best_score: float = -10000
        for action in legals_dodo(state, tour):
            bla = alphabeta_dodo(play_dodo(state, action, tour), minimizing_player, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: Action = legals_dodo(state, tour)[0]
        best_score: float = 10000
        for action in legals_dodo(state, tour):
            bla = alphabeta_dodo(play_dodo(state, action, tour), maximizing_player, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


@memoize
def alphabeta_action_dodo_depth(state: State, tour: Player, alpha=-100, beta=100) -> tuple[float, ActionDodo]:
    """alphabeta avec action avec depth limité"""
    if final_dodo(state, tour):
        return score_dodo(state, tour), (4, 4)
    if tour == maximizing_player:
        best_action: Action = legals_dodo(state, tour)[0]
        best_score: float = -10000
        for action in legals_dodo(state, tour):
            bla = alphabeta_dodo_depth(play_dodo(state, action, tour), minimizing_player, 10, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: Action = legals_dodo(state, tour)[0]
        best_score: float = 10000
        for action in legals_dodo(state, tour):
            bla = alphabeta_dodo_depth(play_dodo(state, action, tour), maximizing_player, 10, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


def strategy_alphabeta_dodo(state: State, tour: Player) -> ActionDodo:
    best_score, best_action = alphabeta_action_dodo(state, tour)
    return best_action

def strategy_random_dodo(state: State, tour: Player) -> ActionDodo:
    legal_actions: list[ActionDodo] = legals_dodo(state, tour)
    return random.choice(legal_actions)


# boucle de jeu
def dodo(strategy_X: Strategy, strategy_O: Strategy) -> Score:
    state: State = initial_state_dodo()
    while not final_dodo(state, 1):
        action_1: Action = strategy_X(state, 1)
        state = play_dodo(state, action_1, 1)
        pprint(state, 4)
        if not final_dodo(state, 2):
            action_2: Action = strategy_O(state, 2)
            state = play_dodo(state, action_2, 2)
            pprint(state, 4)
        else:
            return score_dodo(state, 2)
    return score_dodo(state, 1)
