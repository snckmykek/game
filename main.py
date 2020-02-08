import kivy

kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.clock import Clock

import random

Builder.load_file(r'mainscreen.kv')


class GameEnding(ModalView):

    def __init__(self, **kwargs):
        super(GameEnding, self).__init__(**kwargs)

        self.score = 0

    def on_pre_open(self):
        self.ids.lbl.text = 'GG! Your score is: ' + str(self.score)


class Cube(Button):

    def __init__(self, **kwargs):
        super(Cube, self).__init__(**kwargs)

        self.column = 0
        self.line = 0


class TestApp(App):

    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)

        self.ge = GameEnding()

        self.cols = 5  # Колонки
        self.rows = 5  # Столбцы
        self.swipes = 20  # Количество ходов
        # Цвета, можно добавить. Заполняются рандомно из этого списка. Пока 4 цвета.
        # self.colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (.6, .3, .8, 1)]
        self.cube_pictures = ['images/images_1.png', 'images/images_2.png', 'images/images_3.png', 'images/images_4.png']

        self.score = 0
        self.score_label = Label(text=str(self.score), size_hint_y=None, height=50, color=(1, .5, 0, 1))
        self.swipes_label = Label(text=str(self.swipes), size_hint_y=None, height=50)
        self.g = GridLayout(size_hint=(None, None), size=(100 * self.cols, 100 * self.rows + 50), cols=1)
        self.gridlayout = StencilView()
        b = BoxLayout(size_hint_y=None, height=50)
        b.add_widget(self.score_label)
        b.add_widget(self.swipes_label)
        self.g.add_widget(b)
        self.g.add_widget(self.gridlayout)

        self.objects = list()
        self.x_movement_blocked = False
        self.y_movement_blocked = False
        self.active_column = None
        self.active_line = None
        self.auto_boom = False
        self.touch_start = 0
        self.touch_blocked = False

    def end_game(self):
        self.ge.score = self.score
        self.score = 0
        self.swipes = 20
        self.build()
        self.ge.open()

    def down(self, instance, touch):
        self.active_column = instance.column
        self.active_line = instance.line
        self.touch_start = touch.ppos

    def up(self, instance, touch):
        self.auto_boom = False
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

        self._block_touch(t=.2)
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

    def boom(self, instance, *l):
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

        self._block_touch(t=.3)
        for cube in set(suicidal_cubes):
            self.score += 1 + (int(cube.text) if cube.text != '' else 0)
            cube.text = ''
            animation = Animation(size=(10, 10), d=0.15) + Animation(size=(100, 100), d=0.1)
            animation.bind(on_complete=self.change_color)
            animation.start(cube)

        if set(suicidal_cubes):
            if not self.auto_boom:
                self.swipes -= 1
                self.auto_boom = True
            self._block_touch(t=.6)
            Clock.schedule_once(self.boom, .6)
        else:
            if self.swipes <= 0:
                self.end_game()

        for boosted_cube in self.get_boosted_cube(set(suicidal_cubes)):
            if boosted_cube.text != '':
                if int(boosted_cube.text) == 5:
                    continue
                boosted_cube.text = str(int(boosted_cube.text) + 1)
            else:
                boosted_cube.text = str(1)

        self.refresh_score_label()

    def _block_touch(self, *l, t=.6):
        self.touch_blocked = True
        Clock.schedule_once(self._unblock_touch, t)

    def _unblock_touch(self, *l):
        self.touch_blocked = False

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

    def refresh_score_label(self):
        self.score_label.text = str(self.score)
        self.swipes_label.text = str(self.swipes)

    def change_color(self, animation, instance):
        instance.background_normal = self.cube_pictures[random.randint(0, len(self.cube_pictures) - 1)]

    def movement(self, instance, touch):
        if self.touch_blocked:
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

    def build(self):

        coordinates = list([tuple([x, y]) for x in (range(self.cols))] for y in (range(self.rows)))
        self.objects = list()
        for i, row in enumerate(coordinates):
            for j, coords in enumerate(row):
                button = Cube(size_hint=(None, None), size=(100, 100),
                              pos=list(map(lambda x, y: x * y, coords, (100, 100))),
                              on_touch_move=self.movement, on_touch_down=self.down, on_touch_up=self.up)
                button.background_normal = self.cube_pictures[random.randint(0, len(self.cube_pictures) - 1)]
                button.line = i
                button.column = j
                self.objects.append(button)

        self.gridlayout.clear_widgets()
        for obj in self.objects:
            self.gridlayout.add_widget(obj)

        return self.g


if __name__ == '__main__':
    TestApp().run()
