import sqlite3
from kivy.clock import Clock


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_cubes.db')
        self.cur = self.con.cursor()
        self.sqlite_create_db()
        self.insert_characters_or_skills()
        self.insert_characters_or_skills('characters')

    def close(self):
        self.cur.close()
        self.con.close()

    def sqlite_create_db(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS completed_levels(location TEXT,level TEXT,is_completed BOOLEAN)')

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
                         'level INTEGER,'
                         'exp INTEGER,'
                         'exp_for_next_level INTEGER,'
                         'mana INTEGER,'
                         'mana_pull INTEGER,'
                         'is_available TEXT,'
                         'is_selected TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS characters_skills('
                         'character TEXT,'
                         'skill TEXT,'
                         'skill_image TEXT,'
                         'skill_level INTEGER,'
                         'quantity INTEGER,'
                         'mana_cost INTEGER,'
                         'is_unblock TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS characters_levels('
                         'character TEXT,'
                         'level INTEGER,'
                         'exp_for_level INTEGER)')

    def insert_characters_or_skills(self, table='characters_skills'):

        if table == 'characters' and self.table_is_empty('characters'):
            characters = (['knight', 'images/characters/knight_available.png',
                           'images/characters/knight_not_available.png', 1, 1, 1, 1, 1, 1, 1],
                          ['fairy', 'images/characters/fairy_available.png',
                           'images/characters/fairy_not_available.png', 1, 1, 1, 1, 1, 1, 0],
                          ['spongebob', 'images/characters/spongebob_available.png',
                           'images/characters/spongebob_not_available.png', 1, 1, 1, 1, 1, 0, 0]
                          )
            for ch in characters:
                request = 'INSERT INTO characters VALUES('
                for val in ch:
                    request += '"{}",'.format(val)
                request = request[:-1] + ')'

                self.cur.execute(request)
        elif table == 'characters_skills':
            if self.table_is_empty('characters_skills'):
                for ch in ['knight', 'fairy', 'spongebob']:
                    if ch == 'knight':
                        for i in range(5):
                            request = 'INSERT INTO characters_skills VALUES("{}","{}","{}","{}","{}","{}","{}")'\
                                .format(ch, 'bomb_{}'.format(i+1), 'images/skills/bomb_{}.png'.format(i+1), 1, 3, 1, 1)
                            self.cur.execute(request)
                    elif ch == 'fairy':
                        request = 'INSERT INTO characters_skills VALUES("{}","{}","{}","{}","{}","{}","{}")' \
                            .format(ch, 'destroy_color', 'images/skills/destroy_color.png', 1, 3, 1, 1)
                        self.cur.execute(request)

        self.commit()

    def get_skills(self, character):
        request = 'SELECT * FROM characters_skills WHERE character = "{}"'.format(character)
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def get_characters(self):
        request = 'SELECT * FROM characters'
        self.cur.execute(request)

        return list(self.cur.fetchall())

    def insert_completed_level(self, location, level, is_completed="1"):
        self.cur.execute('INSERT INTO completed_levels VALUES("{0}","{1}","{2}")'.format(location, level, is_completed))
        Clock.schedule_once(self.commit)

    def get_levels(self, location, is_completed="1"):
        request = 'SELECT level FROM completed_levels WHERE location = "{}" AND is_completed = "{}"'.format(location,
                                                                                                            is_completed)
        self.cur.execute(request)
        return [x[0] for x in self.cur.fetchall()]

    def _insert_info(self, values=None):
        request = 'INSERT INTO info VALUES('
        for val in values:
            request += '"{}",'.format(val)
        request = request[:-1] + ')'

        self.cur.execute(request)
    #   commit() в speech_parser.py

    def dialog_is_completed(self, dialog):
        request = 'SELECT level_info_number FROM info WHERE location = "{}" AND level = "{}" AND is_completed = "1"'\
            .format(dialog.location, dialog.level)

        self.cur.execute(request)

        if self.cur.fetchall():
            return True
        else:
            return False

    def fill_info(self, dialog):

        request = 'SELECT level_info_number, level_info FROM info WHERE location = "{}" AND level = "{}" ' \
                  'AND level_question_number = "{}"'.format(dialog.location, dialog.level, dialog.current_player_speech[0])

        self.cur.execute(request)
        level_info = self.cur.fetchall()

        dialog.current_npc_speech = level_info[0]

        self.set_info_is_completed(dialog)

        dialog.all_player_speech = self.get_all_questions(dialog)

    def get_all_questions(self, dialog):
        request = 'SELECT level_question_number, level_question FROM info WHERE location = "{}" AND level = "{}"' \
                  .format(dialog.location, dialog.level)

        self.cur.execute(request)
        return list(self.cur.fetchall())

    def set_info_is_completed(self, dialog):
        request = 'UPDATE info SET is_completed = "1" WHERE ' \
                  'location = "{}" AND level = "{}" AND level_question_number = "{}"'\
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
