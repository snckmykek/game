from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from global_variables import WINDOW
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.widget import Widget

from cubes_game.main import CubesGame
from cubes_game.rounds import rounds

Builder.load_file(r'world_map/main.kv')


class Round(Button):

    def __init__(self, **kwargs):
        super(Round, self).__init__(**kwargs)

        self.background_normal = 'images/ne_najataya.png'
        self.background_down = 'images/najataya.png'
        self.round = 0
        self.size = [WINDOW.width/8, WINDOW.width/8]

    def animate_round(self):
        pass


class WorldMap(ModalView):

    def __init__(self, **kwargs):
        super(WorldMap, self).__init__(**kwargs)

        self.cubes_game = CubesGame()
        self.world_map = self.ids.world_map
        self.coords = tuple()
        self.locations = locations
        self.current_location = self.locations[0]
        self.ids.rl.add_widget(
            Button(text='next', size_hint=(None, None), width=WINDOW.width / 5, height=WINDOW.height / 12,
                   on_press=self.open_location, pos_hint={'x': .8}))

    def on_pre_open(self):
        self.current_location = locations[0]
        self.open_location()

    def open_location(self, instance=None, next_location='next'):
        if next_location == 'first':
            self.current_location = self.locations[0]
        elif next_location == 'next':
            try:
                self.current_location = self.locations[self.locations.index(self.current_location) + 1]
            except IndexError:
                self.current_location = self.locations[0]

        self.coords = self.current_location.coords

        self.ids.lines.canvas.before.clear()

        with self.ids.lines.canvas.before:
            Rectangle(source=self.current_location.background, size=WINDOW.size, pos=self.ids.rl.pos)
            for i, coord in enumerate(self.coords):
                if i == 0:
                    continue
                Color(.1, .1, 1, .3)
                bezier = list([z + 25 for z in self.coords[i]])
                bezier += list([(self.coords[i][0] + self.coords[i - 1][0]) / 2 + 10 + WINDOW.width/16,
                                (self.coords[i][1] + self.coords[i - 1][1]) / 2 - 15 + WINDOW.width/16])
                bezier += list([z + 25 for z in self.coords[i - 1]])
                Line(width=WINDOW.width/60, bezier=bezier)

        with self.ids.lines.canvas.before:
            for i, coord in enumerate(self.coords):
                if i == 0 or i > 1:
                    continue
                Color(.1, .1, 1, .7)
                bezier = list([z + 25 for z in self.coords[i]])
                bezier += list([(self.coords[i][0] + self.coords[i - 1][0]) / 2 + 10 + 25,
                                (self.coords[i][1] + self.coords[i - 1][1]) / 2 - 15 + 25])
                bezier += list([z + 25 for z in self.coords[i - 1]])
                Line(width=WINDOW.width/60, bezier=bezier)

        self.world_map.clear_widgets()
        for i, coord in enumerate(self.coords):
            round_button = self.current_location.round_button(text=str(i), color=(0, 0, 0, 1), pos=coord)
            round_button.bind(on_release=self.play)
            round_button.round = i
            round_button.background_normal = 'images/ne_najataya.png'
            round_button.background_down = 'images/najataya.png'
            self.world_map.add_widget(round_button)

    def play(self, *l):
        try:
            current_round = self.current_location.rounds[l[0].round]
        except IndexError:
            return

        self.cubes_game.round_swipes = current_round.swipes  # Этот раунд - типо уровень. А выше round - это кнопка уровня:)
        self.cubes_game.start_game(current_round.cols if current_round.cols <= 10 else 5,
                                   current_round.rows if current_round.rows <= 10 else 5,
                                   current_round.swipes, colors=current_round.colors)

        self.cubes_game.open()


#######################################################
# Worlds / Locations
class SingleWorld:

    def __init__(self, **kwargs):
        self.coords = tuple((0, 0), )
        self.background = ''
        self.rounds = rounds
        self.round_button = None


# First Location
first_location = SingleWorld()
first_location.coords = [(WINDOW.width / 8, WINDOW.height * 1 / 5), (WINDOW.width * 2.5 / 6, WINDOW.height * 2 / 5),
                         (WINDOW.width / 8, WINDOW.height * 2.2 / 5), (WINDOW.width * 2.5 / 6, WINDOW.height * 3 / 5),
                         (WINDOW.width / 9, WINDOW.height * 3.2 / 5), (WINDOW.width * 3 / 6, WINDOW.height * 4 / 5),
                         (WINDOW.width / 6, WINDOW.height * 4 / 5)]
first_location.background = 'images/world_map_1.png'
first_location.round_button = Round

# Second Location
second_location = SingleWorld()
second_location.coords = [(WINDOW.width * 2 / 8, WINDOW.height * 2 / 5),
                          (WINDOW.width * 2.5 / 6, WINDOW.height * 2 / 5),
                          (WINDOW.width / 8, WINDOW.height * 2.6 / 9),
                          (WINDOW.width * 2.5 / 6, WINDOW.height * 3 / 3.5)]
second_location.background = 'images/world_map_2.png'
second_location.round_button = Round

# LOCATIONS
locations = [first_location, second_location]
