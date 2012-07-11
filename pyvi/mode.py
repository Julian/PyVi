class Mode(object):
    """
    A Mixin to provide the basic functionality for an editor mode.

    """
    def __init__(self, editor):
        self.editor = editor

    def keypress(self, key):
        if key == "esc":
            self.editor.mode = self.editor.Normal(self.editor)
        else:
            handler = getattr(self, "keypress_" + key, None)
            if handler is not None:
                handler()

    def __repr__(self):
        return "<Mode: %s>" % (self.mode.title(),)
