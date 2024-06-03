from fonctionscommunes import *

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


def score_gopher(state: State, tour: Player) -> Score:
    if final_gopher(state, tour):
        if tour == 1:  # joueur1 a perdu
            return -1
        else:  # joueur1 a gagné
            return 1


def play_gopher(state: State, action: ActionGopher, tour: Player) -> State:
    if action not in legals_gopher(state, tour):
        print("erreur: action non légale")
        return state
    else:
        grid = state_to_environnement(state)
        grid[action] = tour
    return environnement_to_state(grid)


def evaluation_state_gopher(state: State, tour: Player) -> Score:
    """fonction d'évaluation de l'état d'un jeu DODO"""
    nb_legals_player: int = len(legals_gopher(state, tour)) - 1
    nb_legals_adversaire: int = len(legals_gopher(state, adversaire(tour)))
    if nb_legals_player == 0:
        return -1
    elif nb_legals_adversaire == 0:
        return 1
    else:
        diff_int = nb_legals_player - nb_legals_adversaire
        return -diff_int / (nb_legals_player + nb_legals_adversaire)


def alphabeta_gopher(state: State, tour: Player, alpha: float = -1000, beta: float = 1000) -> Score:
    """ alphabeta pour le jeu dodo pour un depth illimité"""
    if final_gopher(state, tour):
        return score_gopher(state, tour)
    if tour == maximizing_player:
        value = -10000
        for action in legals_gopher(state, maximizing_player):
            value = max(value,
                        alphabeta_gopher(play_gopher(state, action, maximizing_player), minimizing_player, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 10000
        for action in legals_gopher(state, minimizing_player):
            value = min(value,
                        alphabeta_gopher(play_gopher(state, action, minimizing_player), maximizing_player, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def alphabeta_gopher_depth(state: State, tour: Player, depth: int, alpha: float, beta: float) -> Score:
    """ alphabeta pour le jeu dodo pour un depth limité"""
    if final_gopher(state, tour):
        return score_gopher(state, tour)
    elif depth == 0:
        return evaluation_state_gopher(state, tour)
    else:
        if maximizing_player:
            value = -10000
            for action in legals_gopher(state, maximizing_player):
                value = max(value,
                            alphabeta_gopher_depth(play_gopher(state, action, maximizing_player), minimizing_player,
                                                   depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:  # minimizing player
            value = 10000
            for action in legals_gopher(state, minimizing_player):
                value = min(value,
                            alphabeta_gopher_depth(play_gopher(state, action, minimizing_player), maximizing_player,
                                                   depth - 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value


@memoize
def alphabeta_action_gopher(state: State, tour: Player, alpha=-100, beta=100) -> tuple[Score, ActionGopher]:
    """alphabeta avec action avec depth illimité"""
    if final_gopher(state, tour):
        return score_gopher(state, tour), (4, 4)
    if tour == maximizing_player:
        best_action: ActionGopher = legals_gopher(state, tour)[0]
        best_score: Score = -10000
        for action in legals_gopher(state, tour):
            bla = alphabeta_gopher(play_gopher(state, action, tour), minimizing_player, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: ActionGopher = legals_gopher(state, tour)[0]
        best_score: Score = 10000
        for action in legals_gopher(state, tour):
            bla = alphabeta_gopher(play_gopher(state, action, tour), maximizing_player, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


@memoize
def alphabeta_action_gopher_depth(state: State, tour: Player, alpha=-100, beta=100) -> tuple[Score, ActionGopher]:
    """alphabeta avec action avec depth limité"""
    if final_gopher(state, tour):
        return score_gopher(state, tour), (4, 4)
    if tour == maximizing_player:
        best_action: ActionGopher = legals_gopher(state, tour)[0]
        best_score: float = -10000
        for action in legals_gopher(state, tour):
            bla = alphabeta_gopher_depth(play_gopher(state, action, tour), minimizing_player, 3, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: ActionGopher = legals_gopher(state, tour)[0]
        best_score: float = 10000
        for action in legals_gopher(state, tour):
            bla = alphabeta_gopher_depth(play_gopher(state, action, tour), maximizing_player, 3, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


def strategy_alphabeta_gopher(state: State, tour: Player) -> ActionGopher:
    best_score, best_action = alphabeta_action_gopher(state, tour)
    return best_action


def stategy_random_gopher(state: State, tour: Player) -> ActionGopher:
    legal_actions: list[ActionGopher] = legals_gopher(state, tour)
    return random.choice(legal_actions)


def gopher(strategy_X: Strategy, strategy_O: Strategy, size: int) -> Score:
    state: State = empty_state(size)
    print("----------------joueur1-----------------------")
    print()
    state = play_gopher(state, (0, 0), 1)
    pprint(state, size)
    while not final_gopher(state, 2):
        action_2: Action = strategy_X(state, 2)
        state = play_gopher(state, action_2, 2)
        print("----------------joueur2-----------------------")
        print()
        pprint(state, size)
        if not final_gopher(state, 1):
            action_2: Action = strategy_O(state, 1)
            state = play_gopher(state, action_2, 1)
            print("----------------joueur1-----------------------")
            print()
            pprint(state, size)
        else:
            return score_gopher(state, 1)
    return score_gopher(state, 2)
