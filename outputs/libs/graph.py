# Para graficar 
from graphviz import Digraph

OPERATORS = ['|', '*', '+', '?', '.', ')', '(']
EPSILON = "ε"
# Graficar un automata
# Teniendo nodo por estado de automata
# edge por transicion
def graph(automata, nombre):
    dot = Digraph(name = "Automata")
    #dot.attr(rankdir = "LR")
    for state in automata.states:
        if state.accept:
            dot.node(str(state.id2), str(state.id2), shape = "doublecircle")
        else:
            dot.node(str(state.id2), str(state.id2))
        for transition in state.transitions:
            dot.edge(str(state.id2),str(transition.to), transition.symbol)
    print(dot.source)
    dot.render('test-output/' + nombre + '.gv', view=True)

# Estado
# simbolos
# inicio
# aceptacion
# transicion
def to_txt(automata, nombre):
    f = open("txts/"+nombre+".txt", "w+")
    symbols = []
    for symbol in automata.id:
        if symbol not in OPERATORS and symbol not in symbols and symbol != EPSILON:
            symbols.append(symbol)
    f.write("Automata de "+ str(automata.id)+ "\n")
    f.write("simbolos del lenguaje: ")
    for symbol in symbols:
        f.write(symbol + " ")
    f.write("\n")
    for estado in automata.states:
        f.write("\n")
        if (estado.id2 == 0):
            f.write("Inicial ")
        if (estado.accept):
            f.write(" De Aceptacion")
        f.write("Estado: "+ str(estado.id2) + "\n")
        for transition in estado.transitions:
            f.write("con: "+ str(transition.symbol)+ " a: "+ str(transition.to) + "\n")

    f.close()

