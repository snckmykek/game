from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
from sqlite_requests import db

Builder.load_file('treasure_cave_game/unloading.kv')


class Unloading(ModalView):

    def __init__(self, **kwargs):
        super(Unloading, self).__init__(**kwargs)

    def on_pre_open(self):
        levels_text = ''
        level_settings_text = ''

        for level in db.get_all_treasure_game_levels():
            loc_id = level[0]
            level_id = level[1]

            current_level = db.get_treasure_game_level(loc_id, level_id)

            exp = str(current_level[2])
            gold = str(current_level[3])
            dynamite = str(current_level[4])

            levels_text += str(loc_id) + '|' + str(level_id) + '|' + str(0) + '|' + str(exp) + '|' + \
                str(gold) + '|' + str(dynamite) + '\n'

        self.ids.levels.text = levels_text

        for level in db.get_all_treasure_game_level_settings():
            loc_id = level[0]
            level_id = level[1]
            purpose = level[2]
            item_id = level[3]
            armor = level[4]
            pos_x = level[5]
            pos_y = level[6]
            size_x = level[7]
            size_y = level[8]

            level_settings_text += str(loc_id) + '|' + str(level_id) + '|' + str(purpose) + '|' + \
                str(item_id) + '|' + str(armor) + '|' + str(pos_x) + '|' + \
                str(pos_y) + '|' + str(size_x) + '|' + str(size_y) + '\n'

        self.ids.level_settings.text = level_settings_text

    def copy_text(self, ti):
        ti.copy(ti.text)


unloading = Unloading()
