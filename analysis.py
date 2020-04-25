# Archivo para analizar las partes del archivo original
from libs import trees
from libs import evaluate
from libs import dfa_set
from libs import nfa
from libs import directo 
from libs import graph

import decomp

RESERVED_WORDS = ["ANY", "CONTEXT", "IGNORE", "PRAGMAS", "TOKENS",\
    "CHARACTERS", "END", "IGNORECASE", "PRODUCTIONS", "WEAK", "COMMENTS", \
        "FROM", "NESTED", "SYNC", "COMPILER", "IF", "out", "TO"]
EPSILON  = "ε"

def analyze(name, characters, keywords, tokens):
    print("analizando para ", name)
    character_parse_lines = CHARACTERS(characters)
    #print(character_parse_lines)
    keyword_parse_lines = KEYWORDS(keywords, character_parse_lines)
    #print(keyword_parse_lines)
    token_parse_lines = TOKENS(tokens, character_parse_lines)
    #print(token_parse_lines)
    tree, complete_parse_line = make_tree(keyword_parse_lines, token_parse_lines)
    # Hacer automata
    dfa = directo.directo(tree, complete_parse_line)
    graph.graph(dfa, "pls")

    print(evaluate.is_in_language(dfa, "nani69"))


def CHARACTERS(characters):
    # empezando con characters.
    character_parse_line = {}
    for c in characters:
        temp_string = ""
        flag = False
        i = 0
        string_to_parse = ""
        while i < len(characters[c]):
            if characters[c][i] == '"':
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
                string_to_parse += "."
            elif temp_string + characters[c][i] in character_parse_line:
                string_to_parse += character_parse_line[temp_string+characters[c][i]]
                temp_string = ""
            else:
                temp_string += characters[c][i]
            i += 1
        character_parse_line[c] = string_to_parse
    return character_parse_line

def KEYWORDS(keywords, character_parse_line):
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
                temp += word[i] + "."
            i += 1
        keyword_parse_lines[k] = temp
    return(keyword_parse_lines)

def TOKENS(tokens, characters):
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
                if flag:
                    parse_line += characters[temp] + ")*"
                else:
                    parse_line += characters[temp]
                temp = ""
            if temp == "{":
                flag = not flag
                parse_line += ".("
                temp = ""
            if temp == "}" and flag:
                flag = not flag
                temp = ""
            i += 1
            tokens_parse_lines[t] = parse_line
    return tokens_parse_lines

def make_tree(keyword_parse_lines, token_parse_lines):
    complete_line = ""
    for keyword in keyword_parse_lines:
        complete_line += "(" + keyword_parse_lines[keyword] + ")" + "|"
    for token in token_parse_lines:
        complete_line += "(" + token_parse_lines[token] +")" + "|"
    complete_line = complete_line[:-1]
    print(complete_line)
    print(complete_line)
    tree = trees.evaluate(complete_line)
    return tree, complete_line