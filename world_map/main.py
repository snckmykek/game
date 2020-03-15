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

from cubes_game.main import CubesGame
from cubes_game.rounds import rounds

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

        self.size_lock_default = self.size_lock.copy()


class WorldMap(ModalView):

    def __init__(self, **kwargs):
        super(WorldMap, self).__init__(**kwargs)

        self.dialog = dialog
        self.is_first_open_location = True

        self.cubes_game = CubesGame()
        self.world_map = self.ids.world_map
        self.coords = tuple()
        self.locations = locations
        self.current_location = self.locations[0]
        self.ids.rl.add_widget(
            Button(text='next', size_hint=(None, None), width=WINDOW.width / 5, height=WINDOW.height / 12,
                   on_press=self.open_location, pos_hint={'x': .8}))

    def open_dialog(self):
        self.dialog.location = self.current_location.name
        self.dialog.level = '-1'

        if self.dialog.dialog_is_completed():
            return

        self.dialog.open()

    def on_pre_open(self):
        self.is_first_open_location = True
        self.open_location(None, 'first')

    def on_open(self):
        self.open_dialog()

    def open_location(self, instance=None, next_location='next'):
        if next_location == 'first':
            self.current_location = self.locations[0]
        elif next_location == 'next':
            try:
                self.current_location = self.locations[self.locations.index(self.current_location) + 1]
            except IndexError:
                self.current_location = self.locations[0]
        elif next_location == 'this':
            pass

        self.coords = self.current_location.coords

        self.ids.lines.canvas.before.clear()
        with self.ids.lines.canvas.before:
            Rectangle(source=self.current_location.background, size=WINDOW.size, pos=self.ids.rl.pos)

        self.world_map.clear_widgets()
        for i, coord in enumerate(self.coords):
            round_button = self.current_location.round_button(text=str(i), color=(0, 0, 0, 0), center=coord)
            round_button.bind(on_release=self.play)
            round_button.round = i
            round_button.background_normal = 'images/level_pins/ne_najataya.png'
            round_button.background_down = 'images/level_pins/najataya.png'
            if i == 0:
                check = db.get_past_result(self.current_location.name, i)[3]
                round_button.change_stars(0 if check == -1 else check)
            else:
                check = db.get_past_result(self.current_location.name, i - 1)[3]
                if check > 0:
                    check2 = db.get_past_result(self.current_location.name, i)[3]
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
            self.animation_its_lock(l[0])
            return

        self.cubes_game.world_map = self
        self.cubes_game.current_location = self.current_location
        self.cubes_game.current_round = current_round
        self.cubes_game.round_swipes = current_round.swipes  # Этот раунд - типо уровень. А выше round - это кнопка уровня:)
        self.cubes_game.start_game(current_round.cols if current_round.cols <= 10 else 5,
                                   current_round.rows if current_round.rows <= 10 else 5,
                                   current_round.swipes, colors=current_round.colors)

        self.cubes_game.open()

    def animation_its_lock(self, round):
        s = round.size_lock
        anim = Animation(size_lock=[s[0] * 1.1, s[1] * 1.1], d=.1) + Animation(size_lock=round.size_lock_default, d=.1)
        anim.start(round)

    # def on_touch_down(self, touch):
    #     print([WINDOW.width / touch.pos[0], WINDOW.height / touch.pos[1]])


#######################################################
# Worlds / Locations
class SingleWorld:

    def __init__(self, **kwargs):
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

# Second Location
second_location = SingleWorld()
second_location.coords = [(WINDOW.width * 2 / 8, WINDOW.height * 2 / 5),
                          (WINDOW.width * 2.5 / 6, WINDOW.height * 2 / 5),
                          (WINDOW.width / 8, WINDOW.height * 2.6 / 9),
                          (WINDOW.width * 2.5 / 6, WINDOW.height * 3 / 3.5)]
second_location.background = 'images/maps/world_map_2.png'
second_location.round_button = Round
second_location.name = 'Second'

# LOCATIONS
locations = [first_location, second_location]
