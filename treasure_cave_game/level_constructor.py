from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from global_variables import WINDOW
from sqlite_requests import db

Builder.load_file(r'treasure_cave_game/level_constructor.kv')


class ConstructField(ModalView):
    level_id: int
    loc_id: int

    def __init__(self, **kwargs):
        super(ConstructField, self).__init__(**kwargs)

        self.item_chooser = ItemChooser()
        self.parent_levels_list = None

        self.cols = 5  # Колонки
        self.rows = 9  # Столбцы
        self.a = WINDOW.width / (self.cols + 1)

        self.playing_field = self.ids.playing_field
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)

    def on_pre_open(self):

        self.playing_field.clear_widgets()

        self.ids.level_text.text = str(self.loc_id) + ' ' + str(self.level_id)

        current_level = db.get_treasure_game_level(self.loc_id, self.level_id)

        if current_level is None:

            for i in range(self.cols):
                for j in range(self.rows):
                    but = VisualButton()
                    but.size = [self.a, self.a]
                    but.pos = [self.a * i, self.a * j]
                    self.playing_field.add_widget(but)

        else:
            self.ids.exp.text = str(current_level[2])
            self.ids.gold.text = str(current_level[3])
            self.ids.dynamite.text = str(current_level[4])

            for level in db.get_treasure_game_level_settings(self.loc_id, self.level_id):
                purpose = level[2]
                item_id = level[3]
                armor = level[4]
                pos_x = level[5]
                pos_y = level[6]
                size_x = level[7]
                size_y = level[8]

                but = VisualButton()
                but.size = [self.a * size_x, self.a * size_y]
                but.pos = [self.a * pos_x, self.a * pos_y]
                but.purpose = purpose
                but.item_id = item_id

                if but.purpose:
                    but.background_color = (1, 1, 1, 1)

                    if but.purpose == 'car':
                        but.background_normal = 'images/treasure_cave_game/car.png'
                        but.border = [0, 0, 0, 0]
                    elif but.purpose == 'stone':
                        but.text = str(armor)
                    elif but.purpose == 'key':
                        but.background_normal = 'images/treasure_cave_game/key.png'
                        but.border = [5, 5, 5, 5]
                    elif but.purpose == 'item':
                        but.background_normal = db.get_item_image_by_id(but.item_id)
                        but.border = [5, 5, 5, 5]

                self.playing_field.add_widget(but)

    def on_touch_up(self, touch):

        need_to_cancel = not self.ids.rl.collide_point(*touch.pos)

        obj = VisualButton()
        obj.size = [0, 0]
        obj.pos = [self.a * 5, self.a * 9]
        max_pos = [0, 0]

        for but in self.playing_field.children:
            if but.state == 'down':
                if but.purpose:
                    self.return_buttons(but)
                    if but.purpose == 'stone':
                        self.up_stone(but)
                    need_to_cancel = True
                if but.pos[0] < obj.pos[0]:
                    obj.pos[0] = but.pos[0]
                if but.pos[0] > max_pos[0]:
                    max_pos[0] = but.pos[0]
                if but.pos[1] < obj.pos[1]:
                    obj.pos[1] = but.pos[1]
                if but.pos[1] > max_pos[1]:
                    max_pos[1] = but.pos[1]

        obj.size = [max_pos[0] - obj.pos[0] + self.a, max_pos[1] - obj.pos[1] + self.a]

        if (obj.size[0] > self.a and obj.size[1] > self.a) or need_to_cancel:
            for but in self.playing_field.children:
                but.state = 'normal'
            return

        if not self.change_purpose(obj):
            for but in self.playing_field.children:
                but.state = 'normal'
            return

        buttons = self.playing_field.children.copy()
        for but in buttons:
            if but.state == 'down':
                self.playing_field.remove_widget(but)
        self.playing_field.add_widget(obj)

    def up_stone(self, obj):
        new_armor = int(obj.text) * 2
        if new_armor > 16:
            new_armor = 1
        obj.text = str(new_armor)

    def return_buttons(self, obj):
        if self.ids.cancel.state != 'down':
            return

        is_vertical = obj.size[1] > obj.size[0]
        length = int(obj.size[1] / self.a if is_vertical else obj.size[0] / self.a)

        for i in range(length):
            but = VisualButton()
            but.size = [self.a, self.a]
            but.pos = [obj.pos[0] + self.a * (0 if is_vertical else i), obj.pos[1] + self.a * (i if is_vertical else 0)]
            self.playing_field.add_widget(but)

        self.playing_field.remove_widget(obj)

    def change_purpose(self, obj):
        if self.ids.car.state == 'down':
            if obj.pos[1] > 0 or obj.size[0] > self.a or obj.size[1] > self.a:
                return False
            obj.background_normal = 'images/treasure_cave_game/car.png'
            obj.purpose = 'car'
        elif self.ids.stone.state == 'down':
            if obj.pos[1] == 0:
                return False
            obj.purpose = 'stone'
            obj.text = '1'
        elif self.ids.item.state == 'down':
            if obj.pos[1] == 0 or obj.size[0] > self.a or obj.size[1] > self.a:
                return False
            obj.purpose = 'item'
            obj.border = [5, 5, 5, 5]
            self.choose_item(obj)
        elif self.ids.key.state == 'down':
            if obj.pos[1] == 0 or obj.size[0] > self.a or obj.size[1] > self.a:
                return False
            for but in self.playing_field.children:
                if but.purpose == 'key':
                    return False
            obj.purpose = 'key'
            obj.border = [5, 5, 5, 5]
            obj.background_normal = 'images/treasure_cave_game/key.png'
        else:
            return False

        obj.background_color = (1, 1, 1, 1)
        return True

    def choose_item(self, obj):
        self.item_chooser.obj = obj
        self.item_chooser.open()

    def save_level(self):
        try:
            db.set_treasure_cave_level(self.loc_id, self.level_id, int(self.ids.exp.text), int(self.ids.gold.text),
                                       int(self.ids.dynamite.text))

            db.set_treasure_cave_level_settings(self.loc_id, self.level_id, self.playing_field.children, self.a)

            self.parent_levels_list.on_pre_open()
            self.dismiss()
        except:
            pass


