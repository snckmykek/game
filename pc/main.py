from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock

Builder.load_file('pc/main.kv')


class Computer(ModalView):

    def __init__(self, **kwargs):
        super(Computer, self).__init__(**kwargs)
        self.opacity = 0

    def on_pre_open(self):
        self.opacity = 0

    def on_open(self):
        animation = Animation(opacity=1, d=.3, t='linear')
        animation.start(self)

    def deferred_dismiss(self):
        animation = Animation(opacity=0, d=.3, t='linear')
        animation.bind(on_complete=lambda *x: self.dismiss())
        animation.start(self)


computer = Computer()
