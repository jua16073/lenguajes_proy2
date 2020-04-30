# Archivo general, controla todol

import decomp
import analysis
import to_file

def main():
    print("archivo?")
    archivo = input()
    input_file = open("./inputs/" + archivo)
    data = input_file.read()
    input_file.close()
    name, characters, keywords, tokens = decomp.main(data)
    final_dfa, dfas = analysis.analyze(name, characters, keywords, tokens)
    to_file.create(final_dfa, dfas, name)
    


if __name__ == "__main__":
    main()