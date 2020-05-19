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

Builder.load_file('store/main.kv')


class StoreScreen(ModalView):

    def __init__(self, **kwargs):
        super(StoreScreen, self).__init__(**kwargs)

        self.money_items = self.ids.money_items
        self.crystal_items = self.ids.crystal_items
        self.total_price = 0

        self.make_content_boxes()

    def make_content_boxes(self):

        self.total_price = 0

        for current_box in [self.ids.money_items, self.ids.crystal_items]:

            current_box.clear_widgets()
            for item in db.get_items() + db.get_skills():
                if len(item) > 9:
                    item_id = item[0]
                    image = item[1]
                    cost = item[2] if (current_box == self.money_items) else item[3]
                    object_type = item[4]
                    lvl = item[5]
                    qty = item[6]
                    qty_for_next_lvl = item[7]
                    name = item[8]
                    description = item[9]
                else:
                    item_id = item[0]
                    image = item[2]
                    cost = item[6]
                    object_type = 'skill'
                    lvl = item[3]
                    qty = item[4]
                    qty_for_next_lvl = -1
                    name = item[7]
                    description = item[8]

                if object_type == 'gold':
                    self.ids.gold.text = str(qty)
                elif object_type == 'crystal':
                    self.ids.crystal.text = str(qty)
                    continue

                if cost == -1:
                    continue

                if (current_box == self.crystal_items) and (object_type == 'skill'):
                    continue

                itembox = ShopItemBox()
                itembox.item_id = item_id
                itembox.object_type = object_type
                itembox.description = description
                itembox.quantity = qty
                itembox.cost = cost
                itembox.storescreen = self

                itembox.ids.item_button.name = name
                itembox.ids.item_button.item_id = item_id
                itembox.ids.item_button.description = description
                itembox.ids.item_button.image = image
                itembox.ids.item_button.background_normal = image
                itembox.ids.item_button.background_down = image

                itembox.ids.item_qty.text = str(qty)
                itembox.ids.cost.text = str(cost)
                itembox.ids.item_max_qty.text = str(qty_for_next_lvl) if qty_for_next_lvl != -1 else ''
                itembox.ids.slash.text = '/' if itembox.ids.item_max_qty.text != '' else ''

                itembox.ids.qty_for_buy.qty = 0

                current_box.add_widget(itembox)

    def refresh_shop(self):

        self.total_price = 0

        current_box = self.ids.money_items if (self.ids.tab_panel.current_tab == self.ids.gold) \
                else self.ids.crystal_items

        for item in db.get_items() + db.get_skills():
            if len(item) > 9:
                item_id = item[0]
                image = item[1]
                cost = item[2] if (current_box == self.money_items) else item[3]
                object_type = item[4]
                lvl = item[5]
                qty = item[6]
                qty_for_next_lvl = item[7]
                name = item[8]
                description = item[9]
            else:
                item_id = item[0]
                image = item[2]
                cost = item[6]
                object_type = 'skill'
                lvl = item[3]
                qty = item[4]
                qty_for_next_lvl = -1
                name = item[7]
                description = item[8]

            if object_type == 'gold':
                self.ids.gold.text = str(qty)
            elif object_type == 'crystal':
                self.ids.crystal.text = str(qty)
                continue

            if cost == -1:
                continue

            for itembox in current_box.children:

                if not ((itembox.item_id == item_id) and (itembox.object_type == object_type)):
                    continue

                itembox.item_id = item_id
                itembox.object_type = object_type
                itembox.description = description
                itembox.quantity = qty
                itembox.cost = cost

                itembox.ids.item_button.name = name
                itembox.ids.item_button.item_id = item_id
                itembox.ids.item_button.description = description
                itembox.ids.item_button.image = image
                itembox.ids.item_button.background_normal = image
                itembox.ids.item_button.background_down = image

                itembox.ids.item_qty.text = str(qty)
                itembox.ids.item_max_qty.text = str(qty_for_next_lvl) if qty_for_next_lvl != -1 else ''
                itembox.ids.slash.text = '/' if itembox.ids.item_max_qty.text != '' else ''

                itembox.ids.qty_for_buy.qty = 0

    def buy_items(self):

        current_box = self.ids.money_items if (self.ids.tab_panel.current_tab == self.ids.gold) \
            else self.ids.crystal_items

        if self.total_price > int(self.ids.gold.text if (current_box == self.ids.money_items) else self.ids.crystal.text):
            # stub добавить окошко типо нахуй иди деняк нет
            return

        # stub добавить окошко типо точно ъочешь купить или нет, передать в окошко переменную с ответом,
        # там ее заполнить и вернуть, если да, то покупаем, нет - нахуй
        answer = True

        if not answer:
            return

        for itembox in current_box.children:
            current_qty = itembox.ids.qty_for_buy.qty
            if current_qty == 0:
                continue

            if itembox.object_type == 'skill':
                db.change_skill_quantity(itembox.item_id, itembox.ids.qty_for_buy.qty)
            else:
                db.change_items_qty(itembox.ids.qty_for_buy.qty, item_id=itembox.item_id)
                db.set_item_lvl(itembox.item_id)

        db.change_items_qty(-self.total_price, object_type='gold' if (current_box == self.ids.money_items) else 'crystal')

        self.refresh_shop()


class ShopItemBox(BoxLayout):
    item_id: int
    description: str
    quantity: int
    cost: int
    object_type: str
    storescreen: ObjectProperty

    def __init__(self, **kwargs):
        super(ShopItemBox, self).__init__(**kwargs)

    def change_qty_for_buy(self, sign):

        if (sign == -1) and (self.ids.qty_for_buy.qty == 0):
            return
        if (sign == +1) and (self.ids.qty_for_buy.qty == 999):
            return

        self.ids.qty_for_buy.qty += 1 * sign
        self.storescreen.total_price += self.cost * sign


class ShopItem(Button):
    name: str
    item_id: int
    description: str
    image: str
    cost: int
    cost: int

    def __init__(self, **kwargs):
        super(ShopItem, self).__init__(**kwargs)

        self.image = ''

        self.background_normal = self.image
        self.background_down = self.image


storescreen = StoreScreen()
