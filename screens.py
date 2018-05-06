import curses

from elements.elements import BaseDrawElement
from elements.factories import LineTextCenteredFactory, TextBoxCenteredFactory
from helpers.screen_helper import ScreenHelper
from helpers import UserExitException, get_random_string_without_repeats


class ScreenDrawer(object):
    def __init__(self, screen):
        self.screen = screen
        self.screen.clear()
        self.screen.refresh()

    def draw_element(self, draw_element: BaseDrawElement, color=None):
        if color:
            self.set_color(color)
        draw_element.draw(self.screen)
        self.screen.refresh()

    def set_color(self, color):
        self.screen.attron(curses.color_pair(color))

    def set_color_and_fill_background(self, color):
        self.set_color(color)
        self.screen.clear()

    def get_input(self, draw_element: BaseDrawElement):
        return draw_element.get_user_input(self.screen)


class ScreenInteraction(object):
    def __init__(self):
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        self.drawer = ScreenDrawer(ScreenHelper.get_screen())

    def interact(self):
        raise NotImplementedError("Method interact not implemented")


class WelcomeScreenInteraction(ScreenInteraction):
    def __init__(self):
        super().__init__()
        height, width = self.drawer.screen.getmaxyx()
        self.line_text_factory = LineTextCenteredFactory(width, height)
        self.text_box_centered_factory = TextBoxCenteredFactory(width, height)

    def draw_menu(self):
        height, width = self.drawer.screen.getmaxyx()
        self.drawer.set_color_and_fill_background(2)

        message = self.line_text_factory('CTF.Professional security.').move_y(6, 'Up')
        self.drawer.draw_element(message)

        message = self.line_text_factory("Вам предстоит угадать пароль от секретного хранилища").move_y(3, "Up")
        self.drawer.draw_element(message, color=1)

        message = self.line_text_factory("Введи 'hack', если готов")
        self.drawer.draw_element(message, color=3)

        message = self.line_text_factory('Введите exit чтобы выйти').move_y(2)
        self.drawer.draw_element(message)

        message = self.line_text_factory('Made by John@ShadowServants').set_y(height - 1)
        self.drawer.draw_element(message, color=1)

    def interact(self):
        user_input = None
        while user_input != "hack" and user_input != "exit":
            self.draw_menu()
            text_box = self.text_box_centered_factory(10).move_y(5).configure_border()
            self.drawer.draw_element(text_box)
            user_input = self.drawer.get_input(text_box).lower()
        if user_input == 'exit':
            raise UserExitException("User types exit")


class MainGameScreenInteraction(ScreenInteraction):
    def __init__(self, answer_len=8):
        super().__init__()
        height, width = self.drawer.screen.getmaxyx()
        self.line_text_factory = LineTextCenteredFactory(width, height)
        self.text_box_centered_factory = TextBoxCenteredFactory(width, height)
        self.answer = get_random_string_without_repeats(answer_len)

    def interact(self):
        user_input = None
        while user_input != "ready":
            user_input = self.draw_menu()
        self.input_answer()
        self.return_to_main_menu()

    def draw_menu(self):
        message = 'Пароль состоит только из цифр и заглавных латинских букв. ' \
                  'Длина пароля - {} символов'.format(len(self.answer))

        line_t = self.line_text_factory(message).move_y(10, "Up")
        self.drawer.draw_element(line_t, color=2)

        line_t = self.line_text_factory("Каждый символ может встречаться только один раз").move_y(7, "Up")
        self.drawer.draw_element(line_t, color=1)

        line_t = self.line_text_factory("Введи любую подстроку и узнаешь, начиная с какой позиции она содержится в "
                                        "пароле").move_y(5, "Up")

        self.drawer.draw_element(line_t, color=3)

        line_t = self.line_text_factory("Если такой подстоки нет, программа скажет об этом").move_y(3, "Up")
        self.drawer.draw_element(line_t)

        line_t = self.line_text_factory('Если ты готов вводить пароль, введи ready').move_y(1, 'Up')
        self.drawer.draw_element(line_t)

        line_t = self.line_text_factory("У тебя будет всего одна попытка чтобы ввести его.")
        self.drawer.draw_element(line_t, color=4)

        height, width = self.drawer.screen.getmaxyx()

        line_t = self.line_text_factory("Made by John@ShadowServants").set_y(height - 1)
        self.drawer.draw_element(line_t, color=1)

        t_box = self.text_box_centered_factory(10).move_y(3).configure_border()
        self.drawer.draw_element(t_box)
        user_input = self.drawer.get_input(t_box)
        if user_input != "ready":
            pos = self.answer.find(user_input) + 1
            self.drawer.screen.clear()
            text = "Нет такой подстроки"
            if pos != 0:
                text = 'Подстрока {} находится в пароле на позиции {}'.format(user_input, pos)
            line_t = self.line_text_factory(text).move_y(6)
            self.drawer.draw_element(line_t)
        return user_input

    def input_answer(self):
        self.drawer.screen.clear()
        line_t = self.line_text_factory('Введи свой пароль'.format(self.answer)).move_y(1, 'Up')
        self.drawer.draw_element(line_t)
        self.drawer.set_color(4)
        t_box = self.text_box_centered_factory(10).move_y(3).configure_border()
        self.drawer.draw_element(t_box)
        user_input = self.drawer.get_input(t_box)
        self.drawer.screen.clear()
        if user_input == self.answer:
            self.drawer.draw_element(self.line_text_factory('Верно! Ты получил доступ.').move_y(1, 'Up'), color=2)
        else:
            self.drawer.draw_element(self.line_text_factory("Неправильно. За тобой уже выехали!"), color=4)

    def return_to_main_menu(self):
        message = self.line_text_factory('Для воврата в главное меню нажмите любую клавишу').move_y(3)
        self.drawer.draw_element(message)
        k = ''
        while k == '':
            k = self.drawer.screen.getch()
