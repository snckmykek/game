import kivy

kivy.require('1.0.7')

from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from world_map.main import WorldMap
from dialog.main import dialog
from speech_parser import speech_parser
from sqlite_requests import db


speech_parser()

Builder.load_file(r'mainscreen.kv')


class Menu(BoxLayout):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

        self.world_map = WorldMap()
        self.dialog = dialog

    def play(self):
        self.world_map.open()

    def dialog(self):
        self.dialog.location = 'Первая'
        self.dialog.level = '-1'
        self.dialog.open()

    def delete_table(self, table='speech'):
        db.delete_table(table)

class CubesApp(App):

    def __init__(self, **kwargs):
        super(CubesApp, self).__init__(**kwargs)

    def build(self):
        return Menu()


if __name__ == '__main__':
    CubesApp().run()
