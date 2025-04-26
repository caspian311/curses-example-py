from cursed import CursedApp, CursedWindow, CursedMenu

# You instanciate the application through instanciating a CursedApp
app = CursedApp()

# The way to create windows is by creating classes derived from the
# CursedWindow class. These must have X, Y, WIDTH, and HEIGHT specified
# as class variables. 'max' or an integer value are valid for WIDTH and
# HEIGHT.
# A new gevent thread will be spawned for each window class.
# These act like singletons, and all functions should be class methods.
# The class itself will never be instanciated.
class MainWindow(CursedWindow):
    X, Y = (0, 0)
    WIDTH, HEIGHT = 'max', 23

    # To create a menubar, you create a CursedMenu instance in a MENU
    # class variable.
    # You add a menu to it with the add_menu function, and specify the
    # title, optional hotkey, and a list of menu items in the form of
    # (name, hotkey, callback) or (name, callback).
    # Menu items can be chosen by hotkeys or by the arrow keys and enter.
    MENU = CursedMenu()
    MENU.add_menu('File', key='f', items=[
        ('Save', 's', 'save'),
        ('Quit', 'q', 'quit'),
    ])
    MENU.add_menu('Edit', key='e', items=[
        ('Copy', 'c', 'copy'),
        ('Delete', 'delete')
    ])

    # Decorate your methods with @classmethod since no instance will ever
    # be instanciated.
    @classmethod
    def save(cls):
        # cls.addstr will write a string to x and y location (5, 5)
        cls.addstr('File->Save', 5, 5)

    @classmethod
    def quit(cls):
        # The quit function will run before the window exits.
        # Killing the window is triggered with cls.trigger('quit'),
        # which is the same way to trigger any other function in the
        # CursedWindow.
        cls.addstr('Quitting', 5, 5)

    @classmethod
    def copy(cls):
        cls.addstr('edit->copy', 5, 5)

    @classmethod
    def delete(cls):
        cls.addstr('edit->delete', 5, 5)

    @classmethod
    def update(cls):
        # The update function will be looped upon, so this is where you
        # want to put the main logic. This is what will check for key
        # presses, as well as trigger other functions through
        # cls.trigger.
        # Handle input here, other than what the menu will handle through
        # triggering callbacks itself.
        cls.addstr('x=10, y=12', 10, 12)
        # Press spacebar to open menu
        k = cls.getch()
        if k == 32:
            cls.openmenu()


class FooterWindow(CursedWindow):
    # This window will appear on the bottom, print the string
    # "Press f then q to exit", then quit. The message will stay on the
    # screen.
    # All windows must have called 'quit' to exit out of the program, or
    # simply ctrl-C could be pressed.
    X, Y = (0, 23)
    WIDTH, HEIGHT = 'max', 1

    @classmethod
    def init(cls):
        cls.addstr('Press f then q to exit')
        cls.refresh()
        cls.trigger('quit')


# You need to call app.run() to start the application, which handles
# setting up the windows.
result = app.run()
print(result)
# This checks if ctrl-C or similar was pressed to kill the application.
if result.interrupted():
    print('Ctrl-C pressed.')
else:
    # This will reraise exceptions that were raised in windows.
    result.unwrap()
