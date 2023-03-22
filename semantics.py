"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        return interpretation.get(formula.name)
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
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    pass
    # ======== YOUR CODE HERE ========


def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


