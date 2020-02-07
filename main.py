import kivy
kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from functools import partial
from kivy.uix.stencilview import StencilView


class TestApp(App):

    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)

        self.cols = 3
        self.rows = 3
        self.g = GridLayout(size=(300, 300))
        self.gridlayout = StencilView(size=(300, 300))
        self.g.add_widget(self.gridlayout)

        self.blocked_move = False

    def on_touch_down(self):
        start

    def _move_line(self, instance, touch, direction, *l):

        if direction == 'horizontal':
            if touch.dx > 0:
                animation = Animation(pos=((instance.pos[0] + instance.width)//instance.width*instance.width, instance.pos[1]),
                                      d=0.1)
            else:
                animation = Animation(pos=((instance.pos[0] - instance.width)//instance.width*instance.width, instance.pos[1]), d=0.1)
        else:  # direction == 'vertical':
            if touch.dy > 0:
                animation = Animation(pos=(instance.pos[0], (instance.pos[1] + instance.height)//instance.height*instance.height), d=0.1)
            else:
                animation = Animation(pos=(instance.pos[0], (instance.pos[1] - instance.height)//instance.height*instance.height), d=0.1)

        animation.bind(on_complete=self.after_swipe)
        animation.start(instance)

    def after_swipe(self, animation, instance):
        if (instance.pos[0] + instance.width)//instance.width*instance.width > self.gridlayout.pos[0] + self.gridlayout.width:
            self.gridlayout.remove_widget(instance)
            button = Button(size_hint=(None, None), size=(10, 10),
                            center_x=instance.center_x - instance.width*self.cols, center_y=instance.center_y,
                            text='plop ' + str('new'), on_touch_move=self.animate, on_release=self.test)

            instance.size = (10, 10)
            instance.pos = (50, 50)
            instance.center_x = instance.center_x - instance.width*self.cols

            self.gridlayout.add_widget(instance)
            animation = Animation(size=(100, 100), pos=(0, 0),
                                  d=0.1)
            animation.start(instance)

    def animate(self, instance, touch):
        if abs(touch.dx) > 10 and abs(touch.dx) > abs(touch.dy):
            if (instance.center_x - instance.width / 2) < touch.pos[0] < (instance.center_x + instance.width / 2) \
                    and (instance.center_y - instance.height / 2) < touch.pos[1] < (instance.center_y + instance.height / 2):
                for button in self.gridlayout.children:
                    if button.center_y == instance.center_y:
                        self._move_line(button, touch, 'horizontal')
                        # Clock.schedule_once(partial(self._move_line, button, touch, 'horizontal'), 0.1)

        if abs(touch.dy) > 10 and abs(touch.dx) < abs(touch.dy):
            if (instance.center_x - instance.width / 2) < touch.pos[0] < (instance.center_x + instance.width / 2) \
                    and (instance.center_y - instance.height / 2) < touch.pos[1] < (instance.center_y + instance.height / 2):
                for button in self.gridlayout.children:
                    if button.center_x == instance.center_x:
                        self._move_line(button, touch, 'vertical')
                        # Clock.schedule_once(partial(self._move_line, button, touch, 'vertical'), 0.1)

    def test(self, instance):
        # self.gridlayout.remove_widget(self.gridlayout.children[1])
        # button = Button(size_hint=(None, None), text='plop_new',
        #                 on_touch_move=self.animate, on_release=self.test)
        # self.gridlayout.children[2] = button
        pass

    def build(self):

        coordinates = [
                        [(50, 50), (150, 50), (250, 50)],
                        [(50, 150), (150, 150), (250, 150)],
                        [(50, 250), (150, 250), (250, 250)]
                       ]

        objects = list()

        for i, row in enumerate(coordinates):
            objects.append(list())
            for j, coord in enumerate(row):
                button = Button(size_hint=(None, None), size=(100, 100), center_x=coord[0],
                                center_y=coord[1], text='plop ' + str(i) + ", " + str(j),
                                on_touch_move=self.animate, on_release=self.test)
                objects[i].append(button)

        for row in objects:
            for obj in row:
                self.gridlayout.add_widget(obj)

        return self.g


if __name__ == '__main__':
    TestApp().run()