import curses
import time

from helpers import UserExitException
from helpers.screen_helper import ScreenHelper
from screens import WelcomeScreenInteraction, MainGameScreenInteraction


class Application(object):
    def __init__(self):
        screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        ScreenHelper.set_screen(screen)

    def run(self):
        try:
            while True:
                WelcomeScreenInteraction().interact()
                MainGameScreenInteraction(answer_len=8).interact()
        except KeyboardInterrupt:
            self.stop()
        except UserExitException:
            self.stop()
        except Exception as e:
            self.stop()
            print("Wow something was wrong. Please send this to game-creator {}".format(e))

    def stop(self):
        curses.nocbreak()
        # self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


if __name__ == '__main__':
    # curses.wrapper(debug)
    app = Application()
    app.run()
