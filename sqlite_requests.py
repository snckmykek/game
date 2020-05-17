import sqlite3
from kivy.clock import Clock
# import xlrd
import global_variables


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_cubes.db')
        self.cur = self.con.cursor()
        # self.dict_exel = dict()
        # self.read_exel()
        # self.sqlite_create_db()
        # self.insert_data()
        #
        # for item in self.get_items():
        #     if item[7] == 0:
        #         self.set_item_lvl(item[0])

    def close(self):
        self.cur.close()
        self.con.close()

    def read_exel(self):
        pass
        # wb = xlrd.open_workbook('start_db.xlsx')
        # for name in wb.sheet_names():
        #     self.dict_exel.update({name: list()})
        #
        #     sheet = wb.sheet_by_name(name)
        #
        #     for nrow in range(sheet.nrows):
        #         if nrow == 0:
        #             continue
        #         row = list()
        #         for ncol in range(sheet.ncols):
        #             row.append(sheet.cell_value(nrow, ncol))
        #
        #         self.dict_exel[name].append(row)

    def sqlite_create_db(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS global('
                         'key TEXT,'
                         'value)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS levels('
                         'loc_id INTEGER,'
                         'lvl_id INTEGER,'
                         'is_completed INTEGER,'
                         'difficult INTEGER,'
                         'exp INTEGER,'
                         'gold INTEGER,'
                         'scores INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS completed_levels('
                         'loc_id INTEGER,'
                         'lvl_id INTEGER,'
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
                         'is_completed INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS speech_and_descriptions('
                         'loc_id INTEGER,'
                         'lvl_id INTEGER,'
                         'type TEXT,'
                         'lang TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS manuscripts('
                         'id INTEGER,'
                         'available_image TEXT,'
                         'not_avaliable_image TEXT,'
                         'lvl INTEGER,'
                         'exp INTEGER,'
                         'exp_for_next_lvl INTEGER,'
                         'is_available INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS manuscripts_lang('
                         'id INTEGER,'
                         'name TEXT,'
                         'lang TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS skills('
                         'id INTEGER,'
                         'manuscript_id INTEGER,'
                         'image TEXT,'
                         'lvl INTEGER,'
                         'quantity INTEGER,'
                         'is_unblock INTEGER,'
                         'cost INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS skills_lang('
                         'id INTEGER,'
                         'name TEXT,'
                         'lang TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS for_up_lvl('
                         'object_id INTEGER,'
                         'object_type TEXT,'
                         'lvl INTEGER,'
                         'exp_for_lvl INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS lvl_settings('
                         'loc_id INTEGER,'
                         'id INTEGER,'
                         'cols INTEGER,'
                         'rows INTEGER,'
                         'swipes INTEGER,'
                         'time INTEGER,'
                         'task_name TEXT,'
                         'task_counter INTEGER,'
                         'mega_task_name TEXT,'
                         'mega_task_counter INTEGER,'
                         'task_image TEXT,'
                         'mega_task_image TEXT,'
                         'pos_hint_x REAL,'
                         'pos_hint_y REAL)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS lvl_settings_lang('
                         'id INTEGER,'
                         'loc_id INTEGER,'
                         'name TEXT,'
                         'lang TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS items_and_resources('
                         'id INTEGER,'
                         'image TEXT,'
                         'gold_cost INTEGER,'
                         'crystal_cost INTEGER,'
                         'object_type TEXT,'
                         'lvl INTEGER,'
                         'qty INTEGER,'
                         'qty_for_next_lvl INTEGER,'
                         'dev_info TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS items_and_resources_lang('
                         'id INTEGER,'
                         'name TEXT,'
                         'description TEXT,'
                         'lang TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS chests('
                         'id INTEGER,'
                         'image_closed TEXT,'
                         'image_opened TEXT,'
                         'item_id INTEGER,'
                         'quantity INTEGER,'
                         'probability REAL)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS chests_lang('
                         'id INTEGER,'
                         'name TEXT,'
                         'lang TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS global_bonuses('
                         'loc_id INTEGER,'
                         'lvl_id INTEGER,'
                         'bonus TEXT,'
                         'bonus_type TEXT,'  # mine, ...
                         'quantity REAL)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS game_bonuses('
                         'object_id INTEGER,'
                         'object_type TEXT,'
                         'bonus_item_id INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS colors('
                         'id INTEGER,'
                         'r REAL,'
                         'g REAL,'
                         'b REAL,'
                         'a REAL)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS level_colors('
                         'loc_id INTEGER,'
                         'lvl_id INTEGER,'
                         'color_id INTEGER)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS actions('
                         'id INTEGER,'
                         'loc_id INTEGER,'
                         'lvl_id INTEGER,'
                         'action_type TEXT,'
                         'object_id INTEGER,'
                         'is_completed INTEGER)')

    def insert_data(self):

        for key in self.dict_exel.keys():
            if self.table_is_empty(key):
                for string in self.dict_exel[key]:
                    request = 'INSERT INTO {} VALUES('.format(key)
                    for val in string:
                        request += '"{}",'.format(val)
                    request = request[:-1] + ')'
                    self.cur.execute(request)

        self.commit()

    def get_current_manuscript(self):
        self.cur.execute('SELECT * FROM manuscripts WHERE id = '
                         '(SELECT value FROM global WHERE key = "current_manuscript")')
        manuscript = self.cur.fetchall()[0]

        return manuscript

    def get_lvl_settings(self, loc_id=None):
        self.cur.execute('SELECT lvl_settings.*, lvl_settings_lang.name FROM lvl_settings INNER JOIN lvl_settings_lang '
                         'ON lvl_settings.id = lvl_settings_lang.id AND lvl_settings.loc_id = lvl_settings_lang.loc_id '
                         'WHERE lvl_settings.loc_id = "{0}" '
                         'AND lvl_settings_lang.lang = "{1}"'.format(loc_id, global_variables.LANGUAGE))
        return self.cur.fetchall()

    def get_current_result(self, loc_id, lvl_id, scores):
        request = 'SELECT difficult, exp, gold FROM levels WHERE loc_id = "{0}" ' \
                  'AND lvl_id = "{1}" AND scores = (SELECT MAX(scores) FROM levels WHERE ' \
                  'loc_id = "{2}" AND lvl_id = "{3}" AND scores <= "{4}")' \
            .format(loc_id, lvl_id, loc_id, lvl_id, scores)

        self.cur.execute(request)
        result = self.cur.fetchall()
        if result:
            result = result[0]
        else:
            result = [0, 0, 0]
        return result

    def get_past_result(self, loc_id, lvl_id):

        if lvl_id < 0:  # тогда чекаем ласт уровень прошлой игры
            request = 'SELECT stars, exp, gold FROM completed_levels WHERE loc_id = "{0}" ' \
                      'AND lvl_id = (SELECT MAX(id) FROM lvl_settings WHERE loc_id = "{0}")'\
                .format(loc_id-1)
        else:
            request = 'SELECT stars, exp, gold FROM completed_levels WHERE loc_id = "{0}" ' \
                      'AND lvl_id = "{1}"'.format(loc_id, lvl_id)

        self.cur.execute(request)
        result = self.cur.fetchall()
        if result:
            result = result[0]
        else:
            result = [-1, 0, 0]
        return result

    def is_opened_mine_location(self, lvl_id):
        request = 'SELECT stars, exp, gold FROM completed_levels WHERE loc_id = "{0}" ' \
                  'AND lvl_id = (SELECT MAX(id) FROM lvl_settings WHERE loc_id = "{0}")' \
            .format(lvl_id - 1)

        self.cur.execute(request)

        if self.cur.fetchall():
            return True
        else:
            return False

    def get_skills(self, manuscript_id):
        request = 'SELECT * FROM skills WHERE manuscript_id = "{}"'.format(manuscript_id)
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_items(self):
        request = 'SELECT items_and_resources.*, items_and_resources_lang.name, items_and_resources_lang.description ' \
                  'FROM items_and_resources JOIN items_and_resources_lang ' \
                  'ON items_and_resources.id = items_and_resources_lang.id WHERE items_and_resources_lang.lang = "{}"'\
            .format(global_variables.LANGUAGE)
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_items_for_chest(self, chest_id=0):
        request = 'SELECT chests.item_id, chests.quantity, chests.probability, items_and_resources.image ' \
                  'FROM chests LEFT OUTER JOIN items_and_resources ' \
                  'ON chests.item_id = items_and_resources.id WHERE chests.id = "{}"'.format(chest_id)
        self.cur.execute(request)

        result = list(self.cur.fetchall())

        items = [((x[0], x[1], x[3]), x[2]) for x in result]

        return items

    def get_levels_colors_bonuses(self, loc_id, lvl_id):
        request = 'SELECT colors.r, colors.g, colors.b, colors.a, ' \
                  'SUM(items_and_resources.lvl) FROM game_bonuses ' \
                  'LEFT JOIN items_and_resources ON game_bonuses.bonus_item_id = items_and_resources.id ' \
                  'LEFT JOIN colors ON game_bonuses.object_id = colors.id ' \
                  'WHERE game_bonuses.object_id IN ' \
                  '(SELECT color_id FROM level_colors WHERE loc_id = "{}" AND lvl_id = "{}")' \
                  'GROUP BY colors.r, colors.g, colors.b, colors.a'\
                  .format(loc_id, lvl_id)

        self.cur.execute(request)

        dict_colors = dict()
        for string in self.cur.fetchall():
            dict_colors.update({tuple([string[0], string[1], string[2], string[3]]): string[4]})

        return dict_colors

    def get_manuscripts(self):
        request = 'SELECT * FROM manuscripts'
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_levels(self, loc_id, is_completed="1"):
        request = 'SELECT lvl_id FROM levels WHERE loc_id = "{}" AND is_completed = "{}"'.format(loc_id, is_completed)
        self.cur.execute(request)
        return [x[0] for x in self.cur.fetchall()]

    def get_manuscript_lvl_info(self, manuscript_id):
        request = 'SELECT lvl, exp, exp_for_lvl FROM for_up_lvl WHERE lvl = "{}", object_type = "manuscript"'\
            .format(manuscript_id)

        self.cur.execute(request)
        return self.cur.fetchall()[0]

    def get_resources(self):
        self.cur.execute('SELECT qty FROM items_and_resources WHERE object_type = "crystal"')
        crystal = self.cur.fetchall()[0][0]

        self.cur.execute('SELECT qty FROM items_and_resources WHERE object_type = "gold"')
        gold = self.cur.fetchall()[0][0]

        return [crystal, gold]

    def get_skill_price(self, skill_id):
        self.cur.execute('SELECT cost FROM skills WHERE id = "{}"'.format(skill_id))
        return self.cur.fetchall()[0][0]

    def get_scores_for_stars(self, loc_id, lvl_id):
        self.cur.execute('SELECT scores FROM levels WHERE loc_id = "{}" AND lvl_id = "{}"'.format(loc_id, lvl_id))
        return [x[0] for x in self.cur.fetchall()]

    def get_actions(self, loc_id=-1, lvl_id=-1, action_id=-1, action_type=None):

        if loc_id != -1 and lvl_id != -1:
            request = 'SELECT id, action_type, object_id FROM actions ' \
                      'WHERE loc_id = "{}" AND lvl_id = "{}" AND is_completed = "0"'.format(loc_id, lvl_id)
        else:
            request = ''  # stub

        self.cur.execute(request)

        return self.cur.fetchall()

    def change_actions_completed(self, action_ids, is_completed=1):
        if action_ids:
            request = 'UPDATE actions SET is_completed = "{}" WHERE id IN ('.format(is_completed)
            for action in action_ids:
                request += '"{}",'.format(action)
            request = request[:-1] + ')'
            self.cur.execute(request)
            self.commit()

    def set_skill_quantity(self, skill_id, quantity):
        self.cur.execute('UPDATE skills SET quantity = "{}" WHERE id = "{}"'.format(quantity, skill_id))
        Clock.schedule_once(self.commit)

    def change_items_qty(self, qty, item_id=None, object_type=None):

        if item_id is not None:
            self.cur.execute('UPDATE items_and_resources SET qty = qty + {} WHERE id = "{}"'
                             .format(int(qty), item_id))

        elif object_type is not None:
            self.cur.execute('UPDATE items_and_resources SET qty = qty + {} WHERE object_type = "{}"'
                             .format(int(qty), object_type))
        else:
            return

        self.commit()

    def set_current_manuscript(self, character_id):
        self.cur.execute('UPDATE global SET value = "{}" WHERE key = "current_manuscript"'.format(character_id))
        Clock.schedule_once(self.commit)

    def set_completed_level(self, loc_id, lvl_id, is_completed="1"):
        self.cur.execute('UPDATE levels SET is_completed = "{}" WHERE loc_id = "{}" AND lvl_id = "{}"'
                         .format(is_completed, loc_id, lvl_id))
        Clock.schedule_once(self.commit)

    def set_current_result(self, loc_id, lvl_id, exp, gold, stars):
        self.cur.execute(
            'SELECT COUNT() FROM completed_levels WHERE loc_id = "{}" AND lvl_id = "{}"'.format(loc_id, lvl_id))

        if self.cur.fetchall()[0][0] == 0:
            request = 'INSERT INTO completed_levels VALUES("{}","{}","{}","{}","{}")' \
                .format(loc_id, lvl_id, exp, gold, stars)
        else:
            request = 'UPDATE completed_levels SET exp = "{}", gold = "{}", stars = "{}" WHERE ' \
                      'loc_id = "{}" AND lvl_id = "{}"'.format(exp, gold, stars, loc_id, lvl_id)

        self.cur.execute(request)

        Clock.schedule_once(self.commit)

    def unblock_skill(self, skill_id):
        request = 'UPDATE skills SET is_unblock = "1" WHERE id = "{}"'.format(skill_id)
        self.cur.execute(request)
        Clock.schedule_once(self.commit)

    def unblock_manuscript(self, manuscript_id):
        request = 'UPDATE manuscripts SET is_available = "1" WHERE id = "{}"'.format(manuscript_id)
        self.cur.execute(request)
        Clock.schedule_once(self.commit)

    def set_manuscript_exp(self, manuscript_id, additional_exp):
        self.cur.execute('SELECT exp FROM manuscripts WHERE id = "{}"'.format(manuscript_id))
        exp = self.cur.fetchall()[0][0] + additional_exp

        request = 'SELECT lvl FROM for_up_lvl WHERE object_id = "{}" AND object_type = "manuscript" ' \
                  'AND exp_for_lvl = (SELECT MAX(exp_for_lvl) FROM for_up_lvl WHERE object_id = "{}" ' \
                  'AND object_type = "manuscript" AND exp_for_lvl <= "{}")'.format(manuscript_id, manuscript_id, exp)
        self.cur.execute(request)
        level = self.cur.fetchall()[0][0]

        # for max lvl
        request = 'SELECT MAX(exp_for_lvl) FROM for_up_lvl WHERE object_id = "{}" AND object_type = "manuscript"'\
            .format(manuscript_id)
        self.cur.execute(request)
        max_exp = self.cur.fetchall()[0][0]

        if exp >= max_exp:  # for max lvl
            exp = max_exp
            exp_for_next_level = max_exp
        else:
            request = 'SELECT MIN(exp_for_lvl) FROM for_up_lvl WHERE object_id = "{}" ' \
                      'AND object_type = "manuscript" AND exp_for_lvl > "{}"'.format(manuscript_id, exp)
            self.cur.execute(request)
            exp_for_next_level = self.cur.fetchall()[0][0]

        request = 'UPDATE manuscripts SET exp = "{}", lvl = "{}", exp_for_next_lvl = "{}" ' \
                  'WHERE id = "{}"'.format(exp, level, exp_for_next_level, manuscript_id)
        self.cur.execute(request)

        Clock.schedule_once(self.commit)

    def set_item_lvl(self, item_id):
        self.cur.execute('SELECT qty, object_type FROM items_and_resources WHERE id = "{}"'.format(item_id))
        result = self.cur.fetchall()[0]
        qty, object_type = result[0], result[1]

        if object_type != 'item':
            return

        request = 'SELECT lvl FROM for_up_lvl WHERE object_id = "{0}" AND object_type = "item" ' \
                  'AND exp_for_lvl = (SELECT MAX(exp_for_lvl) FROM for_up_lvl WHERE object_id = "{0}" ' \
                  'AND object_type = "item" AND exp_for_lvl <= "{1}")'.format(item_id, qty)
        self.cur.execute(request)
        level = self.cur.fetchall()[0][0]

        # for max lvl
        request = 'SELECT MAX(exp_for_lvl) FROM for_up_lvl WHERE object_id = "{}" AND object_type = "item"'\
            .format(item_id)
        self.cur.execute(request)
        max_qty = self.cur.fetchall()[0][0]

        if qty >= max_qty:  # for max lvl
            qty = max_qty
            qty_for_next_level = max_qty
        else:
            request = 'SELECT MIN(exp_for_lvl) FROM for_up_lvl WHERE object_id = "{}" ' \
                      'AND object_type = "item" AND exp_for_lvl > "{}"'.format(item_id, qty)
            self.cur.execute(request)
            qty_for_next_level = self.cur.fetchall()[0][0]

        request = 'UPDATE items_and_resources SET lvl = "{}", qty_for_next_lvl = "{}" ' \
                  'WHERE id = "{}"'.format(level, qty_for_next_level, item_id)
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
