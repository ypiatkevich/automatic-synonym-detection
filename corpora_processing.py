def read_file(file):
    file = open(file, "r")
    return [line for line in file.readlines() if line != '\n']