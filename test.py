import curses

from dataclasses import dataclass
from threading import Thread
from time import sleep
from cursed import CursedApp, CursedWindow, CursedMenu

f = open("out.log", "w")
def log(message):
    f.write(f"{message}\n")
    f.flush()

SCREEN_WIDTH, SCREEN_HEIGHT = (240, 55)

@dataclass
class GlobalData():
    def __init__(self):
        self.counter = 0
        self.user_counter = 0
        self.quit = False
        self.quit_now = False

MAIN = GlobalData()

class MainWindow(CursedWindow):
    X, Y = (0, 0)
    WIDTH, HEIGHT = (SCREEN_WIDTH, SCREEN_HEIGHT - 10)
    BORDERED = True

    @classmethod
    def update(cls):
        if MAIN.quit_now:
            cls.trigger('quit')

        cls.addstr("Main Window", 5, 5)
        cls.addstr(f"Counter: {MAIN.counter:3d}", 5, 6)
        cls.addstr(f"Counter: {MAIN.user_counter:3d}", 5, 7)

        cls.refresh()


class UserStatsWindow(CursedWindow):
    X, Y = (0, SCREEN_HEIGHT - 10)
    WIDTH, HEIGHT = (SCREEN_WIDTH, 10)
    BORDERED = True

    @classmethod
    def update(cls):
        if MAIN.quit_now:
            cls.trigger('quit')

        cls.addstr("User Stats Window", 5, 5)
        cls.addstr(f"Counter: {MAIN.counter:3d}", 5, 6)
        cls.addstr(f"Counter: {MAIN.user_counter:3d}", 5, 7)

        k = cls.getch()
        if k == 105:
            MAIN.user_counter += 1
        elif k == 100:
            MAIN.user_counter -= 1
        elif k == ord('q'):
            MAIN.quit = True

        cls.refresh()


def main_app_stuff():
    for i in range(100):
        if MAIN.quit:
            MAIN.quit_now = True
            break
        MAIN.counter += 1
        log(f"updating counter to {MAIN.counter}")
        sleep(1)


def main():
    thread = Thread(target=main_app_stuff)
    thread.start()

    app = CursedApp()
    result = app.run()
    print(result)
    if result.interrupted():
        print('Ctrl-C pressed.')
    else:
        result.unwrap()
    thread.join()
    log("exiting")

if __name__ == "__main__":
    main()

