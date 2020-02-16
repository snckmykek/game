from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from global_variables import WINDOW
from sqlite_requests import db

from dialog.main import dialog

import math
import random

Builder.load_file(r'cubes_game/main.kv')


class CubesGame(ModalView):

    def __init__(self, **kwargs):
        super(CubesGame, self).__init__(**kwargs)

        self.ge = GameEnding()
        self.dialog = dialog

        self.world_map = ObjectProperty
        self.current_round = ObjectProperty
        self.current_location = ObjectProperty
        self.cols = 4  # Колонки
        self.rows = 4  # Столбцы
        self.swipes = 20  # Количество ходов
        self.round_swipes = 20  # Это число не меняется в процессе игры (только при запуске) и при перезапуске используется
        self.colors = 4  # Цветов в раунде
        self.cube_colors = [(1, 0, 0, 1), (0, 1, 0, 1), (.3, .88, .9, 1), (.8, 0, .87, 1), (.9, .5, 0, 1)]

        self.a = WINDOW.width / (self.cols + 1)
        self.score = 0
        self.score_label = self.ids.score_label
        self.swipes_label = self.ids.swipes_label
        self.update_status_board()
        self.playing_field = self.ids.playing_field
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)
        self.cube_pattern = 'images/pattern.png'

        self.objects = list()
        self.background_objects = list()
        self.prizes = list()
        self.x_movement_blocked = False
        self.y_movement_blocked = False
        self.active_column = list()
        self.active_line = list()
        self.touch_start = (0, 0)
        self.touch_blocked = False
        self.touch_is_down = False
        self.forced_up = False
        self.starting_point = None  # Чтобы знать, откуда начал двигать, и если чо, вернуться обратно

    def on_open(self):
        self.dialog.location = self.current_location.name
        self.dialog.level = self.current_round.name
        self.dialog.open()

    def on_pre_dismiss(self):
        self.world_map.open_location(next_location='this')

    def end_game(self, *l):
        self.ge.score = self.score
        self.ge.game = self
        self.ge.open()

    def down(self, instance, touch):
        if self.touch_blocked:
            return

        if not instance.collide_point(*touch.pos):
            return

        self.active_column.clear()
        self.active_line.clear()
        for cube in self.objects:
            if cube.column == instance.column:
                self.active_column.append(cube)
            if cube.line == instance.line:
                self.active_line.append(cube)

        self.touch_start = touch.ppos

        self.touch_is_down = True
        self.forced_up = False

        if not self.starting_point:
            self.starting_point = StartingPoint()
            self.starting_point.pos = [s - self.starting_point.width / 2 for s in touch.pos]
            self.playing_field.add_widget(self.starting_point)

    def up(self, instance, touch):
        if self.touch_blocked:
            return

        if self.starting_point:
            self.playing_field.remove_widget(self.starting_point)
            self.starting_point = None

        if ((abs(touch.pos[0] - self.touch_start[0]) > instance.width / 2) and self.y_movement_blocked) \
                or ((abs(touch.pos[1] - self.touch_start[1]) > instance.width / 2) and self.x_movement_blocked):
            if self.touch_is_down and not self.touch_blocked:
                self.swipes -= 1
        self.touch_is_down = False

        if self.y_movement_blocked or self.x_movement_blocked \
                or (not self.playing_field.collide_point(*touch.pos) and not self.forced_up):
            self.forced_up = True
            self._move_line(instance, touch)
            self.x_movement_blocked = False
            self.y_movement_blocked = False

    def _move_line(self, instance, touch, *l):

        animation = Animation(d=0.1, pos=(0, 0))

        self.touch_blocked = True
        # Запускается анимация на перемещение по нужным координатам для всех кубов в строке или колонке
        is_rounding_up = None  # Эта наркомания обусловлена тем, что бывает подвисают координаты кнопок
        # и соседние кнопки разъезжаются в разные стороны
        if self.y_movement_blocked:
            for but in self.active_line:
                if is_rounding_up is None:
                    is_rounding_up = round(but.pos[0] / but.width) == math.ceil(but.pos[0] / but.width)
                but.column = math.ceil(but.pos[0] / but.width) if is_rounding_up else math.floor(but.pos[0] / but.width)
                animation.animated_properties['pos'] = (but.column * but.width, but.pos[1])
                animation.start(but)
        elif self.x_movement_blocked:
            for but in self.active_column:
                if is_rounding_up is None:
                    is_rounding_up = round(but.pos[1] / but.height) == math.ceil(but.pos[1] / but.height)
                but.line = math.ceil(but.pos[1] / but.height) if is_rounding_up else math.floor(but.pos[1] / but.height)
                animation.animated_properties['pos'] = (but.pos[0], but.line * but.height)
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
                if (obj.background_color == obj_prev_x.background_color) \
                        and (obj.background_color == obj_next_x.background_color):
                    suicidal_cubes.extend([obj, obj_prev_x, obj_next_x])
            if obj_prev_y and obj_next_y:
                if (obj.background_color == obj_prev_y.background_color) \
                        and (obj.background_color == obj_next_y.background_color):
                    suicidal_cubes.extend([obj, obj_prev_y, obj_next_y])

        self.touch_blocked = True
        for cube in set(suicidal_cubes):
            self.score += 1 + (int(cube.text) if cube.text != '' else 0)
            cube.text = ''
            animation = Animation(size=(10, 10), d=0.15) + Animation(size=(self.a, self.a), d=0.1)
            animation.bind(on_complete=self.change_color)
            animation.start(cube)

        copy_background_objects = self.background_objects.copy()
        for background_obj in copy_background_objects:
            for cube in set(suicidal_cubes):
                if (background_obj.column == cube.column) and (background_obj.line == cube.line):
                    self.background_objects.remove(background_obj)
                    self.playing_field.remove_widget(background_obj)

        copy_prizes = self.prizes.copy()
        for prize in copy_prizes:
            take_prize = True
            for background_obj in self.background_objects:
                if (background_obj.column in prize.column) and (background_obj.line in prize.line):
                    take_prize = False
            if take_prize:
                self.playing_field.remove_widget(prize)
                self.ids.rl.add_widget(prize)
                self.prizes.remove(prize)
                animation = Animation(size=(prize.size[0] * 1.2, prize.size[1] * 1.2), d=.4)
                animation += Animation(size=prize.size, d=.4)
                animation += Animation(size=(10, 10), d=.8)
                animation &= Animation(pos=(self.ids.bonus_1.center_x, self.ids.bonus_1.center_y), d=1.3)
                animation.bind(on_complete=self.delete_prize)
                animation.start(prize)

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

    def delete_prize(self, animation, instance):
        self.ids.rl.remove_widget(instance)

    def get_boosted_cube(self, cubes):
        boosted_cubes = list()
        for obj in cubes:
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
        instance.background_color = self.cube_colors[random.randint(0, self.colors - 1)]

    def movement(self, instance, touch):
        if self.touch_blocked or not self.touch_is_down:
            return

        if not self.playing_field.collide_point(*touch.pos):
            self.up(instance, touch)
            return

        if (abs(touch.dx) > abs(touch.dy)) or self.y_movement_blocked:
            if (instance in self.active_line) and not self.x_movement_blocked:
                self.y_movement_blocked = True
                for but in self.active_line:
                    new_pos_x = (touch.pos[0] - self.touch_start[0]) + but.column * but.width
                    if new_pos_x > self.cols * but.width - but.width / 2:
                        new_pos_x -= self.cols * but.width
                    elif new_pos_x < - but.width / 2:
                        new_pos_x += self.cols * but.width
                    but.pos[0] = new_pos_x

        if (abs(touch.dx) < abs(touch.dy)) or self.x_movement_blocked:
            if (instance in self.active_column) and not self.y_movement_blocked:
                self.x_movement_blocked = True
                for but in self.active_column:
                    new_pos_y = (touch.pos[1] - self.touch_start[1]) + but.line * but.height
                    if new_pos_y > self.rows * but.height - but.height / 2:
                        new_pos_y -= self.rows * but.height
                    elif new_pos_y < - but.height / 2:
                        new_pos_y += self.rows * but.height
                    but.pos[1] = new_pos_y

    def start_game(self, cols=5, rows=5, swipes=20, cubes=None, colors=4):
        self.cols = cols
        self.rows = rows
        self.swipes = swipes
        self.colors = colors
        self.a = WINDOW.width / ((self.cols if self.cols >= self.rows else self.rows) + 1)
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)
        if cubes:
            pass  # stub
        self.score = 0
        self.update_status_board()

        coordinates = list([tuple([x, y]) for x in (range(self.cols))] for y in (range(self.rows)))
        self.objects = list()
        for i, row in enumerate(coordinates):
            for j, coords in enumerate(row):
                button = Cube(size_hint=(None, None), size=(self.a, self.a),
                              pos=list(map(lambda x, y: x * y, coords, (self.a, self.a))),
                              on_touch_move=self.movement, on_touch_down=self.down, on_touch_up=self.up)
                button.background_color = self.cube_colors[random.randint(0, self.colors - 1)]
                button.background_normal = self.cube_pattern
                button.background_down = self.cube_pattern
                button.line = i
                button.column = j
                self.objects.append(button)

        self.ids.text_round.text = self.current_round.text_round

        # coordinates_background_objects = [[(0, 0), (1, 0)],
        #                                   [(0, 1), (1, 1)]
        #                                   ]
        # self.background_objects = list()
        # for i, row in enumerate(coordinates_background_objects):
        #     for j, coords in enumerate(row):
        #         button = Cube(size_hint=(None, None), size=(self.a, self.a),
        #                       pos=list(map(lambda x, y: x * y, coords, (self.a, self.a))))
        #         button.line = i
        #         button.column = j
        #         button.background_normal = ''
        #         button.background_color = (.82, .93, .51, 1)
        #         self.background_objects.append(button)
        #
        # self.prizes = list()
        # button = Cube(size_hint=(None, None), size=(self.a*2, self.a*2), pos=(0, 0))
        # button.column = [0, 1]
        # button.line = [0, 1]
        # self.prizes.append(button)
        #
        self.playing_field.clear_widgets()
        # for obj in self.prizes:
        #     self.playing_field.add_widget(obj)
        # for obj in self.background_objects:
        #     self.playing_field.add_widget(obj)
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
        self.game = ObjectProperty

    def on_pre_open(self):
        self.ids.lbl.text = 'GG! Your score is: ' + str(self.score)

    def on_pre_dismiss(self):
        db.insert_completed_level(self.game.current_location.name, self.game.current_round.name)

    def play_again(self):
        self.game.start_game(cols=self.game.cols,
                             rows=self.game.rows,
                             swipes=self.game.round_swipes,
                             colors=self.game.colors)
        self.dismiss()

    def exit_level(self):
        self.dismiss()
        self.game.dismiss()


class Cube(Button):

    def __init__(self, **kwargs):
        super(Cube, self).__init__(**kwargs)

        self.column = 0
        self.line = 0


class StartingPoint(Label):

    def __init__(self, **kwargs):
        super(StartingPoint, self).__init__(**kwargs)

        self.size = (WINDOW.width / 20, WINDOW.width / 20)
