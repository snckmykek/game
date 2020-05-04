# Rounds / Levels
from sqlite_requests import db


class SingleRound:

    def __init__(self):
        self.number = '0'
        self.name = '0'
        self.cols = 5
        self.rows = 5
        self.time = -1
        self.swipes = 20
        self.colors = 4
        self.text_level = ''
        self.task_name = ''
        self.mega_task_name = ''
        self.task_counter = 0
        self.mega_task_counter = 0
        self.single_star_diamonds = 0
        self.two_star_diamonds = 0
        self.three_star_diamonds = 0
        self.task_image = ''
        self.mega_task_image = ''


levels_settings = db.get_levels_settings('Первая')

rounds = list()
for lvl_set in levels_settings:
    lvl = SingleRound()
    lvl.number = lvl_set[1]
    lvl.name = lvl_set[8]
    lvl.cols = lvl_set[2]
    lvl.rows = lvl_set[3]
    lvl.swipes = lvl_set[4]
    lvl.time = lvl_set[5]
    lvl.colors = lvl_set[6]
    lvl.text_level = lvl_set[7]
    lvl.task_name = lvl_set[9]
    lvl.task_counter = lvl_set[10]
    lvl.mega_task_name = lvl_set[11]
    lvl.mega_task_counter = lvl_set[12]
    lvl.task_image = lvl_set[13]
    lvl.mega_task_image = lvl_set[14]

    rounds.append(lvl)
