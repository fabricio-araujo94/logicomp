"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """


from formula import *

def length(formula):
    """Determines the length of a formula in propositional logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return length(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length(formula.left) + length(formula.right) + 1


def subformulas(formula):
    """Returns the set of all subformulas of a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for subformula in subformulas(my_formula):
        print(subformula)

    This piece of code prints p, s, (p v s), (p → (p v s))
    (Note that there is no repetition of p)
    """

    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return {formula}.union(subformulas(formula.inner))
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        sub1 = subformulas(formula.left)
        sub2 = subformulas(formula.right)
        return {formula}.union(sub1).union(sub2)

#  we have shown in class that, for all formula A, len(subformulas(A)) <= length(A).


def atoms(formula):
    """Returns the set of all atoms occurring in a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for atom in atoms(my_formula):
        print(atom)

    This piece of code above prints: p, s
    (Note that there is no repetition of p)
    """

    if isinstance(formula, Atom):
        return {formula.__str__()}
    if isinstance(formula, Not):
        return atoms(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return atoms(formula.left).union(atoms(formula.right))


def number_of_binary_connectives(formula):
    """Returns the number of binary connectives in a formula.
    Binary connectives are connectives thay join two sentences.
    For example: number_of_binary_connectives((p → (¬q))) = 1.
    """

    if isinstance(formula, Atom):
        return 0
    if isinstance(formula, Not):
        return number_of_binary_connectives(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return number_of_binary_connectives(formula.left) + number_of_binary_connectives(formula.right) + 1


def number_of_atoms(formula):
    """Returns the number of atoms occurring in a formula.
    For instance,
    number_of_atoms(Implies(Atom('q'), And(Atom('p'), Atom('q'))))

    must return 3 (Observe that this function counts the repetitions of atoms)
    """

    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return number_of_atoms(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return number_of_atoms(formula.left) + number_of_atoms(formula.right)


def number_of_connectives(formula):
    """Returns the number of connectives occurring in a formula."""

    if isinstance(formula, Atom):
        return 0
    if isinstance(formula, Not):
        return number_of_connectives(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return number_of_connectives(formula.left) + number_of_connectives(formula.right) + 1


def is_literal(formula):
    """Returns True if formula is a literal. It returns False, otherwise"""
    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return True
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return is_literal(formula.left) and is_literal(formula.right)
    return False


def substitution(formula, old_subformula, new_subformula):
    """Returns a new formula obtained by replacing all occurrences
    of old_subformula in the input formula by new_subformula."""

    if isinstance(formula, Atom):
        return
    if isinstance(formula, Not):
        if formula.inner == old_subformula:
            formula.inner = new_subformula
        else:
            substitution(formula.inner, old_subformula, new_subformula)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        if formula.left == old_subformula:
            formula.left = new_subformula
        else:
            substitution(formula.left, old_subformula, new_subformula)
        if formula.right == old_subformula:
            formula.right == new_subformula
        else:
            substitution(formula.right, old_subformula, new_subformula)
    return formula


def is_clause(formula):
    """Returns True if formula is a clause. It returns False, otherwise"""

    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return is_literal(formula)
    if isinstance(formula, Or):
        return is_literal(formula.left) and is_literal(formula.right)
    return False


def is_negation_normal_form(formula):
    """Returns True if formula is in negation normal form.
    Returns False, otherwise."""

    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return isinstance(formula.inner, Atom)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return is_negation_normal_form(formula.left) and is_negation_normal_form(formula.right)


def is_cnf(formula):
    """Returns True if formula is in conjunctive normal form.
    Returns False, otherwise."""

    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return is_clause(formula)
    if isinstance(formula, And):
        if is_clause(formula.left) and is_clause(formula.right):
            return True
    return False

def is_term(formula):
    """Returns True if formula is a term. It returns False, otherwise"""

    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return is_literal(formula)
    if isinstance(formula, And):
        if is_literal(formula.left) and is_literal(formula.right):
            return is_term(formula.left) and is_term(formula.right)
    return False


def is_dnf(formula):
    """Returns True if formula is in disjunctive normal form.
    Returns False, otherwise."""

    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return is_term(formula)
    if isinstance(formula, Or):
        if isinstance(formula.left, Or):
            sub1 = is_dnf(formula.left)
        else:
            sub1 = is_term(formula.left)
        if isinstance(formula.right, Or):
            sub2 = is_dnf(formula.right)
        else:
            sub2 = is_term(formula.right)
        return sub1 and sub2
    return False



def is_decomposable_negation_normal_form(formula):
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""

    if is_negation_normal_form(formula):
        if isinstance(formula, And):
            if not len(set(atoms(formula.left)).intersection(atoms(formula.right))):
                return True
        if isinstance(formula, Or):
            return is_decomposable_negation_normal_form(formula.left) and is_decomposable_negation_normal_form(formula.right)
    return False

