from pyvi.modes import insert


def keypress(editor, key):
    if key == "h":
        row, column = editor.active_window.cursor
        editor.active_window.cursor = (row, column - 1)
    elif key == "i":
        editor.mode = insert
    elif key == "j":
        row, column = editor.active_window.cursor
        editor.active_window.cursor = (row + 1, column)
    elif key == "k":
        row, column = editor.active_window.cursor
        editor.active_window.cursor = (row - 1, column)
    elif key == "l":
        row, column = editor.active_window.cursor
        editor.active_window.cursor = (row, column + 1)
