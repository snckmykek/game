from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
from global_variables import WINDOW
import random

Builder.load_file(r'treasure_chest/main.kv')


class TreasureChest(ModalView):

    def __init__(self, **kwargs):
        super(TreasureChest, self).__init__(**kwargs)

        self.chest_is_open = False
        self.card_is_open = False
        self.additional_card_is_open = False
        self.additional_card_is_activate = False

        items = [('crystal_fragments', 25),
                 ('crystal', 1),
                 ('crystal_fragments', 5),
                 ('crystal_fragments', 5),
                 ('crystal_fragments', 5),
                 ('crystal_fragments', 5),
                 ('crystal_fragments', 5),
                 ('crystal_fragments', 5)
                 ]
        random.choices(['Катя', 'Коля'], weights=[10, 20])

    def on_pre_open(self):
        self.ids.chest.background_normal = 'images/treasure_chest/closed_chest.png'
        for card in [self.ids.card_1, self.ids.card_2, self.ids.card_3]:
            card.background_normal = 'images/treasure_chest/card0.png'
            card.background_color = (1, 1, 1, 0)
            card.size = [0, 0]
            card.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.chest_is_open = False
        self.card_is_open = False
        self.additional_card_is_open = False
        self.additional_card_is_activate = False

    def open_chest(self):
        if self.chest_is_open:
            return

        self.ids.chest.background_normal = 'images/treasure_chest/opened_chest.png'

        for card in [self.ids.card_1, self.ids.card_2, self.ids.card_3]:
            if card == self.ids.card_1:
                pos = {'center_x': 3 / 16, 'center_y': 0.7}
            elif card == self.ids.card_2:
                pos = {'center_x': 0.5, 'center_y': 0.7}
            elif card == self.ids.card_3:
                pos = {'center_x': 13 / 16, 'center_y': 0.7}
            else:
                pos = {'center_x': 0.5, 'center_y': 0.7}
            anim = Animation(width=self.width / 4, height=self.height / 4, background_color=(1, 1, 1, 1), pos_hint=pos,
                             d=1.5)

            anim.start(card)

    def open_card(self, card):
        if self.card_is_open and (self.additional_card_is_open or not self.additional_card_is_activate):
            return

        self.additional_card_is_open = self.card_is_open  # В первый раз обе Ложь, во второй раз card_is_open Истина,
        self.card_is_open = True  # в третий раз сразу возврат

        anim = Animation(width=card.width * (6 / 5), height=card.height * (6 / 5), t='in_out_expo', d=.2) \
            + Animation(width=0, t='linear', d=.3)
        anim.bind(on_complete=lambda anim, card: self.open_card2(card))
        anim.start(card)

    def open_card2(self, card):
        card.background_normal = 'images/treasure_chest/card1.png'
        anim = Animation(width=self.width / 4 * (6 / 5), t='linear', d=.3) \
            + Animation(width=self.width / 4, height=self.height / 4, t='in_expo', d=.2)
        anim.start(card)
