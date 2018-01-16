from curses.textpad import rectangle


class BaseDrawElement(object):
    def draw(self, screen):
        raise NotImplementedError("Not implemented")

    def get_user_input(self, screen):
        raise NotImplementedError("GetUser input is not implemented")


class TextBox(BaseDrawElement):
    def __init__(self, size):
        self.len = size
        self.tx = 1
        self.ty = 1
        self.uly = 1
        self.ulx = 1
        self.lry, self.lrx = 2, 6

    def center(self, h, w):
        self.tx = int((w // 2) - (self.len // 2) - self.len % 2)
        self.ty = int((h // 2) - 2)
        return self

    def move_y(self, size, where='Down'):
        if where == 'Up':
            self.ty -= size
        else:
            self.ty += size
        return self

    def configure_border(self):
        self.uly = self.ty - 1
        self.ulx = self.tx - 1
        self.lry = self.ty + 1
        self.lrx = self.tx + self.len + 1
        return self

    def draw(self, screen):
        rectangle(screen, self.uly, self.ulx, self.lry, self.lrx)

    def get_user_input(self, screen):
        return screen.getstr(self.ty, self.tx, self.len).decode('utf-8')


class LineText(BaseDrawElement):
    color = None

    def __init__(self, text=None):
        self.text = text
        self.x = 1
        self.y = 1

    def set_x_y(self, x, y):
        self.x = x
        self.y = y
        return self

    def set_y(self, y):
        self.y = y
        return self

    def center(self, h, w):
        self.x = int((w // 2) - (len(self.text) // 2) - len(self.text) % 2)
        self.y = int((h // 2) - 2)
        return self

    def move_y(self, size, where='Down'):
        if where == 'Up':
            self.y -= size
        else:
            self.y += size
        return self

    def draw(self, screen):
        screen.addstr(self.y, self.x, self.text)

