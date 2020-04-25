

COMMENTS = ["/*", "*/", "//"]

def read_word(file, actual):
    temp_word = ""
    while actual < len(file):
        if (file[actual] == " " or file[actual] == "\n") and (len(temp_word) > 0):
            break
        elif file[actual] == " " or file[actual] == "\n":
            actual += 1
        else:
            temp_word += file[actual]
            actual += 1
    return temp_word, actual

def main(file):
    actual = 0
    characters = []
    keywords = []
    tokens = []
    productions = []
    temp_word = ""
    while True:
        temp_word, actual = read_word(file, actual)
        if temp_word == "COMPILER":
            name, actual = COMPILER(file, actual)
        if temp_word == "CHARACTERS":
            characters, actual = CHARACTERS(file, actual)
        if temp_word == "KEYWORDS":
            keywords, actual = KEYWORDS(file, actual)
        if temp_word == "TOKENS":
            tokens, actual = TOKENS(file, actual)
        if temp_word == "PRODUCTIONS":
            PRODUCTIONS(file, actual)
        if temp_word == "END":
            final = END(file, actual, name)
            if final:
                break
            else:
                print("No coincide el nombre")
                break
    
    return name, characters, keywords, tokens

def COMPILER(file, actual):
    actual += 1 
    name, actual = read_word(file, actual)
    return name, actual

def CHARACTERS(file, actual):
    actual += 1
    temp = ""
    characters = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "KEYWORDS":
            actual -= 8
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                characters[temp_id] = temp_values
                line =  ""
            else:
                print("no se encuentra el '='")
    return characters, actual

def KEYWORDS(file, actual):
    actual += 1
    temp = ""
    keywords = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "TOKENS":
            actual -= 6
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                keywords[temp_id] = temp_values
                line =  ""
            else:
                print("no se encuentra el '='")
    return keywords, actual

def TOKENS(file, actual):
    actual += 1
    temp = ""
    tokens = {}
    temp_id = ""
    temp_values = ""
    line = ""
    while True:
        temp, actual = read_word(file, actual) 
        if temp == "PRODUCTIONS":
            actual -= 11
            break
        line += temp
        if line[-1] == ".":
            if "=" in line:
                completo = line.split("=")
                temp_id = completo[0]
                temp_values = completo[1]
                tokens[temp_id] = temp_values
                line =  ""
            else:
                print("no se encuentra el '='")
    return tokens, actual

def PRODUCTIONS(file, actual):
    return actual

def END(file, actual, name):
    actual += 1
    end_name, actual = read_word(file, actual)
    if end_name == name:
        return True
    return False


if __name__ == "__main__":
    file = open("inputs/file.txt")
    content = file.read()
    main(content)
    file.close()