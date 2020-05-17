import sqlite3
from kivy.clock import Clock


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_cubes.db')
        self.cur = self.con.cursor()
        self.sqlite_create_db()
        self.insert_characters_levels()
        self.insert_characters_or_skills()
        self.insert_characters_or_skills('characters')
        self.insert_levels()
        self.insert_global_info()
        self.insert_levels_settings()
        self.insert_items()
        self.insert_chest()

    def close(self):
        self.cur.close()
        self.con.close()

    def sqlite_create_db(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS global('
                         'key TEXT,'
                         'value)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS levels('
                         'location TEXT,'
                         'level TEXT,'
                         'is_completed TEXT,'
                         'difficult INTEGER,'
                         'exp INTEGER,'
                         'gold INTEGER,'
                         'scores INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS completed_levels('
                         'location TEXT,'
                         'level TEXT,'
                         'exp INTEGER,'
                         'gold INTEGER,'
                         'stars INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS info('
                         'location TEXT,'
                         'level TEXT,'
                         'level_info_number TEXT,'
                         'level_info TEXT,'
                         'level_question_number TEXT,'
                         'level_question TEXT, '
                         'is_completed TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS characters('
                         'character TEXT,'
                         'character_available_image TEXT,'
                         'character_not_available_image TEXT,'
                         'character_level INTEGER,'
                         'exp INTEGER,'
                         'exp_for_next_level INTEGER,'
                         'is_available TEXT,'
                         'is_selected TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS characters_skills('
                         'character TEXT,'
                         'skill TEXT,'
                         'skill_image TEXT,'
                         'skill_level INTEGER,'
                         'quantity INTEGER,'
                         'is_unblock TEXT,'
                         'gold_cost INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS characters_levels('
                         'character TEXT,'
                         'character_level INTEGER,'
                         'exp_for_level INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS levels_settings('
                         'location TEXT,'
                         'level TEXT,'
                         'cols INTEGER,'
                         'rows INTEGER,'
                         'swipes INTEGER,'
                         'time INTEGER,'
                         'colors INTEGER,'
                         'text_level TEXT,'
                         'name TEXT,'
                         'task_name TEXT,'
                         'task_counter INTEGER,'
                         'mega_task_name TEXT,'
                         'mega_task_counter INTEGER,'
                         'task_image TEXT,'
                         'mega_task_image TEXT,'
                         'location_order INTEGER,'
                         'pos_hint_x REAL,'
                         'pos_hint_y REAL)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS inventory('
                         'item TEXT,'
                         'name TEXT,'
                         'description TEXT,'
                         'quantity INTEGER,'
                         'image TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS chest('
                         'chest TEXT,'
                         'chest_image TEXT,'
                         'item_id TEXT,'
                         'quantity INTEGER,'
                         'probability REAL)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS bonuses('
                         'location TEXT,'
                         'level TEXT,'
                         'bonus TEXT,'
                         'bonus_type TEXT,'  # mine, ...
                         'quantity REAL)')

    def insert_global_info(self):

        if not self.table_is_empty('global'):
            return

        global_info = {'current_character': 'knight',
                       'crystal': 0,
                       'gold': 0,
                       'current_character_developing': 'knight'
                       }

        for key, val in global_info.items():
            request = 'INSERT INTO global VALUES("{}", "{}")'.format(key, val)
            self.cur.execute(request)

        self.commit()

    def insert_levels(self):

        if not self.table_is_empty('levels'):
            return

        levels = [('Stone mine', '0', '0', '1', 0, 30, 70),
                  ('Stone mine', '0', '0', '2', 0, 50, 130),
                  ('Stone mine', '0', '0', '3', 0, 70, 180),

                  ('Stone mine', '1', '0', '1', 0, 100, 200),
                  ('Stone mine', '1', '0', '2', 0, 150, 250),
                  ('Stone mine', '1', '0', '3', 0, 200, 300),

                  ('Stone mine', '2', '0', '1', 0, 120, 220),
                  ('Stone mine', '2', '0', '2', 0, 170, 250),
                  ('Stone mine', '2', '0', '3', 0, 230, 330),

                  ('Первая', '0', '0', '1', 3, 30, 70),
                  ('Первая', '0', '0', '2', 4, 40, 130),
                  ('Первая', '0', '0', '3', 5, 50, 180),

                  ('Первая', '1', '0', '1', 5, 30, 100),
                  ('Первая', '1', '0', '2', 6, 40, 150),
                  ('Первая', '1', '0', '3', 7, 50, 200),

                  ('Первая', '2', '0', '1', 7, 30, 80),
                  ('Первая', '2', '0', '2', 9, 50, 120),
                  ('Первая', '2', '0', '3', 11, 70, 160),

                  ('Первая', '3', '0', '1', 10, 30, 100),
                  ('Первая', '3', '0', '2', 12, 60, 150),
                  ('Первая', '3', '0', '3', 14, 80, 200),

                  ('Первая', '4', '0', '1', 10, 40, 250),
                  ('Первая', '4', '0', '2', 12, 50, 350),
                  ('Первая', '4', '0', '3', 14, 60, 450),

                  ('Первая', '5', '0', '1', 20, 50, 450),
                  ('Первая', '5', '0', '2', 30, 80, 500),
                  ('Первая', '5', '0', '3', 45, 120, 550),

                  ('Первая', '6', '0', '1', 20, 30, 250),
                  ('Первая', '6', '0', '2', 25, 60, 350),
                  ('Первая', '6', '0', '3', 30, 90, 450),

                  ('Первая', '7', '0', '1', 3, 30, 70),
                  ('Первая', '7', '0', '2', 4, 40, 130),
                  ('Первая', '7', '0', '3', 5, 50, 180),

                  ('Первая', '8', '0', '1', 5, 30, 100),
                  ('Первая', '8', '0', '2', 6, 40, 150),
                  ('Первая', '8', '0', '3', 7, 50, 200),

                  ('Первая', '9', '0', '1', 7, 30, 80),
                  ('Первая', '9', '0', '2', 9, 50, 120),
                  ('Первая', '9', '0', '3', 11, 70, 160),

                  ('Первая', '10', '0', '1', 10, 30, 100),
                  ('Первая', '10', '0', '2', 12, 60, 150),
                  ('Первая', '10', '0', '3', 14, 80, 200),

                  ('Первая', '11', '0', '1', 10, 40, 250),
                  ('Первая', '11', '0', '2', 12, 50, 350),
                  ('Первая', '11', '0', '3', 14, 60, 450),

                  ('Первая', '12', '0', '1', 20, 50, 450),
                  ('Первая', '12', '0', '2', 30, 80, 500),
                  ('Первая', '12', '0', '3', 45, 120, 550),

                  ('Second', '0', '0', '1', 3, 30, 70),
                  ('Second', '0', '0', '2', 4, 40, 130),
                  ('Second', '0', '0', '3', 5, 50, 180),

                  ('Second', '1', '0', '1', 5, 30, 100),
                  ('Second', '1', '0', '2', 6, 40, 150),
                  ('Second', '1', '0', '3', 7, 50, 200),

                  ('Second', '2', '0', '1', 7, 30, 80),
                  ('Second', '2', '0', '2', 9, 50, 120),
                  ('Second', '2', '0', '3', 11, 70, 160),

                  ('Second', '3', '0', '1', 10, 30, 100),
                  ('Second', '3', '0', '2', 12, 60, 150),
                  ('Second', '3', '0', '3', 14, 80, 200),

                  ('Second', '4', '0', '1', 10, 40, 250),
                  ('Second', '4', '0', '2', 12, 50, 350),
                  ('Second', '4', '0', '3', 14, 60, 450),

                  ('Second', '5', '0', '1', 20, 50, 450),
                  ('Second', '5', '0', '2', 30, 80, 500),
                  ('Second', '5', '0', '3', 45, 120, 550),

                  ('Second', '6', '0', '1', 20, 30, 250),
                  ('Second', '6', '0', '2', 25, 60, 350),
                  ('Second', '6', '0', '3', 30, 90, 450),

                  ('Second', '7', '0', '1', 3, 30, 70),
                  ('Second', '7', '0', '2', 4, 40, 130),
                  ('Second', '7', '0', '3', 5, 50, 180),

                  ('Second', '8', '0', '1', 5, 30, 100),
                  ('Second', '8', '0', '2', 6, 40, 150),
                  ('Second', '8', '0', '3', 7, 50, 200),

                  ('Second', '9', '0', '1', 7, 30, 80),
                  ('Second', '9', '0', '2', 9, 50, 120),
                  ('Second', '9', '0', '3', 11, 70, 160),

                  ('Second', '10', '0', '1', 10, 30, 100),
                  ('Second', '10', '0', '2', 12, 60, 150),
                  ('Second', '10', '0', '3', 14, 80, 200),

                  ('Second', '11', '0', '1', 10, 40, 250),
                  ('Second', '11', '0', '2', 12, 50, 350),
                  ('Second', '11', '0', '3', 14, 60, 450),

                  ('Second', '12', '0', '1', 20, 50, 450),
                  ('Second', '12', '0', '2', 30, 80, 500),
                  ('Second', '12', '0', '3', 45, 120, 550)
                  ]

        for level in levels:
            request = 'INSERT INTO levels VALUES('
            for val in level:
                request += '"{}",'.format(val)
            request = request[:-1] + ')'
            self.cur.execute(request)
        self.commit()

    def insert_levels_settings(self):

        if not self.table_is_empty('levels_settings'):
            return

        levels_settings = \
            [
                ('Stone mine', '0', 5, 5, 10, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '1', 5, 5, 10, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '2', 3, 3, 20, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '3', 5, 5, 20, -1, 5, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '4', 5, 5, 5, -1, 2, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '5', 8, 8, 20, -1, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '6', 4, 6, 30, -1, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '7', 5, 5, 10, 60, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '8', 3, 3, 20, 100, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '9', 5, 5, 20, 100, 5, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '10', 5, 5, 5, 25, 2, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '11', 8, 8, 20, 120, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),
                ('Stone mine', '12', 4, 6, 30, 150, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", -1),

                ('Первая', '0', 5, 5, 10, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '1', 5, 5, 10, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '2', 3, 3, 20, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '3', 5, 5, 20, -1, 5, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '4', 5, 5, 5, -1, 2, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '5', 8, 8, 20, -1, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '6', 4, 6, 30, -1, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '7', 5, 5, 10, 60, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '8', 3, 3, 20, 100, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '9', 5, 5, 20, 100, 5, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '10', 5, 5, 5, 25, 2, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '11', 8, 8, 20, 120, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),
                ('Первая', '12', 4, 6, 30, 150, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 0),

                ('Second', '0', 5, 5, 10, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '1', 5, 5, 10, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '2', 3, 3, 20, -1, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '3', 5, 5, 20, -1, 5, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '4', 5, 5, 5, -1, 2, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '5', 8, 8, 20, -1, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '6', 4, 6, 30, -1, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '7', 5, 5, 10, 60, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '8', 3, 3, 20, 100, 3, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '9', 5, 5, 20, 100, 5, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '10', 5, 5, 5, 25, 2, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '11', 8, 8, 20, 120, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1),
                ('Second', '12', 4, 6, 30, 150, 4, "", "", "break_stone_color", 15, "combo", 3,
                 "images/info_and_tasks/task_break_stone_color.png", "images/info_and_tasks/combo.png", 1)
            ]

        for level_settings in levels_settings:
            request = 'INSERT INTO levels_settings VALUES('
            for val in level_settings:
                request += '"{}",'.format(val)
            request = request[:-1] + ')'
            self.cur.execute(request)
        self.commit()

    def insert_items(self):

        if not self.table_is_empty('inventory'):
            return

        items = \
            [
                ('item_0', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 56,
                 'images/items/item_0.png'),
                ('item_1', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 113,
                 'images/items/item_1.png'),
                ('item_2', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 633,
                 'images/items/item_2.png'),
                ('item_3', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 1,
                 'images/items/item_3.png'),
                ('item_4', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 96,
                 'images/items/item_4.png'),
                ('item_5', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 13,
                 'images/items/item_5.png'),
                ('item_6', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_6.png'),
                ('item_7', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_7.png'),
                ('item_8', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_8.png'),
                ('item_9', 'Кровавый амулет', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_9.png'),
                ('item_10', 'Разноцветный амулет', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_10.png'),
                ('item_11', 'Вероятность найти сундук', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_11.png'),
                ('chest_1', 'Сундук с сокровищами', 'Выпадает рандом элемент', 19,
                 'images/items/chest.png'),
                ('item_12', 'Вероятность найти ресурсы', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_12.png'),
                ('item_13', 'Комбо бонус', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/item_13.png'),
                ('crystal', 'Кристаллы', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/crystal.png'),
                ('gold', 'Золото', 'Увеличивает количество очков за красные элементы', 0,
                 'images/items/gold.png')
            ]

        for item in items:
            request = 'INSERT INTO inventory VALUES('
            for val in item:
                request += '"{}",'.format(val)
            request = request[:-1] + ')'
            self.cur.execute(request)
        self.commit()

    def insert_chest(self):

        if not self.table_is_empty('chest'):
            return

        items = \
            [
                ('chest_1', 'images/items/chest.png', 'item_0', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_1', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_2', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_3', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_4', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_5', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_6', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_7', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_8', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_9', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_10', 1, 3),
                ('chest_1', 'images/items/chest.png', 'item_11', 1, 0.5),
                ('chest_1', 'images/items/chest.png', 'item_12', 1, 0.5),
                ('chest_1', 'images/items/chest.png', 'item_13', 1, 0.5),
                ('chest_1', 'images/items/chest.png', 'crystal', 10, 1),
                ('chest_1', 'images/items/chest.png', 'gold', 120, 20)
            ]

        for item in items:
            request = 'INSERT INTO chest VALUES('
            for val in item:
                request += '"{}",'.format(val)
            request = request[:-1] + ')'
            self.cur.execute(request)
        self.commit()

    def insert_bonuses(self):

        if not self.table_is_empty('bonuses'):
            return

        items = \
            [
                ('Первая', '', 'Stone mine', 'mine', 0),
                ('Second', '', 'Coal mine', 'mine', 0),
                ('Третья', '', 'Ore mine', 'mine', 0)
            ]

        for item in items:
            request = 'INSERT INTO bonuses VALUES('
            for val in item:
                request += '"{}",'.format(val)
            request = request[:-1] + ')'
            self.cur.execute(request)
        self.commit()

    def insert_characters_levels(self):

        if not self.table_is_empty('characters_levels'):
            return

        characters = ['knight', 'fairy', 'spongebob']

        for ch in characters:
            m = 10
            for i in range(100):
                m += 2
                request = 'INSERT INTO characters_levels VALUES("{}","{}","{}")'.format(ch, i, i * m)
                self.cur.execute(request)
        self.commit()

    def insert_characters_or_skills(self, table='characters_skills'):

        if table == 'characters' and self.table_is_empty('characters'):
            characters = (['knight', 'images/characters/knight_available.png',
                           'images/characters/knight_not_available.png', 0, 0, 1, 1, 1],
                          ['fairy', 'images/characters/fairy_available.png',
                           'images/characters/fairy_not_available.png', 0, 0, 1, 1, 0],
                          ['spongebob', 'images/characters/spongebob_available.png',
                           'images/characters/spongebob_not_available.png', 0, 0, 1, 0, 0]
                          )
            for ch in characters:
                request = 'INSERT INTO characters VALUES('
                for val in ch:
                    request += '"{}",'.format(val)
                request = request[:-1] + ')'

                self.cur.execute(request)

                self.set_characters_exp(ch[0], 0)
        elif table == 'characters_skills':
            if self.table_is_empty('characters_skills'):
                for ch in ['knight', 'fairy', 'spongebob']:
                    if ch == 'knight':
                        for i in range(5):
                            unblock = 1 if i == 0 else 1
                            request = 'INSERT INTO characters_skills VALUES("{}","{}","{}","{}","{}","{}","{}")' \
                                .format(ch, 'bomb_{}'.format(i + 1), 'images/skills/bomb_{}.png'.format(i + 1), 1, 3,
                                        unblock, 10)
                            self.cur.execute(request)
                    elif ch == 'fairy':
                        request = 'INSERT INTO characters_skills VALUES("{}","{}","{}","{}","{}","{}","{}")' \
                            .format(ch, 'destroy_color', 'images/skills/destroy_color.png', 1, 3, 1, 50)
                        self.cur.execute(request)

        self.commit()

    def get_current_character(self):
        self.cur.execute('SELECT * FROM characters WHERE character = '
                         '(SELECT value FROM global WHERE key = "current_character")')
        character = self.cur.fetchall()[0]

        return character

    def get_levels_settings(self, location=None):
        self.cur.execute('SELECT * FROM levels_settings WHERE location = "{}"'.format(location))
        return self.cur.fetchall()

    def get_current_result(self, location, level, scores):
        request = 'SELECT difficult, exp, gold FROM levels WHERE location = "{0}" ' \
                  'AND level = "{1}" AND scores = (SELECT MAX(scores) FROM levels WHERE ' \
                  'location = "{2}" AND level = "{3}" AND scores <= "{4}")' \
            .format(location, level, location, level, scores)

        self.cur.execute(request)
        result = self.cur.fetchall()
        if result:
            result = result[0]
        else:
            result = [0, 0, 0]
        return result

    def get_past_result(self, location, level):
        request = 'SELECT stars, exp, gold FROM completed_levels WHERE location = "{0}" ' \
                  'AND level = "{1}"'.format(location, level)

        self.cur.execute(request)
        result = self.cur.fetchall()
        if result:
            result = result[0]
        else:
            result = [0, 0, 0]
        return result

    def get_skills(self, character):
        request = 'SELECT * FROM characters_skills WHERE character = "{}"'.format(character)
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_items(self):
        request = 'SELECT * FROM inventory'
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_items_for_chest(self, chest='chest_1'):
        request = 'SELECT chest.*, inventory.image FROM chest LEFT OUTER JOIN inventory ON chest.item_id' \
                  ' = inventory.item WHERE chest.chest = "{}"'.format(chest)
        self.cur.execute(request)

        result = list(self.cur.fetchall())

        items = [((x[2], x[3], x[5]), x[4]) for x in result]

        return items

    def get_characters(self):
        request = 'SELECT * FROM characters'
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_levels(self, location, is_completed="1"):
        request = 'SELECT level FROM levels WHERE location = "{}" AND is_completed = "{}"'.format(location,
                                                                                                  is_completed)
        self.cur.execute(request)
        return [x[0] for x in self.cur.fetchall()]

    def get_character_level_info(self, character):
        request = 'SELECT character_level, exp, exp_for_next_level FROM characters WHERE character = "{}"'.format(
            character)
        self.cur.execute(request)
        return self.cur.fetchall()[0]

    def get_resources(self):
        self.cur.execute('SELECT value FROM global WHERE key = "crystal"')
        crystal = self.cur.fetchall()[0][0]

        self.cur.execute('SELECT value FROM global WHERE key = "gold"')
        gold = self.cur.fetchall()[0][0]

        return [crystal, gold]

    def get_skill_price(self, skill_name):
        self.cur.execute('SELECT gold_cost FROM characters_skills WHERE skill = "{}"'.format(skill_name))
        return self.cur.fetchall()[0][0]

    def get_scores_for_stars(self, location, level):
        self.cur.execute('SELECT scores FROM levels WHERE location = "{}" AND level = "{}"'.format(location, level))
        return [x[0] for x in self.cur.fetchall()]

    def set_gold(self, gold):
        self.cur.execute(
            'UPDATE global SET value = value + "{}" WHERE key = "gold"'.format(gold))
        Clock.schedule_once(self.commit)

    def set_skill_quantity(self, skill_name, quantity):
        self.cur.execute('UPDATE characters_skills SET quantity = "{}" WHERE skill = "{}"'.format(quantity, skill_name))
        Clock.schedule_once(self.commit)

    def set_items_qty_change(self, item_id, qty):
        if (item_id == 'crystal') or (item_id == 'gold'):
            self.cur.execute(
                'UPDATE global SET value = value + {} WHERE key = "{}"'.format(int(qty), item_id))
        else:
            self.cur.execute('UPDATE inventory SET quantity = quantity + {} WHERE item = "{}"'.format(int(qty), item_id))
        self.commit()

    def set_current_character(self, character_name):
        self.cur.execute('UPDATE global SET value = "{}" WHERE key = "current_character"'.format(character_name))
        Clock.schedule_once(self.commit)

    def set_completed_level(self, location, level, is_completed="1"):
        self.cur.execute('UPDATE levels SET is_completed = "{}" WHERE location = "{}" AND level = "{}"'
                         .format(is_completed, location, level))
        Clock.schedule_once(self.commit)

    def set_current_result(self, location, level, exp, cf, stars):
        self.cur.execute(
            'SELECT COUNT() FROM completed_levels WHERE location = "{}" AND level = "{}"'.format(location, level))

        if self.cur.fetchall()[0][0] == 0:
            request = 'INSERT INTO completed_levels VALUES("{}","{}","{}","{}","{}")' \
                .format(location, level, exp, cf, stars)
        else:
            request = 'UPDATE completed_levels SET exp = "{}", gold = "{}", stars = "{}" WHERE ' \
                      'location = "{}" AND level = "{}"'.format(exp, cf, stars, location, level)

        self.cur.execute(request)

        Clock.schedule_once(self.commit)

    def set_characters_exp(self, character, additional_exp):
        self.cur.execute('SELECT exp FROM characters WHERE character = "{}"'.format(character))
        exp = self.cur.fetchall()[0][0] + additional_exp

        request = 'SELECT character_level FROM characters_levels WHERE character = "{}" ' \
                  'AND exp_for_level = (SELECT MAX(exp_for_level) FROM characters_levels WHERE character = "{}" ' \
                  'AND exp_for_level <= "{}")'.format(character, character, exp)
        self.cur.execute(request)
        level = self.cur.fetchall()[0][0]

        # for max lvl
        request = 'SELECT MAX(exp_for_level) FROM characters_levels WHERE character = "{}"'.format(character)
        self.cur.execute(request)
        max_exp = self.cur.fetchall()[0][0]

        if exp >= max_exp:  # for max lvl
            exp = max_exp
            exp_for_next_level = max_exp
        else:
            request = 'SELECT MIN(exp_for_level) FROM characters_levels WHERE character = "{}" ' \
                      'AND exp_for_level > "{}"'.format(character, exp)
            self.cur.execute(request)
            exp_for_next_level = self.cur.fetchall()[0][0]

        request = 'UPDATE characters SET exp = "{}", character_level = "{}", exp_for_next_level = "{}" ' \
                  'WHERE character = "{}"'.format(exp, level, exp_for_next_level, character)
        self.cur.execute(request)

        Clock.schedule_once(self.commit)

    def _insert_info(self, values=None):
        request = 'INSERT INTO info VALUES('
        for val in values:
            request += '"{}",'.format(val)
        request = request[:-1] + ')'

        self.cur.execute(request)

    #   commit() в speech_parser.py

    def dialog_is_completed(self, dialog):
        request = 'SELECT level_info_number FROM info WHERE location = "{}" AND level = "{}" AND is_completed = "1"' \
            .format(dialog.location, dialog.level)

        self.cur.execute(request)

        if self.cur.fetchall():
            return True
        else:
            return False

    def fill_info(self, dialog):

        request = 'SELECT level_info_number, level_info FROM info WHERE location = "{}" AND level = "{}" ' \
                  'AND level_question_number = "{}"'.format(dialog.location, dialog.level,
                                                            dialog.current_player_speech[0])

        self.cur.execute(request)
        level_info = self.cur.fetchall()

        try:
            dialog.current_npc_speech = level_info[0]
        except IndexError:
            dialog.current_npc_speech = 'stub'

        self.set_info_is_completed(dialog)

        dialog.all_player_speech = self.get_all_questions(dialog)

    def get_all_questions(self, dialog):
        request = 'SELECT level_question_number, level_question FROM info WHERE location = "{}" AND level = "{}"' \
            .format(dialog.location, dialog.level)

        self.cur.execute(request)
        return list(self.cur.fetchall())

    def set_info_is_completed(self, dialog):
        request = 'UPDATE info SET is_completed = "1" WHERE ' \
                  'location = "{}" AND level = "{}" AND level_question_number = "{}"' \
            .format(dialog.location, dialog.level, dialog.current_player_speech[0])
        self.cur.execute(request)

        self.commit()

    def clear_is_completed(self):
        self.cur.execute('UPDATE info SET is_completed = "0"')

    def commit(self, *l):
        self.con.commit()

    def table_is_empty(self, table='info'):
        request = 'SELECT COUNT(*) as count FROM {}'.format(table)
        self.cur.execute(request)
        return self.cur.fetchall()[0][0] == 0

    def delete_table(self, table='info'):
        self.cur.execute('DROP TABLE IF EXISTS {}'.format(table))
        self.commit()


db = Database()
