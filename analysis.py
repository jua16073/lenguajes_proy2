# Archivo para analizar las partes del archivo original
from libs import trees
from libs import evaluate
from libs import dfa_set
from libs import nfa
from libs import directo 
from libs import graph

import decomp

OPERATORS = ['|', 'ξ']
UNITARY = ['*', 'ψ', '?']
RESERVED_WORDS = ["ANY", "CONTEXT", "IGNORE", "PRAGMAS", "TOKENS", "CHARACTERS", "END", "IGNORECASE", "PRODUCTIONS", "WEAK", "COMMENTS","FROM", "NESTED", "SYNC", "COMPILER", "IF", "out", "TO"]
EPSILON  = "ε"

def analyze(name, characters, keywords, tokens):
    #print("analizando para ", name)
    character_parse_lines = CHARACTERS(characters)
    #print(character_parse_lines)
    keyword_parse_lines = KEYWORDS(keywords, character_parse_lines)
    #print(keyword_parse_lines)
    token_parse_lines = TOKENS(tokens, character_parse_lines)
    print(token_parse_lines)
    dfas, complete_line = make_tree(keyword_parse_lines, token_parse_lines)
    # Hacer automata
    #dfa = directo.directo(tree, complete_parse_line)
    final_dfa = make_one(dfas, complete_line)
    #graph.graph(final_dfa, "nani")
    #resp = evaluate.is_in_language(final_dfa, "nani")

    return final_dfa, dfas



def CHARACTERS(characters):
    # empezando con characters.
    print("analizando CHARACTERS")
    character_parse_line = {}
    for c in characters:
        temp_string = ""
        flag = False
        i = 0
        string_to_parse = ""
        while i < len(characters[c]):
            if characters[c][i] == '"' or characters[c][i] == "'":
                flag = not flag
                if not flag:
                    temp_string = temp_string[:-1] + ")"
                    string_to_parse += temp_string 
                    temp_string = ""
                else:
                    temp_string += "("
            elif flag:
                temp_string += characters[c][i] + "|"
            elif characters[c][i] == "+":
                string_to_parse += "|"
            elif temp_string + characters[c][i] in character_parse_line:
                string_to_parse += character_parse_line[temp_string+characters[c][i]]
                temp_string = ""
            elif temp_string == ".":
                if characters[c][i] == ".":
                    start = string_to_parse[-2]
                    finish = ""
                    while i < len(characters[c]):
                        if characters[c][i] == "'":
                            break
                        i += 1
                    finish = characters[c][i + 1]
                    j = ord(start)
                    while j < ord(finish):
                        string_to_parse += "|" + chr(j)
                        j += 1
                    string_to_parse += "|" + finish

            elif temp_string == "CHR(":
                number = ""
                while i < len(characters[c]):
                    if characters[c][i] == ")":
                        break
                    elif characters[c][i] == " ":
                        pass
                    else:
                        number += characters[c][i]
                    i += 1
                number = int(number)
                symbol = chr(number)
                string_to_parse += "'"+symbol+"'"
                temp_string = ""
            else:
                temp_string += characters[c][i]
            i += 1
        character_parse_line[c] = "(" +  string_to_parse + ")"
    return character_parse_line

def KEYWORDS(keywords, character_parse_line):
    print("analizando KEYWORDS")
    keyword_parse_lines = {}
    for k in keywords:
        word = keywords[k][:-1]
        i = 0
        temp = ""
        flag = False
        while i < len(word):
            if word[i] == '"':
                flag = not flag
                if not flag:
                    temp = temp[:-1] +  ")"
                else:
                    temp += "("
            else:
                temp += word[i] + "ξ"
            i += 1
        keyword_parse_lines[k] = temp
    return(keyword_parse_lines)

def word_break(line, characters, actual = 0, inicial = ""):
    temp = inicial
    actual += 1
    validos = [inicial]
    while actual < len(line):
        temp += line[actual]
        if temp in characters:
            validos.append(temp)
        actual += 1
    print(max(validos, key=len))
    return max(validos, key = len)


def TOKENS(tokens, characters):
    print("analizando TOKENS")
    tokens_parse_lines = {}
    for t in tokens:
        token = tokens[t]
        i = 0
        temp = ""
        parse_line = ""
        flag = False
        while i < len(token):
            temp += token[i]
            if temp in characters:
                og = temp
                temp = word_break(token, characters, i, temp)
                if og != temp:
                    i += len(temp) - len(og)
                if flag:
                    parse_line += characters[temp] + ")*"
                else:
                    parse_line += characters[temp]
                temp = ""
            if "|" == temp:
                parse_line = parse_line[:-2] + "|"
                temp = ""
            if temp == "{":
                flag = not flag
                parse_line += "ξ("
                temp = ""
            if temp == "}" and flag:
                flag = not flag
                temp = ""
            if temp == "[":
                second_flag = True
                if parse_line != "":
                    parse_line += "ξ"
                parse_line += "("
                temp = ""
            if temp == "]":
                second_flag = False
                parse_line += "?"
                temp = ""
            if temp == '"':
                inner = ""
                i += 1
                while i < len(token):
                    if token[i] == '"':
                        break
                    inner += token[i]
                    i += 1
                if parse_line != "" :
                    parse_line += "ξ(" + inner + ")"
                else:
                    parse_line += "(" + inner + ")"
                if token[i + 1] != "" and token[i + 1] != "\n" and token[i + 1] != ".":
                    parse_line += "ξ"
                temp = ""
            if temp == "(":
                parse_line += "("
                temp = ""
            if temp == ")":
                parse_line += ")"
                temp = ""
            i += 1
        if parse_line[-1] in OPERATORS:
            parse_line = parse_line[:-1]
        tokens_parse_lines[t] = parse_line
    return tokens_parse_lines

def make_tree(keyword_parse_lines, token_parse_lines):
    print("haciendo arboles")
    complete_line = ""
    dfas = {}
    for keyword in keyword_parse_lines:
        complete_line += "(" + keyword_parse_lines[keyword] + ")" + "|"
        tree = trees.evaluate(keyword_parse_lines[keyword])
        dfas[keyword] = directo.directo(tree, keyword_parse_lines[keyword])
    for token in token_parse_lines:
        complete_line += "(" + token_parse_lines[token] +")" + "|"
        #print(token, ": ", token_parse_lines[token])
        tree = trees.evaluate(token_parse_lines[token])
        #trees.print2DUtil(tree, 0)
        dfas[token] = directo.directo(tree, token_parse_lines[token])
    complete_line = complete_line[:-1]
    tree = trees.evaluate(complete_line)
    return dfas, complete_line

def make_one(dfas, complete_line):
    print("haciendo el ARBOL")
    tree = trees.evaluate(complete_line)
    final_dfa = directo.directo(tree, complete_line)
    return final_dfa