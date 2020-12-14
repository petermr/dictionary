# dictionary editor
# read, write, modify AMI dictionaries

def read_dictionary_as_text(dictionary_file):
    with open(dictionary_file, "r") as f:
        dictionary = f.read();
    return dictionary