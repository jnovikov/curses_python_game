from elements.elements import LineText, TextBox


class BaseElementFactory(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_item(self, *args, **kwargs):
        raise NotImplementedError("Method get_item is not implemented")

    def __call__(self, *args, **kwargs):
        return self.get_item(*args, **kwargs)


class LineTextCenteredFactory(BaseElementFactory):

    def get_item(self, text):
        return LineText(text).center(self.height, self.width)


class TextBoxCenteredFactory(BaseElementFactory):

    def get_item(self, size):
        return TextBox(size).center(self.height, self.width)
