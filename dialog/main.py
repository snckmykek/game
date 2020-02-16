from sqlite_requests import db
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

Builder.load_file(r'dialog/main.kv')


class PlayerSpeechBox(BoxLayout):

    def __init__(self, **kwargs):
        super(PlayerSpeechBox, self).__init__(**kwargs)


class NPCSpeechBox(RelativeLayout):

    def __init__(self, **kwargs):
        super(NPCSpeechBox, self).__init__(**kwargs)


class PlayerSpeechButton(Button):

    def __init__(self, **kwargs):
        super(PlayerSpeechButton, self).__init__(**kwargs)

        self.speech = tuple()


class Dialog(ModalView):

    def __init__(self, **kwargs):
        super(Dialog, self).__init__(**kwargs)

        self.all_player_speech = list()
        self.lang = ''
        self.npc_image = ''
        self.npc_name = ''
        self.current_player_speech = tuple(['', ''])  # number, text
        self.current_npc_speech = tuple(['', ''])  # number, text
        self.location = ''
        self.level = ''

        self.current_speaker_is_player = False
        self.content_box = self.ids.content_box
        self.player_speech_box = PlayerSpeechBox()
        self.npc_speech_box = NPCSpeechBox()
        self.npc_speech_box.ids.but.bind(on_press=self.npc_said)

    def on_pre_open(self):
        self.current_player_speech = tuple(['', ''])
        self.current_speaker_is_player = False
        self.refresh_speech_box()

    def refresh_speech_box(self):
        db.fill_speech(self)

        self.content_box.clear_widgets()
        if self.current_speaker_is_player:
            self.player_speech_box.clear_widgets()
            for sp in self.all_player_speech:
                psb = PlayerSpeechButton(text=sp[1], on_press=self.player_said)
                psb.speech = sp
                self.player_speech_box.add_widget(psb)
            self.content_box.add_widget(self.player_speech_box)
        else:
            self.npc_speech_box.ids.speech.text = self.current_npc_speech[1]
            self.content_box.add_widget(self.npc_speech_box)

        self.current_speaker_is_player = not self.current_speaker_is_player

    def player_said(self, instance):
        self.current_player_speech = instance.speech
        self.refresh_speech_box()

    def npc_said(self, instance):
        db.set_speech_is_completed(self)
        if self.current_npc_speech[0] == '-1':
            self.dismiss()
            return
        self.refresh_speech_box()

    def clear_db(self):
        db.clear_is_completed()


dialog = Dialog()