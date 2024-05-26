from typing import Union
from fonctionscommunes import *

#print(empty_state(7))



def one_ennemy_connection(cell: Cell,player:Player, grid : State) -> bool  : 
    
    State = state_to_environnement(grid)
    voisins = voisins(cell,State)
    nb_ennemies_connection = 0
    
    for i in voisins : 
        
        if State[i] != Player and State[i] != 0 : 
            
            nb_ennemies_connection = nb_ennemies_connection + 1
    
    if nb_ennemies_connection == 1 : return True
    return False


def friendy_connection(cell: Cell,player:Player, grid : State) -> bool  : 
    State =  state_to_environnement(grid)
    voisins = voisins(cell,grid)
    
    for i in voisins : 
        
        if State[i] == Player :  return True
    
    return False
            

def legals_Gopher(grid:State,player:Player) -> list[Cell] : 
    
    state =  state_to_environnement(grid)

    vide = True
    for i,j in state.items() : 
         if j != 0 : vide = False
    
    if vide :
        return list(state.keys())
    
    legals = []
    
    for i,j in state.enumerate() : 
        
        if not friendy_connection(i,player,state) and  one_ennemy_connection(i,player,state) : 
            legals.append(i)
    return legals

 
print(legals_Gopher(empty_state(7),1))
            
            
            
            
            
            
            
        
        

            
        
         
            
        
    
    
    
    
    
    
    
    
    
    
    

























