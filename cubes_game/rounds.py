# Rounds / Levels
from sqlite_requests import db


class SingleRound:

    def __init__(self):
        self.loc_id = 0
        self.lvl_id = 0
        self.name = '0'
        self.cols = 5
        self.rows = 5
        self.time = -1
        self.swipes = 20
        self.colors_ids = [0]
        self.cube_colors = [(1, 0, 0, 1)]
        self.text_level = ''
        self.task_name = ''
        self.mega_task_name = ''
        self.task_counter = 0
        self.mega_task_counter = 0
        self.task_image = ''
        self.mega_task_image = ''
        self.pos_hint_x = 0
        self.pos_hint_y = 0


levels_settings = db.get_lvl_settings(0)

rounds = list()
for lvl_set in levels_settings:
    lvl = SingleRound()
    lvl.loc_id = lvl_set[0]
    lvl.lvl_id = lvl_set[1]
    lvl.cols = lvl_set[2]
    lvl.rows = lvl_set[3]
    lvl.swipes = lvl_set[4]
    lvl.time = lvl_set[5]
    lvl.task_name = lvl_set[6]
    lvl.task_counter = lvl_set[7]
    lvl.mega_task_name = lvl_set[8]
    lvl.mega_task_counter = lvl_set[9]
    lvl.task_image = lvl_set[10]
    lvl.mega_task_image = lvl_set[11]
    lvl.pos_hint_x = lvl_set[12]
    lvl.pos_hint_y = lvl_set[13]
    lvl.name = lvl_set[14]

    lvl.colors_bonuses = db.get_levels_colors_bonuses(lvl.loc_id, lvl.lvl_id)
    lvl.cube_colors = list(lvl.colors_bonuses.keys())

    rounds.append(lvl)
