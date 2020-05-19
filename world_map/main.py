from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from global_variables import WINDOW
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.widget import Widget
from sqlite_requests import db
from dialog.main import dialog
from kivy.animation import Animation
import random
from treasure_chest.main import TreasureChest
from inventory.main import Inventory
from store.main import storescreen as store

from cubes_game.main import CubesGame
from cubes_game.rounds import rounds
from cubes_game.animatoins import do_animation

Builder.load_file(r'world_map/main.kv')


class Round(Button):

    def __init__(self, **kwargs):
        super(Round, self).__init__(**kwargs)

        self.background_normal = 'images/level_pins/ne_najataya.png'
        self.background_down = 'images/level_pins/najataya.png'
        self.round = 0
        self.size = [WINDOW.width / 4, WINDOW.width / 4]
        self.size_1 = [0, 0]
        self.size_2 = [0, 0]
        self.size_3 = [0, 0]
        self.size_4 = [0, 0]
        self.size_lock = [self.width, self.height]
        self.size_lock_default = self.size_lock.copy()

    def animate_round(self):
        pass

    def change_stars(self, qty_stars):
        self.size_1 = [0, 0]
        self.size_2 = [0, 0]
        self.size_3 = [0, 0]
        self.size_lock = [0, 0]

        if qty_stars == -1:
            self.size_lock = [self.width, self.height]
        if qty_stars > 0:
            self.size_1 = [self.width / 3.5, self.height / 3.5]
        if qty_stars > 1:
            self.size_2 = [self.width / 3.5, self.height / 3.5]
        if qty_stars > 2:
            self.size_3 = [self.width / 3.5, self.height / 3.5]
        if qty_stars > 3:
            self.size_4 = [self.width / 2.5, self.height / 2.5]

        self.size_lock_default = self.size_lock.copy()


class ParameterButton(Button):

    def __init__(self, **kwargs):
        super(ParameterButton, self).__init__(**kwargs)

        self.parameter = ''
        self.default_center_x = 0
        self.border = [0, 0, 0, 0]


