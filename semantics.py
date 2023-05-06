"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import *
from other_functions import *


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        return interpretation.get(formula.name) # the name of the atom is also the name of the key in the dictionary.
    if isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return not interpretation.get(formula.inner.name)
        else:
            return not truth_value(formula.inner, interpretation)
    if isinstance(formula, And):
        return truth_value(formula.left, interpretation) and truth_value(formula.right, interpretation)
    if isinstance(formula, Or):
        return truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    if isinstance(formula, Implies):
        return not truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)


def partial_truth_value(formula, interpretation):
    if isinstance(formula, Atom):
        if type(interpretation.get(formula.name)) == type(True):
            return interpretation.get(formula.name)
        else:
            return None

    if isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            if type(interpretation.get(formula.inner.name)) == type(True):
                return not interpretation.get(formula.inner.name)
            else:
                return None
        else:
            return not partial_truth_value(formula.inner, interpretation)

    if isinstance(formula, And):
        sub1 = partial_truth_value(formula.left, interpretation)
        sub2 = partial_truth_value(formula.right, interpretation)

        if sub1 == True and sub2 == True:
            return True
        elif sub1 == False or sub2 == False:
            return False
        else:
            return None

    if isinstance(formula, Or):
        sub1 = partial_truth_value(formula.left, interpretation)
        sub2 = partial_truth_value(formula.right, interpretation)

        if sub1 == True or sub2 == True:
            return True
        elif sub1 == False and sub2 == False:
            return False
        else:
            return None

    if isinstance(formula, Implies):
        sub1 = partial_truth_value(formula.left, interpretation)
        sub2 = partial_truth_value(formula.right, interpretation)

        if sub1 == False or sub2 == True:
            return True
        elif sub1 == True and sub2 == False:
            return False
        else:
            return None


def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    
    # Um tratamento para especificar o que foi passado como parâmetro para premisa: uma lista, uma fórmula ou nenhum dos dois.
    if type(premises) == list:
        formula = and_all(premises) # Será necessário para descobrir uma valoração que deixe todas as premisas verdadeiras.
    else:
        if not atoms(premises) == None:
            formula = premises
        else:
            return 'Premissa inválida.'

    conclusion_atoms = atoms(conclusion) # Necessário para filtrar os valores.
      
    while(1):
        check = satisfiability_brute_force(formula) # Valoração que deixa todas as premissas verdadeiras
  
        if check == False: # Quando todas as valorações foram encontradas (ou são inexistentes), o laço é quebrado.
            break
        
        # Filtragem de valores necessários para a conclusão.
        check_conclusion = {}
        
        for k, v in check.items():
            if k in conclusion_atoms:
                check_conclusion[k] = v

        if not truth_value(conclusion, check_conclusion): # Se for falsa, não é consequência lógica.
            return False
              
        formula = And(formula, Not(and_all(dict_to_atom(check)))) # Cria uma nova fórmula negando a valoração encontrada.
        
    return True


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    
    vars = atoms(formula1) # coleta das atômicas.
    tam = 2**len(vars) # quantidade de valorações possíveis.
    
    interpretation = {} # dicionário de valorações.
    
    # "Setando" todas as variáveis em True.
    for i in range(0, len(vars)):
        temp = vars.pop()
        interpretation[temp] = True
    
    # Ordenar as atômicas para melhor visualização.
    interpretation = dict(sorted(interpretation.items()))
    
    for i in range(0, tam):
        if not truth_value(formula1, interpretation) and truth_value(formula2, interpretation):
            return False
    
        for j, (k, v) in enumerate(interpretation.items()):
            if j == 0:
                interpretation[k] = not interpretation[k]
            elif not (i + 1) % (tam / 2**j):
                interpretation[k] = not interpretation[k]
    
    return True



def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    
    if satisfiability_brute_force(Not(formula)) == False:
        return True
    
    return False

def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    
    print(formula)
    vars = atoms(formula) # coleta das atômicas
    values = {}

    return sat_check(vars, formula, values)


def sat_check(vars, formula, values):
    if not len(vars): 
       if truth_value(formula, values):
           return values
       return False

    var = vars.pop() # selecionando atômica

    values1 = values.copy() 
    values2 = values.copy()
    
    # adicionando atômica ao dicionário da valoração
    values1[var] = True
    values2[var] = False
    
    check = sat_check(vars.copy(), formula, values1)

    if check != False:
       return check

    return sat_check(vars.copy(), formula, values2)


def double_satisfiability(formula):
    check = satisfiability_brute_force(formula)
    
    if check == False:
        return False
        
    new_formula = And(formula, Not(and_all(dict_to_atom(check))))
    
    if satisfiability_brute_force(new_formula) == False:
        return False
        
    return True

def all_models(formula):
    vars = atoms(formula) # coleta das atômicas.
    tam = 2**len(vars) # quantidade de valorações possíveis.
    
    interpretation = {} # dicionário de valorações.
    
    # "Setando" todas as variáveis em True.
    for i in range(0, len(vars)):
        temp = vars.pop()
        interpretation[temp] = True
    
    # Ordenar as atômicas para melhor visualização.
    interpretation = dict(sorted(interpretation.items()))
    # Também é necessário para o laço interno.
    
    true_interpretation = [] # lista para armazenar as valorações
    
    for i in range(0, tam):
        if truth_value(formula, interpretation):
            true_interpretation.append(interpretation.copy())
    
        for j, (k, v) in enumerate(interpretation.items()):
            if j == 0:
                interpretation[k] = not interpretation[k]
            elif not (i + 1) % (tam / 2**j):
                interpretation[k] = not interpretation[k]

    return true_interpretation
    
