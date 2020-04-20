# Archivo para procesar un archivo de CocoR

cocor_words = ["COMPILER", "CHARACTERS", "KEYWORDS", "TOKENS", "PRODUCTIONS", "END"]

def main(file):
    flag = 0
    ids = []
    for line in file:
        #print("toca la linea: ", line)
        if "(." in line:
            flag += 10
        if flag == 0 and "COMPILER" in line:
            name = line.split("COMPILER")[1][1:]
            print(name , "\n")
        elif flag == 1:
            if line != " \n" and line != "\n":
                    temp_id = line.split("=")[0]
                    temp_value = line.split("=")[1]
                    print(temp_id)
                    print(temp_value[0:len(temp_value)-2])
        elif flag == 2:
            print("Tocan Keywords")
        elif flag == 3:
            print("Tocan Tokens")
        elif flag == 4:
            print("Tocan Producciones")
        elif flag == 5:
            print("Final")
        elif flag >= 10:
            pass

        if check(line):
            flag += 1
        if ".)" in line:
            flag -= 10

def check(line):
    for word in cocor_words:
        if word in line:
            return True
    return False
            

if __name__ == "__main__":
    input = open("inputs/file.txt")
    main(input)