from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock

Builder.load_file('information/main.kv')


class Information(ModalView):

    def __init__(self, **kwargs):
        super(Information, self).__init__(**kwargs)

        self.information = dict()
        self.information_index = 0
        self.information_image = ''
        self.information_text = ''
        self.opacity = 0
        self.label_background = ''
        self.information_text = ''

    def on_pre_open(self):
        self.opacity = 0
        self.information_index = 0
        self.label_background = self.information['background']
        self.information_text = self.information['text']

    def on_open(self):
        animation = Animation(opacity=1, d=.3, t='linear')
        animation.start(self)

    def deferred_dismiss(self):
        animation = Animation(opacity=0, d=.3, t='linear')
        animation.bind(on_complete=lambda *x: self.dismiss())
        animation.start(self)


information = Information()
