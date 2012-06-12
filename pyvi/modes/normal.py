from pyvi.modes import insert


def keypress(editor, key):
    if key == "i":
        editor.mode = insert
