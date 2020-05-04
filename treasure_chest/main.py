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
from sqlite_requests import db
import random

Builder.load_file(r'treasure_chest/main.kv')


class TreasureChest(ModalView):

    def __init__(self, **kwargs):
        super(TreasureChest, self).__init__(**kwargs)

        self.chest_is_open = False
        self.card_is_open = False
        self.additional_card_is_open = False
        self.additional_card_is_activate = False
        self.owner = ObjectProperty
        self.preliminary_prizes = list()

        self.items = [(('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 25),
                      (('crystal', 10, 'images/treasure_chest/card1.png'), 1),
                      (('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 5),
                      (('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 15),
                      (('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 25),
                      (('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 10),
                      (('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 15),
                      (('crystal_fragments', 70, 'images/treasure_chest/card1.png'), 25)
                      ]

    def on_pre_open(self):
        self.ids.chest.background_normal = 'images/treasure_chest/closed_chest.png'
        for card in [self.ids.card_1, self.ids.card_2, self.ids.card_3]:
            card.background_normal = 'images/treasure_chest/card0.png'
            card.background_color = (1, 1, 1, 0)
            card.size = [0, 0]
            card.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            card.color = (1, 1, 1, 0)

        self.chest_is_open = False
        self.card_is_open = False
        self.additional_card_is_open = False
        self.additional_card_is_activate = False

        self.items = db.get_items_for_chest()

    def on_dismiss(self):
        self.owner.refresh_inventory()

    def open_chest(self):
        if self.chest_is_open:
            return

        self.preliminary_prizes.clear()
        self.preliminary_prizes.extend(random.choices([x[0] for x in self.items], weights=[x[1] for x in self.items], k=3))

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

        if card == self.ids.card_1:
            db.set_items_qty_change(self.preliminary_prizes[0][0], self.preliminary_prizes[0][1])
            card.text = self.preliminary_prizes[0][0]
        elif card == self.ids.card_2:
            db.set_items_qty_change(self.preliminary_prizes[1][0], self.preliminary_prizes[1][1])
            card.text = self.preliminary_prizes[1][0]
        elif card == self.ids.card_3:
            db.set_items_qty_change(self.preliminary_prizes[2][0], self.preliminary_prizes[2][1])
            card.text = self.preliminary_prizes[2][0]

        anim = Animation(width=card.width * (6 / 5), height=card.height * (6 / 5), t='in_out_expo', d=.2) \
               + Animation(width=0, t='linear', d=.3)
        anim.bind(on_complete=lambda anim, card: self.open_card2(card))
        anim.start(card)

    def open_card2(self, card):
        if card == self.ids.card_1:
            card.background_normal = self.preliminary_prizes[0][2]
        elif card == self.ids.card_2:
            card.background_normal = self.preliminary_prizes[1][2]
        elif card == self.ids.card_3:
            card.background_normal = self.preliminary_prizes[2][2]

        anim = Animation(width=self.width / 4 * (6 / 5), t='linear', d=.3) \
               + Animation(width=self.width / 4, height=self.height / 4, t='in_expo', d=.2)
        anim.start(card)
