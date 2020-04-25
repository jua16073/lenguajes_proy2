# Archivo general, controla todol

import decomp
import analysis

def main():
    input_file = open("./inputs/file.txt")
    data = input_file.read()
    input_file.close()
    name, characters, keywords, tokens = decomp.main(data)
    # print("nombre del compilador: ", name)
    # print("caracteres validos: ")
    # for c in characters:
    #     print(c, ": ", characters[c])
    # print("keywords")
    # for k in keywords:
    #     print(k, ": ", keywords[k])
    # print("tokens")
    # for t in tokens:
    #     print(t, ": ", tokens[t])
    analysis.analyze(name, characters, keywords, tokens)

if __name__ == "__main__":
    main()