# Can be useful as singleton alternative
class ScreenHelper(object):
    _screen = None

    @classmethod
    def get_screen(cls):
        return cls._screen

    @classmethod
    def set_screen(cls, screen):
        cls._screen = screen
