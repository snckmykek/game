import sqlite3
from kivy.clock import Clock
import xlrd


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_cubes.db')
        self.cur = self.con.cursor()
        self.dict_exel = dict()
        self.read_exel()
        self.sqlite_create_db()
        self.insert_data()

        # self.insert_characters_levels()
        # self.insert_characters_or_skills()
        # self.insert_characters_or_skills('characters')
        # self.insert_levels()
        #
        # self.insert_levels_settings()
        # self.insert_items()
        # self.insert_chest()

    def close(self):
        self.cur.close()
        self.con.close()

    def read_exel(self):
        wb = xlrd.open_workbook('start_db.xlsx')
        for name in wb.sheet_names():
            self.dict_exel.update({name: list()})

            sheet = wb.sheet_by_name(name)

            for nrow in range(sheet.nrows):
                if nrow == 0:
                    continue
                row = list()
                for ncol in range(sheet.ncols):
                    row.append(sheet.cell_value(nrow, ncol))

                self.dict_exel[name].append(row)

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
                         'task_name TEXT,'
                         'task_counter INTEGER,'
                         'mega_task_name TEXT,'
                         'mega_task_counter INTEGER,'
                         'task_image TEXT,'
                         'mega_task_image TEXT,'
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
        self.cur.execute('SELECT * FROM characters WHERE character = '
                         '(SELECT value FROM global WHERE key = "current_character")')
        manuscript = self.cur.fetchall()[0]

        return manuscript

    def get_lvl_settings(self, location=None):
        self.cur.execute('SELECT * FROM lvl_settings WHERE location = "{}"'.format(location))
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
        request = 'SELECT stars, exp, gold FROM completed_levels WHERE loc_id = "{0}" ' \
                  'AND lvl_id = "{1}"'.format(loc_id, lvl_id)

        self.cur.execute(request)
        result = self.cur.fetchall()
        if result:
            result = result[0]
        else:
            result = [0, 0, 0]
        return result

    def get_skills(self, manuscript_id):
        request = 'SELECT * FROM skills WHERE manuscript_id = "{}"'.format(manuscript_id)
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_items(self):
        request = 'SELECT * FROM items_and_resources'
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_items_for_chest(self, chest_id=0):
        request = 'SELECT chest.*, items_and_resources.image FROM chest LEFT OUTER JOIN items_and_resources ON ' \
                  'chest.item_id = items_and_resources.id WHERE chest.chest_id = "{}"'.format(chest_id)
        self.cur.execute(request)

        result = list(self.cur.fetchall())

        items = [((x[2], x[3], x[5]), x[4]) for x in result]

        return items

    def get_manuscripts(self):
        request = 'SELECT * FROM manuscripts'
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_levels(self, loc_id, is_completed="1"):
        request = 'SELECT lvl_id FROM levels WHERE loc_id = "{}" AND is_completed = "{}"'.format(loc_id, is_completed)
        self.cur.execute(request)
        return [x[0] for x in self.cur.fetchall()]

    def get_manuscript_lvl_info(self, character):
        request = 'SELECT character_level, exp, exp_for_next_level FROM characters WHERE character = "{}"'.format(
            character)
        self.cur.execute(request)
        return self.cur.fetchall()[0]

    def get_resources(self):
        self.cur.execute('SELECT quantity FROM items_and_resources WHERE id = 14')
        crystal = self.cur.fetchall()[0][0]

        self.cur.execute('SELECT quantity FROM items_and_resources WHERE id = 15')
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
