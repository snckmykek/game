from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
from sqlite_requests import db
import random
from common_module import game_action

from world_map.main import WorldMap, locations_mine, locations

Builder.load_file(r'home/main.kv')


class Home(ModalView):

    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.world_map = WorldMap

    def on_open(self):
        current_loc_id = db.get_val_from_global('current_loc_id')
        current_lvl_id = db.get_val_from_global('current_lvl_id')
        game_action.execute_action('home', current_loc_id, current_lvl_id)

    def play_treasure_hunt(self):
        self.world_map.is_treasure_hunting = True
        self.world_map.current_location = locations[0]
        self.world_map.open()

    def play_stone_mine(self):
        self.world_map.is_treasure_hunting = False
        self.world_map.current_location = locations_mine[0]
        self.world_map.open()

    def open_game_store(self):
        pass

    def open_daily_bonus(self):
        pass


Home = Home()
