from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock

Builder.load_file('miniature/main.kv')


class Miniature(ModalView):

    def __init__(self, **kwargs):
        super(Miniature, self).__init__(**kwargs)

        self.miniature_list = list()
        self.miniature_index = 0
        self.miniature_image = ''
        self.miniature_text = ''
        self.opacity = 0

    def on_pre_open(self):
        self.opacity = 0
        self.miniature_index = 0
        self.show_next_miniature()

    def on_open(self):
        animation = Animation(opacity=1, d=.3, t='linear')
        animation.start(self)

    def deferred_dismiss(self):
        animation = Animation(opacity=0, d=.3, t='linear')
        animation.bind(on_complete=lambda *x: self.dismiss())
        animation.start(self)

    def show_next_miniature(self):
        try:
            next_miniature = self.miniature_list[self.miniature_index]
            self.miniature_index += 1
        except IndexError:
            self.deferred_dismiss()
            return

        self.miniature_image = next_miniature['image']
        self.miniature_text = next_miniature['text']


miniature = Miniature()
