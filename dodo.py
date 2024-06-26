from fonctionscommunes import *
import math


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

    result.append(((0, 0), 0))
    # resultat
    result = sorted(result, key=lambda x: x[0][0] + x[0][1], reverse=True)
    return result


# print(initial_state_dodo())

def voisins_Dodo(cellule_dodo: tuple[Cell, Player], grid: Grid) -> list[Cell]:
    result: list[Cell] = []
    cell = cellule_dodo[0]

    if cellule_dodo[1] == 1:
        #  print("HELLO")
        new_cells = [
            (cell[0], cell[1] + 1),  # haut a gauche
            (cell[0] + 1, cell[1]),  # Haut a droite
            (cell[0] + 1, cell[1] + 1)  # directement au dessus
        ]
    else:
        new_cells = [
            (cell[0], cell[1] - 1),  # en bas a gauche
            (cell[0] - 1, cell[1]),  # en bas a droite
            (cell[0] - 1, cell[1] - 1)  # directement au dessous
        ]

    #  print(new_cells)
    for new_cell in new_cells:

        # print(new_cell)
        #  print(grid)
        for cellplayer in grid:
            # print("okay")
            if new_cell == cellplayer:
                result.append(new_cell)
    # print(result)
    return result


# print(initial_state_dodo())
# rint(state_to_environnement(initial_state_dodo()))

# rint(voisins_Dodo(((1,0),2),state_to_environnement(initial_state_dodo())))

def voisins_libres_dodo(cellule_dodo: tuple[Cell, Player], grid: Grid) -> list[Cell]:
    voisins = voisins_Dodo(cellule_dodo, grid)
    result: list[Cell] = []
    for cell in voisins:
        if grid[cell] == 0:
            result.append(cell)
    return result


def legals_dodo(state: State, tour: Player) -> list[ActionDodo]:
    result: list[ActionDodo] = []
    grid: Grid = state_to_environnement(state)

    # Lescellules appartenant au joueur
    player_cells = [cell for cell in state if cell[1] == tour]
    for cell in player_cells:
        voisins = voisins_libres_dodo(cell, grid)
        for voisin in voisins:
            result.append((cell[0], voisin))

    return result


def final_dodo(state: State, tour: Player) -> bool:
    return legals_dodo(state, tour) == []


def score_dodo(state: State, tour: Player) -> Score:
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


'''
def evaluation_state_dodo(state: State, tour: Player) -> Score:
    """fonction d'évaluation de l'état d'un jeu DODO"""
    nb_legals_player: int = len(legals_dodo(state, tour)) - 1
    nb_legals_adversaire: int = len(legals_dodo(state, adversaire(tour)))
    if nb_legals_player <= 0:
        return 1
    elif nb_legals_adversaire <= 0:
        return -1
    else:
        diff_int = nb_legals_adversaire - nb_legals_player

        return diff_int / (nb_legals_adversaire + nb_legals_player)

'''


def centrality_score(cell: Cell) -> float:
    center = (0, 0)
    distance = abs(cell[0] - center[0]) + abs(cell[1] - center[1])
    return max(0, 6 - distance)  # The farther from the center, the lower the score


def evaluation_state_dodo(state: State, tour: Player) -> Score:
    """Improved evaluation function for Dodo game state."""

    nb_legals_player = len(legals_dodo(state, tour))
    nb_legals_adversaire = len(legals_dodo(state, adversaire(tour)))

    if nb_legals_player == 0:
        return float('-inf')  # Loss for the current player
    if nb_legals_adversaire == 0:
        return float('inf')  # Win for the current player

    # Mobility factor
    mobility_score = nb_legals_player - nb_legals_adversaire

    # Centrality factor
    centrality_player = sum(centrality_score(cell) for cell, p in state if p == tour)
    centrality_adversaire = sum(centrality_score(cell) for cell, p in state if p == adversaire(tour))
    centrality_diff = centrality_player - centrality_adversaire

    # Blocking potential
    blocking_score = 0
    for cell, p in state:
        if p == tour:
            blocking_score += sum(1 for move in legals_dodo(state, adversaire(tour)) if move[1] == cell)

    # Combine factors with appropriate weights
    return (0.6 * mobility_score) + (0.2 * centrality_diff) + (0.2 * blocking_score)


# stratégie alpha-beta
def alphabeta_dodo(state: State, tour: Player, alpha: float = -1000, beta: float = 1000) -> Score:
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


def alphabeta_dodo_depth(state: State, tour: Player, depth: int, alpha: float, beta: float) -> Score:
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


maximizing_player: Player = 1
minimizing_player: Player = 2


# Memoize function for Dodo
def memoize_dodo(f: Callable[[State, Player, int], Tuple[Score, ActionDodo]], cache_file: str = 'cachedodo2.csv') -> \
        Callable[[State, Player, int], Tuple[Score, ActionDodo]]:
    cache: Dict[int, Tuple[Score, ActionDodo]] = load_cache_from_file(cache_file)  # Load cache from file

    def g(state: State, player: Player, depth: int) -> Tuple[Score, ActionDodo]:
        symmetric_states = generate_symmetric_states(state)
        hashed_values = [hash_zobrist(sym_state) for sym_state in symmetric_states]

        for hashed_value in hashed_values:
            if hashed_value in cache:
                return cache[hashed_value]

        val = f(state, player, depth)
        for hashed_value in hashed_values:
            cache[hashed_value] = val

        return val

    # Register the cache saving function to be called on program exit
    atexit.register(save_cache_to_file, cache, cache_file)

    return g


