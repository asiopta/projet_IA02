from typing import Union

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

def empty_state(n : Taille) -> State:
    """c'est pas du tout clean. Mais ca marche (je pense)"""
    # je pense que je vais la changer, c'est à voir
    result: State = []
    n = n- 1 
    for i in range(-n, 1, 1):
        for j in range(-n, 1, 1):
            cell: Cell = (i, j)
            result.append((cell, 0))
    for i in range(0, n + 1 , 1):
        for j in range(0, n + 1, 1):
            if i == j == 0:
                pass
            else : 
                cell: Cell = (i, j)
                result.append((cell, 0))
            
    for i in range(2, n):
        
        result.append(((-1, i), 0))
        result.append(((i, -1), 0))
        result.append(((1, -i), 0))
        result.append(((-i, 1), 0))
    l =  n // 2 
    for i in range(1,l+1) :
        
        result.append(((-i, i), 0))
        result.append(((i, -i), 0))
       
    return result

def pprint(state: State, size: int):
    """Pretty print the state of the hexagonal grid"""
    # Sort first by y (descending) and then by x (ascending)
    sorted_state = sorted(state, key=lambda x: (-x[0][1], x[0][0]))
    real_size = size - 1
    j = 0

    for i in range(real_size, -real_size - 1, -1):
        if i > 0:
            print(i * "_ ", end="")
        
        # On recupere les elements qui ont la meme y 
        line_elements = []
        while j < len(sorted_state) and sorted_state[j][0][1] == i:
            line_elements.append(sorted_state[j])
            j += 1
        
        # on ordonne les elements suivant la valeur de x 
        for cell, player in sorted(line_elements, key=lambda x: x[0][0]):
            print(f"({cell[0]}, {cell[1]})", end="")
            print(player, end=" ")

        if i < 0:
            print(abs(i) * "_ ", end="")
        
        print("\n")




















