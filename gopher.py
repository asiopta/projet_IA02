from typing import Union
from fonctionscommunes import *

print(fc.empty_state(7))

def legals_Gopher(state:grid,Player:player) -> list[Cell] : 
    friendly = [] 
    ennemy = []
    legals = []
    for i,j in grid.enumerate() : 
         if j == player : 
             friendly.append(i)
             ennemy.append(i)
         if j != player and j!= 0 : 
             ennemy.append(i)
         
    if len(ennemy) == 0 and len(friendly) == 0 :
        
        

            
        
         
            
        
    
    
    
    
    
    
    
    
    
    
    

























