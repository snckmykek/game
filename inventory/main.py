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
from global_variables import WINDOW, FIRSTSHARDS
from sqlite_requests import db
from treasure_chest.main import TreasureChest
import random

Builder.load_file(r'inventory/main.kv')


def get_qty_shards(qty=0):
    item_max_qty = FIRSTSHARDS

    item_level = 0
    item_qty = 0

    for i in range(qty):
        item_qty += 1
        if item_qty == item_max_qty:
            item_level += 1
            item_max_qty *= 2

    return {'item_level': item_level, 'item_qty': item_qty, 'item_max_qty': item_max_qty}


class Inventory(ModalView):

    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)

        self.inventory_box = self.ids.inventory_box
        self.treasure_chest = TreasureChest()

    def on_pre_open(self):
        self.refresh_inventory()

    def open_treasure_chest(self):
        self.treasure_chest.owner = self
        self.treasure_chest.open()

    def refresh_inventory(self):

        self.ids.chest_qty.text = '0'

        self.inventory_box.clear_widgets()
        for item in db.get_items():
            item_id = item[0]
            image = item[1]
            gold_cost = item[2]
            crystal_cost = item[3]
            object_type = item[4]
            lvl = item[5]
            qty = item[6]
            qty_for_next_lvl = item[7]
            name = item[8]
            description = item[9]

            if object_type == 'chest':  # Сундуки в отдельном поле находятся
                self.ids.chest_qty.text = str(int(self.ids.chest_qty.text) + qty)
                continue
            elif object_type == 'gold':
                self.ids.gold.text = str(qty)
                continue
            elif object_type == 'crystal':
                self.ids.crystal.text = str(qty)
                continue

            itembox = ItemBox()
            # itembox.height = WINDOW.height / 10
            itembox.item_id = item_id
            itembox.description = description
            itembox.quantity = qty
            itembox.gold_cost = gold_cost
            itembox.crystal_cost = crystal_cost

            itembox.ids.item_button.name = name
            itembox.ids.item_button.item_id = item_id
            itembox.ids.item_button.description = description
            itembox.ids.item_button.image = image
            itembox.ids.item_button.background_normal = image
            itembox.ids.item_button.background_down = image

            # dict_qty = get_qty_shards(itembox.quantity)
            itembox.ids.item_level.text = str(lvl)
            itembox.ids.item_qty.text = str(qty)
            itembox.ids.item_max_qty.text = str(qty_for_next_lvl)

            self.inventory_box.add_widget(itembox)


class ItemBox(BoxLayout):
    item_id: int
    description: str
    quantity: int
    gold_cost: int
    crystal_cost: int

    def __init__(self, **kwargs):
        super(ItemBox, self).__init__(**kwargs)

        self.height = WINDOW.height / 10


class Item(Button):
    name: str
    item_id: int
    description: str
    image: str
    gold_cost: int
    crystal_cost: int

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

        self.image = ''

        self.background_normal = self.image
        self.background_down = self.image
