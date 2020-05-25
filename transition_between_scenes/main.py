from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.animation import Animation

Builder.load_file('transition_between_scenes/main.kv')


class Transition(ModalView):

    def __init__(self, **kwargs):
        super(Transition, self).__init__(**kwargs)

        self.current_opacity = 0
        self.func = None

    def on_pre_open(self):
        self.current_opacity = 0

    def on_open(self):
        animation = Animation(current_opacity=.5, d=.25, t='linear') + Animation(current_opacity=0, d=.25, t='linear')
        animation.bind(on_complete=lambda *x: self.continue_animation())
        animation.start(self)
        self.func()

    def continue_animation(self):
        # self.func()
        self.dismiss()
