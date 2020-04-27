# Para automatas de funciones individuales
from libs import nfa
from libs import trees

OPERATORS = ['|', '*', '+', '?', '.', ')', '(']

EPSILON = "ε"

# manejo del arbol para mandar a la funcion correcta de la raiz del arbol
def t_handler(tree, automata):
    start = 0
    finish = 0
    if tree.data in OPERATORS:
        if tree.data == ".":
            start , finish = concatenation(tree, automata)
        elif tree.data == "|":
            start, finish = option(tree, automata)
        elif tree.data == "*":
            start, finish = kleene(tree, automata)
        elif tree.data == "+":
            start, finish = plus(tree, automata)
        elif tree.data == "?":
            start, finish = question(tree, automata)
    else:
        start, finish = single(tree, automata)
    return start, finish

# Crear los estados de un automata de concatenacion y transiciones 
def concatenation(tree, automata):
    symbol = tree.data
    
    if tree.left.data in OPERATORS:
        st1, fn1 = t_handler(tree.left, automata)
    else:
        st1, fn1 = single(tree.left, automata)
    
    if tree.right.data in OPERATORS:
        st2, fn2 = t_handler(tree.right, automata)
    else:
        st2, fn2 = single(tree.right, automata)

    fn1.transitions.append(nfa.Transition(EPSILON, st2.id))

    return st1, fn2

# Crear nodos y transiciones de un automata or
def option(tree, automata):
    symbol = tree.data

    start = nfa.State(len(automata.states), len(automata.states))
    automata.states.append(start)

    if tree.left.data in OPERATORS:
        st1, fn1 = t_handler(tree.left, automata)
    else:
        st1, fn1 = single(tree.left, automata)
    
    if tree.right.data in OPERATORS:
        st2, fn2 = t_handler(tree.right, automata)
    else:
        st2, fn2 = single(tree.right, automata)
    
    end = nfa.State(len(automata.states), len(automata.states))
    automata.states.append(end)

    start.transitions.append(nfa.Transition(EPSILON, st1.id))
    start.transitions.append(nfa.Transition(EPSILON, st2.id))
    fn1.transitions.append(nfa.Transition(EPSILON, end.id))
    fn2.transitions.append(nfa.Transition(EPSILON, end.id))

    return start, end

# r* = r+ | e
# Crear nodos y transiciones de un automata kleene
def kleene(tree, automata):
    symbol = tree.data

    start = nfa.State(len(automata.states), len(automata.states))
    automata.states.append(start)

    if tree.left.data in OPERATORS:
        st1, fn1 = t_handler(tree.left, automata)
    else:
        st1, fn1 = single(tree.left, automata)
    
    end = nfa.State(len(automata.states), len(automata.states))
    automata.states.append(end)

    start.transitions.append(nfa.Transition(EPSILON, st1.id))
    start.transitions.append(nfa.Transition(EPSILON, end.id))
    fn1.transitions.append(nfa.Transition(EPSILON, st1.id))
    fn1.transitions.append(nfa.Transition(EPSILON, end.id))

    return start, end

# r+ = r*r
# r+ = rr*
# Crear nodos y transiciones de un automata plus
def plus(tree, automata):
    symbol = tree.data

    if tree.left.data in OPERATORS:
        st1, fn1 = t_handler(tree.left, automata)
    else:
        st1, fn1 = single(tree.left, automata)
    
    temp = trees.Tree()
    temp.data = "*"
    temp.left = tree.left

    st2, fn2 = kleene(temp, automata)

    fn1.transitions.append(nfa.Transition(EPSILON, st2.id))

    return st1, fn2

# r? = r | e
# Crear nodos y transiciones de un automata ?
def question(tree, automata):

    temp = trees.Tree()
    temp2 = trees.Tree()
    temp2.data = EPSILON
    temp.data = "|"
    temp.left = tree.left
    temp.right = temp2

    st1, fn1 = option(temp, automata)

    return st1, fn1



# Creacion de automata de un solo simbolo
# Regresa los 2 estados creados, cada uno con sus transiciones
def single(tree, automata):
    symbol = tree.data
    first = nfa.State(len(automata.states), len(automata.states))
    automata.states.append(first)
    second = nfa.State(len(automata.states), len(automata.states))
    automata.states.append(second)
    first.transitions.append(nfa.Transition(symbol, second.id))
    return first, second

