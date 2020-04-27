# Generacion de NFA
from libs import trees
from libs import individuales

OPERATORS = ['|', '*', '+', '?', '.', ')', '(']
EPSILON = "ε"

# Clases para la creacion de automatas
class Automata:
    def __init__(self, exp):
        self.id = exp
        # Array de objetos State
        self.states = []

class State:
    def __init__(self, num, num2):
        self.id = num
        # debido a la implementacion de dfa's un segundo id sirve para graficar
        self.id2 = num2
        # Array de objetos Transition
        self.transitions = []
        self.accept = False
        #self.transitions.append(Transition(EPSILON, self.id))
    pass

class Transition:
    def __init__(self, sym, to):
        self.symbol = sym
        self.to = to

# Llama t_handler del archivo individuales.
def create_automata(tree, og):
    auto = Automata(og)
    trees.print2DUtil(tree, 5)
    start , finish = individuales.t_handler(tree, auto)
    finish.accept = True
    return auto