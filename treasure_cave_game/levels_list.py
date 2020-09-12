from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from treasure_cave_game.level_constructor import constructor
from treasure_cave_game.main import treasure_cave_game
from sqlite_requests import db
from treasure_cave_game.unloading import unloading

Builder.load_file(r'treasure_cave_game/levels_list.kv')


class LevelsList(ModalView):

    def __init__(self, **kwargs):
        super(LevelsList, self).__init__(**kwargs)

        constructor.parent_levels_list = self

    def on_pre_open(self):
        self.ids.levelslist_kv.clear_widgets()
        for level in db.get_all_treasure_game_levels():
            level_box = LevelBox()
            level_box.loc_id = level[0]
            level_box.level_id = level[1]
            level_box.ids.level_text.text = str(level_box.loc_id) + ' ' + str(level_box.level_id)

            self.ids.levelslist_kv.add_widget(level_box)

        add_button = Button()
        add_button.text = '+'
        add_button.size_hint_y = None
        add_button.height = 50
        add_button.bind(on_press=self.add_level)
        self.ids.levelslist_kv.add_widget(add_button)

        add_button = Button()
        add_button.text = 'save'
        add_button.size_hint_y = None
        add_button.height = 50
        add_button.bind(on_press=self.open_save)
        self.ids.levelslist_kv.add_widget(add_button)

    def open_save(self, *l):
        unloading.open()

    def add_level(self, *largs):
        max_lvl = 0
        for obj in self.ids.levelslist_kv.children:
            try:
                if obj.level_id > max_lvl:
                    max_lvl = obj.level_id
            except AttributeError:
                pass
        constructor.level_id = max_lvl + 1
        constructor.loc_id = 0
        constructor.open()


class LevelBox(BoxLayout):

    def __init__(self, **kwargs):
        super(LevelBox, self).__init__(**kwargs)

        self.level_id = -1
        self.loc_id = -1

    def edit_level(self):
        constructor.level_id = self.level_id
        constructor.loc_id = self.loc_id
        constructor.open()

    def open_level(self):
        treasure_cave_game.level_id = self.level_id
        treasure_cave_game.loc_id = self.loc_id
        treasure_cave_game.open()


levels_list = LevelsList()
