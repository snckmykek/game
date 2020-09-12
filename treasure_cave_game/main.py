from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from dialog.main import dialog
from global_variables import WINDOW
from sqlite_requests import db
from kivy.clock import Clock
from treasure_cave_game.animatoins import do_animation

Builder.load_file(r'treasure_cave_game/main.kv')


class TreasureCaveGame(ModalView):
    level_id: int
    loc_id: int

    def __init__(self, **kwargs):
        super(TreasureCaveGame, self).__init__(**kwargs)

        self.cols = 5  # Колонки
        self.rows = 9  # Столбцы
        self.a = WINDOW.width / (self.cols + 1)

        self.playing_field = self.ids.playing_field
        self.ids.rl.size = (self.a * self.cols, self.a * self.rows)

        self.current_car = None
        self.current_bonus = None
        self.dynamite_power = 1
        self.exp = 0
        self.gold = 0

    def on_pre_open(self):
        self.start_game()

    def start_game(self):
        self.playing_field.clear_widgets()

        self.ids.level_text.text = str(self.loc_id) + ' ' + str(self.level_id)

        current_level = db.get_treasure_game_level(self.loc_id, self.level_id)
        self.exp = str(current_level[2])
        self.gold = str(current_level[3])
        dynamite = str(current_level[4])

        if current_level is None:
            self.dismiss()

        for level in db.get_treasure_game_level_settings(self.loc_id, self.level_id):
            purpose = level[2]
            item_id = level[3]
            armor = level[4]
            pos_x = level[5]
            pos_y = level[6]
            size_x = level[7]
            size_y = level[8]

            if purpose == 'car':
                but = Car()
            elif purpose == '':
                but = VisualLabel()
            else:
                but = VisualButton()
            but.size = [self.a * size_x, self.a * size_y]
            but.pos = [self.a * pos_x, self.a * pos_y]
            but.purpose = purpose
            but.item_id = item_id

            if but.purpose:
                but.background_color = (1, 1, 1, 1)

                if but.purpose == 'car':
                    but.background_normal = 'images/treasure_cave_game/car.png'
                    but.background_down = 'images/treasure_cave_game/car.png'
                    but.bind(on_press=self.change_current_car)
                    but.dynamite = dynamite
                    but.border = [0, 0, 0, 0]
                elif but.purpose == 'stone':
                    but.text = str(armor)
                    but.bind(on_release=self.boom)
                    length = int(size_x if size_x > size_y else size_y)
                    # but.background_normal = 'images/treasure_cave_game/stone{}.png'.format(str(length))
                    # but.background_normal = 'images/treasure_cave_game/stone.png'
                    but.background_down = but.background_normal
                    but.border = [10, 10, 10, 10]
                elif but.purpose == 'key':
                    but.background_normal = 'images/treasure_cave_game/key.png'
                    but.border = [5, 5, 5, 5]
                elif but.purpose == 'item':
                    but.background_normal = db.get_item_image_by_id(but.item_id)
                    but.border = [5, 5, 5, 5]

            self.playing_field.add_widget(but)

        self.move_cars()

    def boom(self, obj):

        if self.current_car is None and self.current_bonus is None:
            return

        if (obj.pos[1] - self.a != self.current_car.pos[1]) \
                or not (obj.pos[0] <= self.current_car.pos[0] <= obj.pos[0] + obj.size[0] - self.a):
            return  # мб анимация типо нельзя

        if self.current_car.dynamite == 0:
            return

        self.current_car.dynamite = int(self.current_car.dynamite) - 1

        armor = int(obj.text)
        new_armor = armor - self.dynamite_power

        if new_armor <= 0:
            self.activate_boom_animation(obj)
            self.move_cars()

        else:
            self.activate_change_armor_animation(obj, new_armor)

    def move_cars(self):
        item = False
        for but in self.playing_field.children.copy():
            if but.purpose == 'car':
                item = item or self.move_car(but)

        if item:
            Clock.schedule_once(self.take_items, .6)

    def take_items(self, *largs):
        for but in self.playing_field.children.copy():
            if but.purpose == 'car':
                action = self.check_next_cell(but.pos[0], but.pos[1] + self.a, True)
                if action != 'stop' and action != 'go':
                    self.return_buttons(action)
                    # do_animation('take_item', action, lambda *l: self.return_buttons)

        self.move_cars()
        # Clock.schedule_once(lambda *l: self.move_cars, .6)

    def move_car(self, obj):
        pos_y = obj.pos[1]
        action = 'go'
        item = False
        while action == 'go':
            pos_y += self.a
            action = self.check_next_cell(obj.pos[0], pos_y)

            if action == 'item':
                item = True

        do_animation('move_car', obj, pos_y - self.a)

        return item

    def activate_boom_animation(self, obj):
        self.ids.playing_field.remove_widget(obj)
        self.return_buttons(obj)

    def activate_change_armor_animation(self, obj, new_armor):
        obj.text = str(new_armor)

    def change_current_car(self, car):
        if car.state == 'down':
            self.current_car = car
        else:
            self.current_car = None

    def check_next_cell(self, pos_x, pos_y, need_return_obj=False):

        next_obj = None

        for obj in self.playing_field.children:
            if obj.pos[0] == pos_x and obj.pos[1] == pos_y:
                next_obj = obj
                break

        if next_obj is None:
            return 'stop'
        else:
            if next_obj.purpose == '':
                return 'go'
            elif next_obj.purpose == 'item' or next_obj.purpose == 'key':
                return next_obj if need_return_obj else 'item'
            elif next_obj.purpose == 'stone':
                return 'stop'

    def return_buttons(self, obj):

        is_vertical = obj.size[1] > obj.size[0]
        length = int(obj.size[1] / self.a if is_vertical else obj.size[0] / self.a)

        for i in range(length):
            but = VisualLabel()
            but.size = [self.a, self.a]
            but.pos = [obj.pos[0] + self.a * (0 if is_vertical else i), obj.pos[1] + self.a * (i if is_vertical else 0)]
            self.playing_field.add_widget(but)

        self.playing_field.remove_widget(obj)


class VisualButton(Button):

    def __init__(self, **kwargs):
        super(VisualButton, self).__init__(**kwargs)

        self.purpose = ''
        self.item_id = -1


class VisualLabel(Label):

    def __init__(self, **kwargs):
        super(VisualLabel, self).__init__(**kwargs)

        self.purpose = ''
        self.item_id = -1


class Car(ToggleButton):

    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)

        self.group = 'car'
        self.purpose = ''
        self.item_id = -1
        self.dynamite = 0


treasure_cave_game = TreasureCaveGame()