class WorldMap(ModalView):

    def __init__(self, **kwargs):
        super(WorldMap, self).__init__(**kwargs)

        self.dialog = dialog
        self.is_first_open_location = True
        self.is_treasure_hunting = True

        self.cubes_game = CubesGame()
        self.inventory = Inventory()
        self.screenstore = store
        self.world_map = self.ids.world_map
        self.coords = tuple()
        self.locations = locations
        self.current_location = self.locations[0]
        self.menu_buttons = list()
        self.add_buttons()

    def add_buttons(self):
        button = ParameterButton(text='next', size_hint=(None, None), width=WINDOW.width / 5, height=WINDOW.height / 12,
                                 on_press=self.open_next_or_prev_location, pos_hint={'x': .8})
        button.parameter = 'next'
        self.ids.rl.add_widget(button)

        button = ParameterButton(text='prev', size_hint=(None, None), width=WINDOW.width / 5, height=WINDOW.height / 12,
                                 on_press=self.open_next_or_prev_location, pos_hint={'x': 0})
        button.parameter = 'prev'
        self.ids.rl.add_widget(button)

        open_close_menu_button = ParameterButton(text='', size_hint=(None, None),
                                                 size=[WINDOW.height / 12, WINDOW.height / 12],
                                                 on_press=self.open_close_menu,
                                                 pos=[WINDOW.width * .85, WINDOW.height * .77])
        open_close_menu_button.parameter = 'open'
        open_close_menu_button.background_normal = 'images/maps/menu_buttons/open_menu_button.png'
        open_close_menu_button.background_down = 'images/maps/menu_buttons/open_menu_button.png'
        self.ids.rl.add_widget(open_close_menu_button)

        self.menu_buttons.clear()

        button = ParameterButton(text='', size_hint=(None, None), size=[0, 0],
                                 on_press=self.open_close_menu, pos=[WINDOW.width * .85, WINDOW.height * .7])
        button.parameter = 'teleport'
        button.background_normal = 'images/maps/menu_buttons/teleport_menu_button.png'
        button.background_down = 'images/maps/menu_buttons/teleport_menu_button_down.png'
        self.menu_buttons.append(button)

        button = ParameterButton(text='', size_hint=(None, None), size=[0, 0],
                                 on_press=self.open_close_menu, pos=[WINDOW.width * .85, WINDOW.height * .6])
        button.parameter = 'inventory'
        button.text = 'inv'
        button.background_normal = 'images/maps/menu_buttons/inventory_menu_button.png'
        button.background_down = 'images/maps/menu_buttons/inventory_menu_button_down.png'
        button.bind(on_release=self.inventory.open)
        self.menu_buttons.append(button)

        button = ParameterButton(text='', size_hint=(None, None), size=[0, 0],
                                 on_press=self.open_close_menu, pos=[WINDOW.width * .85, WINDOW.height * .5])
        button.parameter = 'characters'
        button.background_normal = 'images/maps/menu_buttons/characters_menu_button.png'
        button.background_down = 'images/maps/menu_buttons/characters_menu_button_down.png'
        self.menu_buttons.append(button)

        button = ParameterButton(text='', size_hint=(None, None), size=[0, 0],
                                 on_press=self.open_close_menu, pos=[WINDOW.width * .85, WINDOW.height * .4])
        button.parameter = 'shop'
        button.text = 'shop'
        button.background_normal = 'images/maps/menu_buttons/shop_menu_button.png'
        button.background_down = 'images/maps/menu_buttons/shop_menu_button_down.png'
        button.bind(on_release=self.screenstore.open)
        self.menu_buttons.append(button)

        button = ParameterButton(text='', size_hint=(None, None), size=[0, 0],
                                 on_press=self.open_close_menu, pos=[WINDOW.width * .85, WINDOW.height * .3])
        button.parameter = 'exit'
        button.text = '<<Back'
        button.background_normal = 'images/maps/menu_buttons/exit_menu_button.png'
        button.background_down = 'images/maps/menu_buttons/exit_menu_button_down.png'
        button.bind(on_release=self.dismiss)
        self.menu_buttons.append(button)

        for but in self.menu_buttons:
            but.center_x = open_close_menu_button.center_x
            self.ids.rl.add_widget(but)

    def open_dialog(self):
        self.dialog.location = self.current_location.loc_id
        self.dialog.level = '-1'

        if self.dialog.dialog_is_completed() or self.dialog.current_npc_speech == ('', ''):
            return

        self.dialog.open()

    def on_pre_open(self):
        self.is_first_open_location = True
        if self.is_treasure_hunting:
            self.locations = locations
        else:
            self.locations = locations_mine
        self.open_location()

    def on_open(self):
        self.open_dialog()

    def open_close_menu(self, instance):
        if instance.parameter == 'open':
            instance.parameter = 'close'
            instance.background_normal = 'images/maps/menu_buttons/close_menu_button.png'
            instance.background_down = 'images/maps/menu_buttons/close_menu_button.png'
            do_animation('open_close_menu_buttons', instance, [WINDOW.height / 9, WINDOW.height / 9])
            for but in self.menu_buttons:
                do_animation('open_close_menu_buttons', but, [WINDOW.height / 9, WINDOW.height / 9])
        elif instance.parameter == 'close':
            instance.parameter = 'open'
            instance.background_normal = 'images/maps/menu_buttons/open_menu_button.png'
            instance.background_down = 'images/maps/menu_buttons/open_menu_button.png'
            do_animation('open_close_menu_buttons', instance, [WINDOW.height / 12, WINDOW.height / 12])
            for but in self.menu_buttons:
                do_animation('open_close_menu_buttons', but, [0, 0])
        else:
            return

    def open_next_or_prev_location(self, instance=None):
        if instance.parameter == 'next':
            try:
                location = self.locations[self.locations.index(self.current_location) + 1]
            except IndexError:
                location = self.locations[0]
        elif instance.parameter == 'prev':
            try:
                location = self.locations[self.locations.index(self.current_location) - 1]
            except IndexError:
                location = self.locations[-1]
        else:
            location = self.current_location

        self.open_location(location)

    def open_location(self, next_location=None):

        self.current_location = next_location if next_location is not None else self.current_location

        self.coords = self.current_location.coords

        self.ids.world_background.canvas.before.clear()
        with self.ids.world_background.canvas.before:
            Rectangle(source=self.current_location.background, size=WINDOW.size, pos=self.ids.rl.pos)

        self.world_map.clear_widgets()
        for i, coord in enumerate(self.coords):
            round_button = self.current_location.round_button(text=str(i), color=(0, 0, 0, 0), center=coord)
            round_button.bind(on_release=self.play)
            round_button.round = i
            round_button.background_normal = 'images/level_pins/ne_najataya.png'
            round_button.background_down = 'images/level_pins/najataya.png'

            if self.current_location.loc_id == -1:
                if i == 0:
                    round_button.change_stars(0)
                else:
                    round_button.change_stars(0 if db.is_opened_mine_location(i) else -1)
            elif self.current_location.loc_id == 0 and i == 0:
                check = db.get_past_result(0, 0)[0]
                round_button.change_stars(0 if check == -1 else check)
            else:
                check = db.get_past_result(self.current_location.loc_id, i - 1)[0]
                if check > 0:
                    check2 = db.get_past_result(self.current_location.loc_id, i)[0]
                    round_button.change_stars(0 if check2 == -1 else check2)
                else:
                    round_button.change_stars(-1)
            self.world_map.add_widget(round_button)

        if (not self.is_first_open_location) and (next_location != 'this'):
            self.open_dialog()
        else:
            self.is_first_open_location = False

    def play(self, *l):
        try:
            current_round = self.current_location.rounds[l[0].round]
        except IndexError:
            return

        if l[0].size_lock != [0, 0]:  # Если раунд заблочен
            do_animation('its_lock', l[0])
            return

        self.cubes_game.world_map = self
        self.cubes_game.current_location = self.current_location
        self.cubes_game.current_level = current_round
        self.cubes_game.round_swipes = current_round.swipes  # Этот раунд - типо уровень. А выше round - это кнопка уровня:)
        self.cubes_game.start_game()

        self.cubes_game.open()


