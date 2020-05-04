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

        resources = db.get_resources()

        self.ids.crystal.text = str(resources[0])
        self.ids.crystal_fragments.text = str(resources[1])

        self.inventory_box.clear_widgets()
        for item in db.get_items():
            item_id = item[0]
            name = item[1]
            description = item[2]
            quantity = item[3]
            image = item[4]

            if item_id[:5] == 'chest':  # Сундуки в отдельном поле находятся
                self.ids.chest_qty.text = str(quantity)
                self.ids.chest_qty_image.background_normal = str(image)
                self.ids.chest_qty_image.background_down = str(image)
                continue

            itembox = ItemBox()
            # itembox.height = WINDOW.height / 10
            itembox.item_id = item_id
            itembox.description = description
            itembox.quantity = quantity

            itembox.ids.item_button.name = name
            itembox.ids.item_button.item_id = item_id
            itembox.ids.item_button.description = description
            itembox.ids.item_button.image = image
            itembox.ids.item_button.background_normal = image
            itembox.ids.item_button.background_down = image

            dict_qty = get_qty_shards(itembox.quantity)
            itembox.ids.item_level.text = str(dict_qty['item_level'])
            itembox.ids.item_qty.text = str(dict_qty['item_qty'])
            itembox.ids.item_max_qty.text = str(dict_qty['item_max_qty'])

            self.inventory_box.add_widget(itembox)


class ItemBox(BoxLayout):
    item_id: str
    description: str
    quantity: int

    def __init__(self, **kwargs):
        super(ItemBox, self).__init__(**kwargs)

        self.height = WINDOW.height / 10


class Item(Button):
    name: str
    item_id: str
    description: str
    image: str

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)

        self.image = ''

        self.background_normal = self.image
        self.background_down = self.image
