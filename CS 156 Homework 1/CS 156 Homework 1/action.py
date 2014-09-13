__author__ = 'Anthony Ferrero'


class Action(object):
    """Represents a singly-linked list of actions."""
    def __init__(self, parent=None):
        self._parent = parent

    def parent(self):
        return self._parent


class Up(Action):
    def __init__(self, parent):
        super.__init__(parent)


class Down(Action):
    def __init__(self, parent):
        super.__init__(parent)


class Right(Action):
    def __init__(self, parent):
        super.__init__(parent)


class Left(Action):
    def __init__(self, parent):
        super.__init__(parent)
