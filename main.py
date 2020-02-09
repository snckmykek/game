import kivy

kivy.require('1.0.7')

from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.clock import Clock
from global_variables import WINDOW

import random

Builder.load_file(r'mainscreen.kv')


class Menu(BoxLayout):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

        self.cubes_game = CubesGame()

    def play(self):
        self.cubes_game.open()


class CubesGame(ModalView):

    def __init__(self, ** kwargs):
        super(CubesGame, self).__init__(**kwargs)

        self.ge = GameEnding()

        self.cols = 5  # Колонки
        self.rows = 5  # Столбцы
        self.swipes = 20  # Количество ходов
        self.cube_pictures = ['images/images_1.png', 'images/images_2.png', 'images/images_3.png', 'images/images_4.png']

        self.a = WINDOW.width / (self.cols + 1)
        self.score = 0
        self.score_label = self.ids.score_label
        self.swipes_label = self.ids.swipes_label
        self.update_status_board()
        self.playing_field = self.ids.playing_field
        # self.playing_field.size = (self.a * self.cols, self.a * self.rows)
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)
        self.starting_point = None

        self.objects = list()
        self.x_movement_blocked = False
        self.y_movement_blocked = False
        self.active_column = None
        self.active_line = None
        self.touch_start = (0, 0)
        self.touch_blocked = False
        self.touch_is_down = False

    def on_pre_open(self):
        self.start_game()

    def end_game(self, *l):
        self.ge.score = self.score
        self.ge.game = self
        self.score = 0
        self.swipes = 20
        self.ge.open()

    def down(self, instance, touch):
        self.active_column = instance.column
        self.active_line = instance.line
        self.touch_start = touch.ppos

        self.touch_is_down = True

        if not self.starting_point:  # Чтобы знать, откуда начал двигать, и если чо, вернуться обратно
            self.starting_point = StartingPoint()
            self.starting_point.pos = [s - self.starting_point.width / 2 for s in touch.pos]
            self.playing_field.add_widget(self.starting_point)

    def up(self, instance, touch):
        if self.starting_point:
            self.playing_field.remove_widget(self.starting_point)
            self.starting_point = None

        if (abs(touch.pos[0] - self.touch_start[0]) > instance.width / 2) \
                or (abs(touch.pos[1] - self.touch_start[1]) > instance.width / 2):
            if self.touch_is_down and not self.touch_blocked:
                self.swipes -= 1
        self.touch_is_down = False

        x = instance.center_x - instance.width / 2
        x2 = instance.center_x + instance.width / 2
        y = instance.center_y - instance.height / 2
        y2 = instance.center_y + instance.height / 2
        if (x < touch.pos[0] < x2 and self.y_movement_blocked) or (y < touch.pos[1] < y2 and self.x_movement_blocked):
            self.active_column = None
            self.active_line = None
            self._move_line(instance, touch)
            self.x_movement_blocked = False
            self.y_movement_blocked = False

    def _move_line(self, instance, touch, *l):

        animation = Animation(d=0.1, pos=(0, 0))

        self.touch_blocked = True
        # Запускается анимация на перемещение по нужным координатам для всех кубов в строке или колонке
        for but in self.objects:
            if self.y_movement_blocked:
                but.column = round(but.pos[0] / but.width)
                animation.animated_properties['pos'] = (but.column * but.width, but.pos[1])
            elif self.x_movement_blocked:
                but.line = round(but.pos[1] / but.height)
                animation.animated_properties['pos'] = (but.pos[0], but.line * but.height)
            else:
                continue
            animation.start(but)
        Clock.schedule_once(self.boom, .2)

    def boom(self, instance=None, *l):
        suicidal_cubes = list()

        for obj in self.objects:
            obj_prev_x = None
            obj_next_x = None
            obj_prev_y = None
            obj_next_y = None
            for o in self.objects:
                if o.line == obj.line:
                    if o.column == obj.column - 1:
                        obj_prev_x = o
                    if o.column == obj.column + 1:
                        obj_next_x = o
                if o.column == obj.column:
                    if o.line == obj.line - 1:
                        obj_prev_y = o
                    if o.line == obj.line + 1:
                        obj_next_y = o

            if obj_prev_x and obj_next_x:
                if (obj.background_normal == obj_prev_x.background_normal) \
                        and (obj.background_normal == obj_next_x.background_normal):
                    suicidal_cubes.extend([obj, obj_prev_x, obj_next_x])
            if obj_prev_y and obj_next_y:
                if (obj.background_normal == obj_prev_y.background_normal) \
                        and (obj.background_normal == obj_next_y.background_normal):
                    suicidal_cubes.extend([obj, obj_prev_y, obj_next_y])

        self.touch_blocked = True
        for cube in set(suicidal_cubes):
            self.score += 1 + (int(cube.text) if cube.text != '' else 0)
            cube.text = ''
            animation = Animation(size=(10, 10), d=0.15) + Animation(size=(self.a, self.a), d=0.1)
            animation.bind(on_complete=self.change_color)
            animation.start(cube)

        if set(suicidal_cubes):
            Clock.schedule_once(self.boom, .6)
        else:
            self.touch_blocked = False
            if self.swipes <= 0:
                Clock.schedule_once(self.end_game, .3)

        for boosted_cube in self.get_boosted_cube(set(suicidal_cubes)):
            if boosted_cube.text != '':
                if int(boosted_cube.text) == 5:
                    continue
                boosted_cube.text = str(int(boosted_cube.text) + 1)
            else:
                boosted_cube.text = str(1)

        self.update_status_board()

    def get_boosted_cube(self, cubes):
        boosted_cubes = list()
        for obj in cubes:
            obj_prev_x = None
            obj_next_x = None
            obj_prev_y = None
            obj_next_y = None
            for o in self.objects:
                if o.line == obj.line:
                    if o.column == obj.column - 1:
                        boosted_cubes.append(o)
                    if o.column == obj.column + 1:
                        boosted_cubes.append(o)
                if o.column == obj.column:
                    if o.line == obj.line - 1:
                        boosted_cubes.append(o)
                    if o.line == obj.line + 1:
                        boosted_cubes.append(o)

        return set(boosted_cubes) - cubes

    def update_status_board(self):
        self.score_label.text = str(self.score)
        self.swipes_label.text = str(self.swipes)

    def change_color(self, animation, instance):
        instance.background_normal = self.cube_pictures[random.randint(0, len(self.cube_pictures) - 1)]
        instance.background_down = instance.background_normal

    def movement(self, instance, touch):
        if self.touch_blocked:
            return

        if not self.playing_field.collide_point(*touch.pos):
            return

        if abs(touch.dx) > abs(touch.dy):
            if (instance.center_x - instance.width / 2) < touch.pos[0] < (instance.center_x + instance.width / 2) \
                    and instance.line == self.active_line and not self.x_movement_blocked:
                self.y_movement_blocked = True
                for but in self.objects:
                    if but.line == instance.line:
                        new_pos_x = (touch.pos[0] - self.touch_start[0]) + but.column * but.width
                        if new_pos_x > self.cols * but.width - but.width / 2:
                            new_pos_x -= self.cols * but.width
                        elif new_pos_x < - but.width / 2:
                            new_pos_x += self.cols * but.width
                        but.pos[0] = new_pos_x
        elif abs(touch.dx) < abs(touch.dy):
            if (instance.center_y - instance.height / 2) < touch.pos[1] < (instance.center_y +
                                                                           instance.height / 2) and instance.column == self.active_column and not self.y_movement_blocked:
                self.x_movement_blocked = True
                for but in self.objects:
                    if but.column == instance.column:
                        new_pos_y = (touch.pos[1] - self.touch_start[1]) + but.line * but.height
                        if new_pos_y > self.rows * but.height - but.height / 2:
                            new_pos_y -= self.rows * but.height
                        elif new_pos_y < - but.height / 2:
                            new_pos_y += self.rows * but.height
                        but.pos[1] = new_pos_y

    def start_game(self):
        self.swipes = 20
        self.score = 0
        self.update_status_board()

        coordinates = list([tuple([x, y]) for x in (range(self.cols))] for y in (range(self.rows)))
        self.objects = list()
        for i, row in enumerate(coordinates):
            for j, coords in enumerate(row):
                button = Cube(size_hint=(None, None), size=(self.a, self.a),
                              pos=list(map(lambda x, y: x * y, coords, (self.a, self.a))),
                              on_touch_move=self.movement, on_touch_down=self.down, on_touch_up=self.up)
                button.background_normal = self.cube_pictures[random.randint(0, len(self.cube_pictures) - 1)]
                button.background_down = button.background_normal
                button.line = i
                button.column = j
                self.objects.append(button)

        self.playing_field.clear_widgets()
        for obj in self.objects:
            self.playing_field.add_widget(obj)

        # Сделать так, чтобы при старте уже не было 3 в ряд не взорвавшихся
        # Не работает, тк в буме есть отложенные события. Потом сделать кек
        # self.boom()
        # self.score = 0
        # self.update_status_board()


class GameEnding(ModalView):

    def __init__(self, **kwargs):
        super(GameEnding, self).__init__(**kwargs)

        self.score = 0
        self.game = ''

    def on_pre_open(self):
        self.ids.lbl.text = 'GG! Your score is: ' + str(self.score)

    def on_pre_dismiss(self):
        self.game.start_game()


class Cube(Button):

    def __init__(self, **kwargs):
        super(Cube, self).__init__(**kwargs)

        self.column = 0
        self.line = 0


class StartingPoint(Label):

    def __init__(self, **kwargs):
        super(StartingPoint, self).__init__(**kwargs)

        self.size = (WINDOW.width / 20, WINDOW.width / 20)


class CubesApp(App):

    def __init__(self, **kwargs):
        super(CubesApp, self).__init__(**kwargs)

    def build(self):
        return Menu()


if __name__ == '__main__':
    CubesApp().run()