#######################################################
# Worlds / Locations
class SingleWorld:

    def __init__(self, **kwargs):
        self.loc_id = 0
        self.name = 'Faceless'
        self.coords = tuple((0, 0), )
        self.background = ''
        self.rounds = rounds
        self.round_button = None


# First Location
first_location = SingleWorld()
first_location.coords = [(WINDOW.width / 2.6, WINDOW.height / 6.15), (WINDOW.width / 1.55, WINDOW.height / 5.00),
                         (WINDOW.width / 1.19, WINDOW.height / 3.45), (WINDOW.width / 1.67, WINDOW.height / 2.93),
                         (WINDOW.width / 2.81, WINDOW.height / 2.65), (WINDOW.width / 3.13, WINDOW.height / 1.92),
                         (WINDOW.width / 1.57, WINDOW.height / 1.76), (WINDOW.width / 1.17, WINDOW.height / 1.55),
                         (WINDOW.width / 1.65, WINDOW.height / 1.38), (WINDOW.width / 3.00, WINDOW.height / 1.34),
                         (WINDOW.width / 4.16, WINDOW.height / 1.18), (WINDOW.width / 2.0, WINDOW.height / 1.13)]
first_location.background = 'images/maps/world_map_1.png'
first_location.round_button = Round
first_location.name = 'Первая'
first_location.loc_id = 0

# Second Location
second_location = SingleWorld()
second_location.coords = [(WINDOW.width / 2.6, WINDOW.height / 6.15), (WINDOW.width / 1.55, WINDOW.height / 5.00),
                          (WINDOW.width / 1.19, WINDOW.height / 3.45), (WINDOW.width / 1.67, WINDOW.height / 2.93),
                          (WINDOW.width / 2.81, WINDOW.height / 2.65), (WINDOW.width / 3.13, WINDOW.height / 1.92),
                          (WINDOW.width / 1.57, WINDOW.height / 1.76), (WINDOW.width / 1.17, WINDOW.height / 1.55),
                          (WINDOW.width / 1.65, WINDOW.height / 1.38), (WINDOW.width / 3.00, WINDOW.height / 1.34),
                          (WINDOW.width / 4.16, WINDOW.height / 1.18), (WINDOW.width / 2.0, WINDOW.height / 1.13)]
second_location.background = 'images/maps/world_map_2.png'
second_location.round_button = Round
second_location.name = 'Second'
second_location.loc_id = 1

# Stone mine Location
stone_mine_location = SingleWorld()
stone_mine_location.coords = [(WINDOW.width / 2.6, WINDOW.height / 6.15), (WINDOW.width / 1.55, WINDOW.height / 5.00),
                          (WINDOW.width / 1.19, WINDOW.height / 3.45), (WINDOW.width / 1.67, WINDOW.height / 2.93),
                          (WINDOW.width / 2.81, WINDOW.height / 2.65), (WINDOW.width / 3.13, WINDOW.height / 1.92),
                          (WINDOW.width / 1.57, WINDOW.height / 1.76), (WINDOW.width / 1.17, WINDOW.height / 1.55),
                          (WINDOW.width / 1.65, WINDOW.height / 1.38), (WINDOW.width / 3.00, WINDOW.height / 1.34),
                          (WINDOW.width / 4.16, WINDOW.height / 1.18), (WINDOW.width / 2.0, WINDOW.height / 1.13)]
stone_mine_location.background = 'images/maps/world_map_2.png'
stone_mine_location.round_button = Round
stone_mine_location.name = 'Stone mine'
stone_mine_location.loc_id = -1

# LOCATIONS
locations = [first_location, second_location]

locations_mine = [stone_mine_location]

###########################
WorldMap = WorldMap()
