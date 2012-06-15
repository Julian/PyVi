from pyvi.modes import insert


def keypress(editor, key):
    if key == "h":
        editor.active_window.cursor.column -= 1
    elif key == "i":
        editor.mode = insert
    elif key == "j":
        editor.active_window.cursor.row += 1
    elif key == "k":
        editor.active_window.cursor.row -= 1
    elif key == "l":
        editor.active_window.cursor.column += 1
