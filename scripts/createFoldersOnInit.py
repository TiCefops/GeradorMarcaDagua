import os


def criarPastas():
    locale = os.path.abspath(os.getcwd())
    try:
        os.makedirs(locale + "/gerados")
    except:
        print()

    try:
        os.makedirs(locale + "/marca")
    except:
        print()


class createFoldersOnInit:
    def __init__(self):
        criarPastas()

