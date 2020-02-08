import kivy

kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from functools import partial
from kivy.uix.stencilview import StencilView


class Cube(Button):

    def __init__(self, **kwargs):
        super(Cube, self).__init__(**kwargs)

        self.column = 0
        self.line = 0


class TestApp(App):

    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)

        self.cols = 3
        self.rows = 3
        self.g = GridLayout(size_hint=(None, None), size=(300, 300), cols=1)
        self.gridlayout = StencilView(size=(300, 300))
        self.g.add_widget(self.gridlayout)

        self.objects = list()
        self.x_movement_blocked = False
        self.y_movement_blocked = False
        self.active_column = None
        self.active_line = None

    def down(self, instance, touch):
        self.active_column = instance.column
        self.active_line = instance.line

    def up(self, instance, touch):
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
                # if but.line == instance.line:
                animation.animated_properties['pos'] = (round(but.pos[0] / instance.width) * instance.width, but.pos[1])
                # else:
                #     continue
            elif self.x_movement_blocked:
                # if but.column == instance.column:
                animation.animated_properties['pos'] = (but.pos[0], round(but.pos[1] / instance.height) * instance.height)
                # else:
                #     continue
            else:
                continue
            animation.start(but)

    def after_swipe(self, animation, instance):
        pass
        # if (instance.pos[0] + instance.width) // instance.width * instance.width > self.gridlayout.pos[0] \
        #         + self.gridlayout.width:
        #     self.gridlayout.remove_widget(instance)
        #     button = Button(size_hint=(None, None), size=(10, 10),
        #                     center_x=instance.center_x - instance.width * self.cols, center_y=instance.center_y,
        #                     text='plop ' + str('new'), on_touch_move=self.animate, on_release=self.test)
        #
        #     instance.size = (10, 10)
        #     instance.pos = (50, 50)
        #     instance.center_x = instance.center_x - instance.width * self.cols
        #
        #     self.gridlayout.add_widget(instance)
        #     animation = Animation(size=(100, 100), pos=(0, 0),
        #                           d=0.1)
        #     animation.start(instance)

    def movement(self, instance, touch):
        # print(touch.dx, touch.dy)
        if abs(touch.dx) > abs(touch.dy):
            if (instance.center_x - instance.width / 2) < touch.pos[0] < (instance.center_x + instance.width / 2) \
                    and instance.line == self.active_line and not self.x_movement_blocked:
                self.y_movement_blocked = True
                for but in self.objects:
                    if but.line == instance.line:
                        but.pos[0] += touch.dx/2
        elif abs(touch.dx) < abs(touch.dy):
            if (instance.center_y - instance.height / 2) < touch.pos[1] < (instance.center_y +
                    instance.height / 2) and instance.column == self.active_column \
                    and not self.y_movement_blocked:
                self.x_movement_blocked = True
                for but in self.objects:
                    if but.column == instance.column:
                        but.pos[1] += touch.dy/2

    def test(self, instance):
        # self.gridlayout.remove_widget(self.gridlayout.children[1])
        # button = Button(size_hint=(None, None), text='plop_new',
        #                 on_touch_move=self.animate, on_release=self.test)
        # self.gridlayout.children[2] = button
        pass

    def build(self):

        coordinates = [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)]
        ]

        for i, row in enumerate(coordinates):
            for j, coords in enumerate(row):
                button = Cube(size_hint=(None, None), size=(100, 100),
                              pos=list(map(lambda x, y: x * y, coords, (100, 100))),
                              text='plop ' + str(i) + ", " + str(j),
                              on_touch_move=self.movement, on_release=self.test,
                              on_touch_down=self.down, on_touch_up=self.up)
                button.line = i
                button.column = j
                self.objects.append(button)

        for obj in self.objects:
            self.gridlayout.add_widget(obj)

        return self.g

    # Работа со структурой Кубов
    def get_coords(self, instance):
        coords = tuple()
        for row in self.objects:
            for d in row:
                pass


if __name__ == '__main__':
    TestApp().run()
