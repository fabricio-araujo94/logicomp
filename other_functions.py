from formula import *

def and_all(list):
    if len(list) > 2:
        return And(list[0], and_all(list[1:]))
    elif len(list) == 2:
        return And(list[0], list[1])
    else:
        return None
        
def dict_to_atom(interpretation):
    atoms = []
    
    for k, v in interpretation.items():
        if v == False:
            atoms.append(Not(Atom(k)))
        else:
            atoms.append(Atom(k))
            
    return atoms