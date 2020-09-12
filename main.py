import kivy

kivy.require('1.0.7')

from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.animation import Animation

from home.main import Home
from dialog.main import dialog
from sqlite_requests import db
from common_module import game_action
from miniature.main import miniature
from treasure_cave_game.levels_list import levels_list
from kivy.clock import Clock

Builder.load_file(r'mainscreen.kv')

class Menu(BoxLayout):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

        self.home = Home
        self.dialog = dialog

        Clock.schedule_once(self.check_actions)

    def check_actions(self, d):
        current_loc_id = db.get_val_from_global('current_loc_id')
        current_lvl_id = db.get_val_from_global('current_lvl_id')
        game_action.execute_action('menu', current_loc_id, current_lvl_id)

    def play(self):
        self.home.open()

    def open_dialog(self):
        self.dialog.open()

    def delete_table(self, table='speech'):
        levels_list.open()


class CubesApp(App):

    def __init__(self, **kwargs):
        super(CubesApp, self).__init__(**kwargs)

    def build(self):
        return Menu()


if __name__ == '__main__':
    CubesApp().run()