class VisualButton(Button):

    def __init__(self, **kwargs):
        super(VisualButton, self).__init__(**kwargs)

        self.purpose = ''
        self.item_id = -1

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.state = 'down'


class ItemChooser(ModalView):

    def __init__(self, **kwargs):
        super(ItemChooser, self).__init__(**kwargs)

        self.obj = None

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

            itembox = ItemBoxItemChooser()
            # itembox.height = WINDOW.height / 10
            itembox.item_id = item_id
            itembox.quantity = qty
            itembox.gold_cost = gold_cost
            itembox.crystal_cost = crystal_cost

            itembox.ids.item_button.name = name
            itembox.ids.item_button.item_id = item_id
            itembox.ids.item_button.image = image
            itembox.ids.item_button.background_normal = image
            itembox.ids.item_button.background_down = image
            itembox.ids.item_button.bind(on_press=self.choose_item)

            self.ids.inventory_box.add_widget(itembox)

    def choose_item(self, but):
        self.obj.background_normal = but.background_normal
        self.obj.item_id = but.item_id
        self.dismiss()


class ItemBoxItemChooser(BoxLayout):
    item_id: int
    description: str
    quantity: int
    gold_cost: int
    crystal_cost: int

    def __init__(self, **kwargs):
        super(ItemBoxItemChooser, self).__init__(**kwargs)

        self.height = WINDOW.height / 10


class ItemItemChooser(Button):
    name: str
    item_id: int
    description: str
    image: str
    gold_cost: int
    crystal_cost: int

    def __init__(self, **kwargs):
        super(ItemItemChooser, self).__init__(**kwargs)

        self.image = ''

        self.background_normal = self.image
        self.background_down = self.image


constructor = ConstructField()
