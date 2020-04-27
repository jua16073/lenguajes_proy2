# file to create another file

def create(dfa, extras, name):
    print("yay ", name)
    i = 0
    output = open("./outputs/" + name + ".py", "w+")
    output.write("#file to test\n\n")
    output.write("from libs import evaluate\n")


    output.write("class Automata:\n     def __init__(self, exp):\n        self.id = exp \n        self.states = []\n\n")
    output.write("class State: \n   def __init__(self,num):\n     self.id = num\n     self.transitions = []\n     self.accept = False \n\n")
    output.write("class Transition: \n  def __init__(self,sym,to):\n        self.symbol = sym\n        self.to = to\n\n")


    output.write("def read_word(file, actual):\n")
    output.write("  temp_word = ''\n")
    output.write("  while actual < len(file):\n")
    output.write("      if(file[actual] == ' ' or file[actual] == '\\n') and (len(temp_word)>0):\n")
    output.write("          break\n")
    output.write("      elif file[actual] == ' ' or file[actual] == '\\n':\n")
    output.write("          actual += 1\n")
    output.write("      else:\n")
    output.write("          temp_word += file[actual]\n")
    output.write("          actual += 1\n")
    output.write("  return temp_word, actual\n\n")

    
    
    output.write("def main():\n")
    
    write_automata(dfa, i, output)
    output.write("  prueba = open('./outputs/prueba.txt')\n")
    output.write("  data = prueba.read()\n")
    output.write("  prueba.close()\n")
    #output.write("  print(evaluate.is_in_language(automata0, 'asf8'))\n")
    
    output.write("  i = 0\n")
    output.write("  while i < len(data):\n")
    output.write("      word, i = read_word(data, i)\n")
    output.write("      print(word,': ', evaluate.is_in_language(automata0, word))\n")
    output.write("      i += 1\n")
    output.write('if __name__ == "__main__":\n'+'   main()')

    output.close()

def write_automata(automata,i, file):
    file.write("  automata"+str(i)+' = Automata("'+ automata.id+'")\n')
    for node in automata.states:
        file.write("  temp_node= State("+ str(node.id2) + ")\n")
        if node.accept:
            file.write("  temp_node.accept = True\n")
        for transition in node.transitions:
            file.write("  temp_transition = Transition('" +transition.symbol+"', "+str(transition.to) +")\n")
            file.write("  temp_node.transitions.append(temp_transition)\n")
        file.write("  automata"+str(i)+".states.append(temp_node)\n")