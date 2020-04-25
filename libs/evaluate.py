# Archivo para evaluar una expresion
# En un automata

import collections

EPSILON = "ε"

# Chequear si la cadena de caracteres esta en el 
# lenguaje desrito por el automata
def is_in_language(automata, expresion):
    if expresion == " ":
        expresion = EPSILON
    actual = [0]
    actual = cerradura(automata, actual)
    i = 0
    while True:
        temp = []
        #print("simbolo: ",expresion[i])
        #print("Estados a chequear: ",actual)
        for num in actual:
            for transition in automata.states[num].transitions:
                if transition.symbol == expresion[i] and transition.to not in temp:
                    temp.append(transition.to)
        i += 1
        temp = cerradura(automata, temp)
        if not temp and expresion == EPSILON:
            break
        actual = temp.copy()
        if i > len(expresion)-1:
            break
    for id in actual:
        if automata.states[id].accept:
            return True
    return False
    
# Funcion de cerradura epsilon
def cerradura(automata, actual):
    for num in actual:
        for transition in automata.states[num].transitions:
            if transition.symbol == EPSILON and transition.to not in actual:
                actual.append(transition.to)
    return actual

# seleccion de un nodo de arbol basado en un id
def select(automata, id):
    for state in automata.states:
        if collections.Counter(state.id) == collections.Counter(id):
            return state
    return False
