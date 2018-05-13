import os

from text_processing import *


def read_file(file):
    file = open(file, "r")
    return [line for line in file.readlines() if line != '\n']


def read_text(file):
    file = open(file, "r")
    text = file.read()
    return split_into_sentences(text)


def write_triples_to_file(triples):
    open("output/triples.txt", "w").close()
    file = open("output/triples.txt", "r+")
    for triple in triples:
        file.write(triple.__str__())
    file.close()