@memoize_dodo
def alphabeta_action_dodo(state: State, tour: Player, alpha=-100, beta=100) -> tuple[Score, ActionDodo]:
    """alphabeta avec action avec depth illimité"""
    if final_dodo(state, tour):
        return score_dodo(state, tour), ((4, 4), (4, 4))
    if tour == maximizing_player:
        best_action: Action = legals_dodo(state, tour)[0]
        best_score: Score = -10000
        for action in legals_dodo(state, tour):
            bla = alphabeta_dodo(play_dodo(state, action, tour), minimizing_player, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        best_action: Action = legals_dodo(state, tour)[0]
        best_score: Score = 10000
        for action in legals_dodo(state, tour):
            bla = alphabeta_dodo(play_dodo(state, action, tour), maximizing_player, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


@memoize_dodo
def alphabeta_action_dodo_depth(state: State, tour: Player, depth, alpha=-100, beta=100) -> tuple[Score, ActionDodo]:
    """alphabeta avec action avec depth limité"""
    if final_dodo(state, tour):
        return score_dodo(state, tour), ((4, 4), (4, 4))
    if tour == maximizing_player:
        actions_legales: list[ActionDodo] = legals_dodo(state, tour)
        best_action: Action = actions_legales[0]
        best_score: Score = -10000
        for action in actions_legales:
            bla = alphabeta_dodo_depth(play_dodo(state, action, tour), minimizing_player, depth, alpha, beta)
            if bla > best_score:
                best_score = bla
                best_action = action
    else:
        actions_legales: list[ActionDodo] = legals_dodo(state, tour)
        best_action: Action = actions_legales[0]
        best_score: Score = 10000
        for action in actions_legales:
            bla = alphabeta_dodo_depth(play_dodo(state, action, tour), maximizing_player, depth, alpha, beta)
            if bla < best_score:
                best_score = bla
                best_action = action

    return best_score, best_action


def strategy_alphabeta_dodo(state: State, tour: Player, time_left: int, total_time: int, size: int) -> ActionDodo:
    if size <= 4 and (time_left > (95 * total_time) / 100 or time_left < 45):
        best_score, best_action = alphabeta_action_dodo_depth(state, tour, 2)
    elif size >= 6 and (time_left > (70 * total_time) / 100 or time_left < 45):
        best_score, best_action = alphabeta_action_dodo_depth(state, tour, 2)
    elif time_left > (40 * total_time):
        best_score, best_action = alphabeta_action_dodo_depth(state, tour, 4)
    else:
        best_score, best_action = alphabeta_action_dodo_depth(state, tour, 3)
    return best_action


def strategy_random_dodo(state: State, tour: Player) -> ActionDodo:
    legal_actions: list[ActionDodo] = legals_dodo(state, tour)
    return random.choice(legal_actions)


def MCTS(state: State, player: Player, iterations: int) -> ActionDodo:
    """Monte Carlo Tree Search for Dodo game."""

    class Node:
        def __init__(self, state: State, parent=None):
            self.state = state
            self.parent = parent
            self.children = []
            self.visits = 0
            self.wins = 0
            self.untried_actions = legals_dodo(state, player)

        def add_child(self, child_state: State, action: ActionDodo):
            child_node = Node(child_state, parent=self)
            self.children.append((child_node, action))
            return child_node

        def update(self, result):
            self.visits += 1
            self.wins += result

    def uct_select(node: Node):
        """Select a child node based on UCT (Upper Confidence Bound for Trees)."""
        log_parent_visits = math.log(node.visits)
        return max(node.children,
                   key=lambda n: (n[0].wins / n[0].visits) + math.sqrt(2 * log_parent_visits / n[0].visits))

    def rollout(state: State, player: Player):
        """Simulate a random game from the current state."""
        while not final_dodo(state, player):
            legal_actions = legals_dodo(state, player)
            action = random.choice(legal_actions)
            state = play_dodo(state, action, player)
            player = adversaire(player)
        return score_dodo(state, player)

    root = Node(state)

    for _ in range(iterations):
        node = root
        state = root.state
        player = player

        # Select
        while node.untried_actions == [] and node.children != []:
            node, action = uct_select(node)
            state = play_dodo(state, action, player)
            player = adversaire(player)

        # Expand
        if node.untried_actions != []:
            action = random.choice(node.untried_actions)
            state = play_dodo(state, action, player)
            node.untried_actions.remove(action)
            node = node.add_child(state, action)
            player = adversaire(player)

        # Simulate
        result = rollout(state, player)

        # Backpropagate
        while node is not None:
            node.update(result)
            node = node.parent
            result = -result

    return max(root.children, key=lambda c: c[0].wins / c[0].visits)[1]


# boucle de jeu
def dodo(strategy_X: Strategy, strategy_O: Strategy, _size: int = 4) -> Score:
    state: State = initial_state_dodo()
    while not final_dodo(state, 1):
        action_1: Action = strategy_X(state, 1)
        state = play_dodo(state, action_1, 1)
        print("----------------joueur1-----------------------")
        print(action_1)
        print()
        pprint(state, 4)

        if not final_dodo(state, 2):
            action_2: Action = strategy_O(state, 2)
            state = play_dodo(state, action_2, 2)
            print("----------------joueur2-----------------------")
            print(action_2)
            print()
            pprint(state, 4)
        else:
            return score_dodo(state, 2)
    return score_dodo(state, 1)
