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

WINDOW = WindowSettings()