from typing import Union

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
    et revoie le joueur gagnant, l'état final et le score'''
    print()


'''
TODO:
- fonction qui inverse la position par rapport au couleur
- fonction qui inverse la positions par rapport l'axe vertical

- la fonction d'évaluation de la position

- une fonction qui visualise l'état du jeu (affichage de l'hexagon)
    pprint(state: State) -> None
- une fonction qui gère le jeu (le tour des joueurs)
    Dodo(strategy_1, strategy_2) -> Score

'''

'''
Jeux DODO:
on peut utiliser comme structure list[list[Player]]
Pour cela, on doit faire un convertissement de coordonnées
pour chaque cellule sous forme (int, int), ca devient (int+3, int+3)

'''


# nos fonctions à nous
def state_to_environnement(state: State) -> Environment:
    result: dict = {}
    for item in state:
        result[item[0]] = item[1]
    return result


def environnement_to_state(grid: Environment) -> State:
    result: State = []
    for key, value in grid.items():
        # print(key)
        # print(value)
        result.append((key, value))
    return result


def empty_state() -> State:
    """c'est pas du tout clean. Mais ca marche (je pense)"""
    # je pense que je vais la changer, c'est à voir
    result: State = []
    for i in range(-3, 1, 1):
        for j in range(-3, 1, 1):
            cell: Cell = (i, j)
            result.append((cell, 0))
    for i in range(0, 3, 1):
        for j in range(0, 3, 1):
            if i == j == 0:
                pass
            cell: Cell = (i, j)
            result.append((cell, 0))
    for i in {1, 2}:
        result.append(((-1, i), 0))
        result.append(((i, -1), 0))
    result.append(((-2, 1), 0))
    result.append(((1, -2), 0))
    return result


def initial_state() -> State:
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

# faut review et tester toutes les fonctions ci dessous
def voisins(cellule: Cell, grid: Environment) -> list[Cell]:
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


def voisins_libres(cellule_dodo: tuple[Cell, Player], grid: Environment) -> list[Cell]:
    voisins: list[Cell] = voisins_Dodo(cellule_dodo, grid)
    result: list[Cell] = []
    for cell in voisins:
        if grid(cell) == 0:
            result.append(cell)
    return result


def legals(state: State, tour: Player) -> list[ActionDodo]:
    result: list[ActionDodo] = []
    for cell in state:
        while cell[1] == tour:
            voisins = voisins_libres(cell, state_to_environnement(state))
            for voisin in voisins:
                result.append((cell[0], voisin))
    return result

def final(state: State, tour: Player) -> bool:
    return legals(state, tour) == 0

def score(state: State) -> int:
    if final(state, 1):
        return 1
    elif final(state, 2):
        return -1

def play(state: State, action: ActionDodo, tour: Player) -> State:
    if action not in legals(state, tour):
        print("erreur: action non légale")
        return state
    else:
        grid = state_to_environnement(state)
        grid[action[0]] = 0
        grid[action[1]] = tour
    return state


def main():
    state = empty_state()
    test = [((1, 0), 0), ((1, 2), 0), ((1, 3), 0)]
    print(test)
    test2 = state_to_environnement(test)
    print(test2)
    print(environnement_to_state(test2))


if __name__ == "__main__":
    main()
