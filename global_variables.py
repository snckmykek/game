from kivy.core.window import Window


# User
class UserInfo:
    name: str

    def __init__(self):
        self.name = 'Admin'


# end User


# Window
class WindowSettings:
    size: tuple
    width: int
    height: int

    def __init__(self):
        self.width = Window.width
        self.height = Window.height
        self.size = (self.width, self.height)


# end Window


# Level button
class LevelButton:
    size: tuple
    width: int
    height: int

    def __init__(self):
        self.width = Window.width / 8
        self.height = Window.height / 8
        self.size = (self.width, self.height)


# end Level button


# Common button
class CommonButton:
    size: tuple
    width: int
    height: int

    def __init__(self):
        self.width = Window.width / 4
        self.height = Window.height / 16
        self.size = (self.width, self.height)


# end Common button


WINDOW = WindowSettings()
LEVELBUTTON = LevelButton()
COMMONBUTTON = CommonButton()
FIRSTSHARDS = 10
LANGUAGE = 'ru'
