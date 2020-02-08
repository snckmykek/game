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
        self.colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (.6, .3, .8, 1)]

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

    def end_game(self):
        self.ge.score = self.score
        self.score = 0
        self.swipes = 20
        self.build()
        self.ge.open()

    def down(self, instance, touch):
        self.active_column = instance.column
        self.active_line = instance.line

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
        animation.bind(on_complete=self.after_swipe)

        # Запускается анимация на перемещение по нужным координатам для всех кубов в строке или колонке
        for but in self.objects:
            if self.y_movement_blocked:
                animation.animated_properties['pos'] = (round(but.pos[0] / but.width) * but.width, but.pos[1])
            elif self.x_movement_blocked:
                animation.animated_properties['pos'] = (
                    but.pos[0], round(but.pos[1] / but.height) * but.height)
            else:
                continue
            animation.start(but)

    def after_swipe2(self, animation, instance):
        #???????????????????????????????????????????????????????????????????????????????????
        column = instance.pos[0] / instance.width
        line = instance.pos[1] / instance.height

        new_pos = [0, 0]
        if column > self.cols - .5:
            instance.column = 0
            new_pos = ((self.cols - 1 - column) * instance.width, instance.pos[1])
        elif column < -.5:
            instance.column = self.cols - 1
            new_pos = ((self.cols - 1 - column) * instance.width, instance.pos[1])
        elif line > self.rows - .5:
            instance.line = 0
            new_pos = (instance.pos[0], (self.rows - 1 - line) * instance.height)
        elif line < -.5:
            instance.line = self.rows - 1
            new_pos = (instance.pos[0], (self.rows - 1 - line) * instance.height)
        else:
            instance.column = round(column)
            instance.line = round(line)
            return

        print(instance.column, instance.line)

        instance.pos = new_pos

        # self.gridlayout.remove_widget(instance)
        # instance.pos = new_pos
        # instance.size = (10, 10)
        # self.gridlayout.add_widget(instance)
        # animation = Animation(size=(100, 100), pos=instance.pos, d=0.1)
        # animation.start(instance)

    def after_swipe(self, animation, instance):
        # instance.column = instance.pos[0] / instance.width
        # instance.line = instance.pos[1] / instance.height
        #
        # if instance.column > self.cols - 1:
        #     instance.column = 0
        # elif instance.column < 0:
        #     instance.column = self.cols - 1
        # elif instance.line > self.rows - 1:
        #     instance.line = 0
        # elif instance.line < 0:
        #     instance.line = self.rows - 1
        # else:
        #     return
        #
        # self.gridlayout.remove_widget(instance)
        # instance.size = (10, 10)
        # instance.pos = (instance.column * 100, instance.line * 100)
        # self.gridlayout.add_widget(instance)
        # animation = Animation(size=(100, 100), pos=instance.pos, d=0.1)
        # animation.start(instance)
        # animation.bind(on_complete=
        self.boom(animation, instance)

    def boom(self, animation, instance):
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

        for cube in set(suicidal_cubes):
            self.score += 1 + (int(cube.text) if cube.text != '' else 0)
            cube.text = ''
            animation = Animation(size=(10, 10), d=0.2) + Animation(size=(100, 100), d=0.1)
            animation.bind(on_complete=self.change_color)
            animation.start(cube)

        if set(suicidal_cubes):  # Перепилить на просто отложенный вызов
            if not self.auto_boom:
                self.swipes -= 1
                self.auto_boom = True
            anim = Animation(d=.4)
            anim.bind(on_complete=self.boom)
            anim.start(cube)
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
        instance.background_color = self.colors[random.randint(0, len(self.colors) - 1)]

    def movement(self, instance, touch):
        if abs(touch.dx) > abs(touch.dy):
            if (instance.center_x - instance.width / 2) < touch.pos[0] < (instance.center_x + instance.width / 2) \
                    and instance.line == self.active_line and not self.x_movement_blocked:
                self.y_movement_blocked = True
                for but in self.objects:
                    if but.line == instance.line:
                        but.pos[0] += touch.dx / 2
                        self.after_swipe2('animation', but)
        elif abs(touch.dx) < abs(touch.dy):
            if (instance.center_y - instance.height / 2) < touch.pos[1] < (instance.center_y +
                    instance.height / 2) and instance.column == self.active_column and not self.y_movement_blocked:
                self.x_movement_blocked = True
                for but in self.objects:
                    if but.column == instance.column:
                        but.pos[1] += touch.dy / 2
                        self.after_swipe2('animation', but)

    def build(self):

        coordinates = list([tuple([x, y]) for x in (range(self.cols))] for y in (range(self.rows)))
        self.objects = list()
        for i, row in enumerate(coordinates):
            for j, coords in enumerate(row):
                button = Cube(size_hint=(None, None), size=(100, 100),
                              pos=list(map(lambda x, y: x * y, coords, (100, 100))),
                              on_touch_move=self.movement, on_touch_down=self.down, on_touch_up=self.up)
                button.background_color = self.colors[random.randint(0, len(self.colors) - 1)]
                button.line = i
                button.column = j
                self.objects.append(button)

        self.gridlayout.clear_widgets()
        for obj in self.objects:
            self.gridlayout.add_widget(obj)

        return self.g


if __name__ == '__main__':
    TestApp().run()
