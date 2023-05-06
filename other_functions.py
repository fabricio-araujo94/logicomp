from formula import *

def and_all(list):
    """Takes a list of formulas and creates a formula that is a disjunction of all formulas in the list."""

    if len(list) > 2:
        return And(list[0], and_all(list[1:]))
    elif len(list) == 2:
        return And(list[0], list[1])
    else:
        return list[0]
        
def dict_to_atom(interpretation):
    """Turns a dictionary into a list of atoms."""
    
    atoms = []
    
    for k, v in interpretation.items():
        if v == False:
            atoms.append(Not(Atom(k)))
        else:
            atoms.append(Atom(k))
            
    return atoms