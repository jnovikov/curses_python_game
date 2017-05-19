import curses
from curses.textpad import rectangle
from random import randint, seed
import time
from string import ascii_uppercase, digits


def get_random_string(n):
    res = ''
    seed(str(time.time()))
    alpha = list(ascii_uppercase + digits)
    for i in range(n):
        k = randint(0, len(alpha) - 1 - i)
        res += alpha[k]
        alpha[k], alpha[len(alpha) - i - 1] = alpha[len(alpha) - i - 1], alpha[k]
    return res


class LineText(object):
    color = None

    def __init__(self, text):
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
        screen.refresh()


class TextBox(object):
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


class ApplicationDrawer(object):
    def __init__(self, screen):
        self.stdscr = screen
        self.stdscr.clear()
        self.stdscr.refresh()

    def draw_line(self, line: LineText):
        self.stdscr.addstr(line.y, line.x, line.text)
        self.stdscr.refresh()

    def draw_text_box(self, box: TextBox):
        rectangle(self.stdscr, box.uly, box.ulx, box.lry, box.lrx)
        self.stdscr.refresh()

        s = self.stdscr.getstr(box.ty, box.tx, box.len)
        self.stdscr.refresh()
        return s

    def set_color(self, color):
        self.stdscr.attron(curses.color_pair(color))


class Application(object):
    def __init__(self):
        screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        self.drawer = ApplicationDrawer(screen)
        # Start colors in curses

    def draw_main_menu(self):
        a = ''
        while a != 'exit' and a != 'hack':
            height, width = self.drawer.stdscr.getmaxyx()
            # curses.echo()
            self.drawer.set_color(2)
            self.drawer.stdscr.clear()
            message = LineText('CTF.Professional security.').center(height, width).move_y(6, 'Up')
            self.drawer.draw_line(message)
            self.drawer.set_color(1)
            message = LineText('Вам предстоит угадать пароль от секретного хранилища') \
                .center(height, width).move_y(3, 'Up')
            self.drawer.draw_line(message)
            self.drawer.set_color(3)
            message = LineText('Введи hack если готов').center(height, width)
            self.drawer.draw_line(message)
            message = LineText('Введите exit чтобы выйти').center(height, width).move_y(2)
            self.drawer.draw_line(message)
            self.drawer.set_color(1)
            message = LineText('Made by John@ShadowServants').center(height, width).set_y(height - 1)
            self.drawer.draw_line(message)
            # t = TextBox(10)
            t = TextBox(10).center(height, width).move_y(5).configure_border()
            a = self.drawer.draw_text_box(t).decode('utf-8')
            a = a.lower()
        if a == 'exit':
            self.stop()
        else:
            self.drawer.stdscr.clear()

    def draw_game(self):
        req = ''
        n = 8
        answer = get_random_string(n)
        self.drawer.stdscr.clear()
        while req != 'ready':
            height, width = self.drawer.stdscr.getmaxyx()
            # curses.echo()
            self.drawer.set_color(2)

            message = LineText(
                'Пароль состоит только из цифр и заглавных латинских букв. Длина пароля - {} символов'.format(
                    n)).center(height,
                               width).move_y(
                10, 'Up')
            self.drawer.draw_line(message)
            self.drawer.set_color(1)
            message = LineText('Каждый символ может встречаться только один раз'.format(n)).center(height,
                                                                                                   width).move_y(7,
                                                                                                                 'Up')
            self.drawer.draw_line(message)
            self.drawer.set_color(3)
            message = LineText(
                'Введи любую подстроку и узнаешь, начиная с какой позиции она содержится в пароле.').center(height,
                                                                                                            width).move_y(
                5, 'Up')
            self.drawer.draw_line(message)
            message = LineText('Если такой подстоки нет, программа скажет об этом').center(height, width).move_y(3,
                                                                                                                 'Up')
            self.drawer.draw_line(message)
            message = LineText('Если ты готов вводить пароль, введи ready').center(height, width).move_y(1, 'Up')
            self.drawer.draw_line(message)
            self.drawer.set_color(4)
            message = LineText('У тебя будет всего одна попытка чтобы ввести его.').center(height, width)
            self.drawer.draw_line(message)
            self.drawer.set_color(1)

            message = LineText('Made by John@ShadowServants').center(height, width).set_y(height - 1)
            self.drawer.draw_line(message)
            t = TextBox(10).center(height, width).center(height, width).move_y(3).configure_border()
            req = self.drawer.draw_text_box(t).decode('utf-8')
            pos = answer.find(req) + 1
            self.drawer.stdscr.clear()
            line = 'Подстрока {} находится в пароле на позиции {}'.format(req, pos)
            if pos == 0:
                line = 'Нет такой подстроки'
            message = LineText(line).center(height, width).move_y(6)
            self.drawer.draw_line(message)

        self.drawer.stdscr.clear()
        height, width = self.drawer.stdscr.getmaxyx()
        message = LineText('Введи свой пароль. debug {}'.format(answer)).center(height, width).move_y(1, 'Up')
        self.drawer.draw_line(message)
        self.drawer.set_color(4)
        t = TextBox(10).center(height, width).center(height, width).move_y(3).configure_border()
        req = self.drawer.draw_text_box(t).decode('utf-8')
        self.drawer.stdscr.clear()
        if req == answer:
            self.drawer.set_color(2)
            message = LineText('Верно! Ты получил доступ.'.format(answer)).center(height, width).move_y(1, 'Up')
            self.drawer.draw_line(message)
        else:
            self.drawer.set_color(4)
            message = LineText('Неправильно. За тобой уже выехали!'.format(answer)).center(height, width).move_y(1,
                                                                                                                 'Up')
            self.drawer.draw_line(message)
        k = ''
        while k == '':
            k = self.drawer.stdscr.getch()

    def run(self):
        try:
            while True:
                self.draw_main_menu()
                self.draw_game()
        except Exception:
            self.stop()

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        curses.nocbreak()
        # self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


def debug(screen):
    screen.clear()
    screen.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    k = 0
    while k != ord('q'):
        text = LineText('kek')
        text.draw(screen)
        screen.refresh()
        k = screen.getch()


if __name__ == '__main__':
    # curses.wrapper(debug)
    app = Application()
    app.run()
