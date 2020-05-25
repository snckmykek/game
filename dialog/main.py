# from sqlite_requests import db
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.relativelayout import RelativeLayout
# from kivy.uix.button import Button
from kivy.clock import Clock
# import time
from kivy.animation import Animation

Builder.load_file(r'dialog/main.kv')


class Dialog(ModalView):

    def __init__(self, **kwargs):
        super(Dialog, self).__init__(**kwargs)

        self.stop = False
        self.queue = 0
        self.speech_list = [{'speaker': 'hero', 'position': 'left',
                             'text': 'Ошибка, код 1: пожалуйста сообщите о ней разработчику',
                             'image': 'images/heroes/hero.png'}]
        self.letter_delay = .1
        self.game_action = None

    def on_pre_open(self):
        self.ids.speech_list_field.clear_widgets()
        self.letter_delay = .05
        self.stop = False
        self.queue = 0

    def set_stop(self):
        self.stop = True

    def on_open(self):
        animation = Animation(opacity=1, d=.3, t='linear')
        animation.bind(on_complete=lambda *x: self.show_next_speech())
        animation.start(self)

    def deferred_dismiss(self):
        animation = Animation(opacity=0, d=.3, t='linear')
        animation.bind(on_complete=lambda *x: self.dismiss())
        animation.start(self)

    def show_next_speech(self):
        try:
            next_speech = self.speech_list[self.queue]
        except IndexError:
            return

        self.queue += 1

        if next_speech['position'] == 'left':
            self.ids.left_speaker.speaker_image = next_speech['image']
        elif next_speech['position'] == 'right':
            self.ids.right_speaker.speaker_image = next_speech['image']

        speech_box = self.make_speech_box(next_speech)

        Clock.schedule_once(speech_box.add_text, .05)

    def make_speech_box(self, speech):
        speech_box = SpeechBox()
        if speech['position'] == 'left':
            speech_box.size_hint_indent_left = .01
            speech_box.size_hint_indent_right = .3
        else:
            speech_box.size_hint_indent_left = .3
            speech_box.size_hint_indent_right = .01
        speech_box.dialog = self

        speech_box.txt = speech['text']

        return speech_box


class SpeechBox(BoxLayout):

    def __init__(self, **kwargs):
        super(SpeechBox, self).__init__(**kwargs)

        self.dialog = None
        self.size_hint_indent_left = .3
        self.size_hint_indent_right = .0

        self.stop = dialog.stop
        self.i = 0
        self.txt = ''

    def add_text(self, d):
        self.dialog.ids.speech_list_field.add_widget(self)
        self.ids.current_text.text = ''
        self.i = 0
        Clock.schedule_once(self.add_letter, d)

    def add_letter(self, d):
        if dialog.stop:
            self.ids.current_text.text = self.txt
            dialog.stop = False
            self.dialog.show_next_speech()
            return

        try:
            self.ids.current_text.text += self.txt[self.i]
            self.i += 1
            Clock.schedule_once(self.add_letter, d)
        except IndexError:
            self.dialog.show_next_speech()
            return


dialog = Dialog()

