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

        self.cur.execute('CREATE TABLE IF NOT EXISTS speech('
                         'location TEXT,'
                         'level TEXT,'
                         'npc TEXT,'
                         'npc_number_speech TEXT,'
                         'npc_speech TEXT,'
                         'player_number_speech TEXT,'
                         'player_speech TEXT,'
                         'is_available_by_speech TEXT,'
                         'alternatives TEXT,'
                         'is_available_by_rating TEXT,'
                         'is_completed TEXT,'
                         'is_canceled TEXT,'
                         'is_after_game TEXT)')

        self.cur.execute('CREATE TABLE IF NOT EXISTS characters('
                         'character TEXT,'
                         'character_available_image TEXT,'
                         'character_not_available_image TEXT,'
                         'level INTEGER,'
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

    def insert_characters_or_skills(self, table='characters_skills'):

        if table == 'characters' and self.table_is_empty('characters'):
            characters = (['knight', 'images/characters/knight_available.png',
                           'images/characters/knight_not_available.png', 1, 1, 1],
                          ['fairy', 'images/characters/fairy_available.png',
                           'images/characters/fairy_not_available.png', 1, 1, 0],
                          ['spongebob', 'images/characters/spongebob_available.png',
                           'images/characters/spongebob_not_available.png', 1, 1, 0]
                          )
            for ch in characters:
                request = 'INSERT INTO characters VALUES("{}","{}","{}","{}","{}","{}")'.format(*ch)
                self.cur.execute(request)
        else:
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
        request = 'SELECT * FROM characters'.format()
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

    def _insert_speech(self, values=None):
        request = 'INSERT INTO speech VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}",' \
                  '"{11}","{12}")'.format(*values)
        self.cur.execute(request)

    def fill_speech(self, dialog, after_game=False):

        after_game = "1" if after_game else "0"

        request = 'SELECT npc_number_speech, npc_speech FROM speech WHERE ' \
                  'location = "{}" AND level = "{}" AND npc != "" AND player_number_speech = "{}" ' \
                  'AND is_completed = "0" AND is_after_game = "{}" AND is_canceled = "0"'\
            .format(dialog.location, dialog.level, dialog.current_player_speech[0], after_game)

        self.cur.execute(request)
        npc_speech = self.cur.fetchall()

        if (dialog.current_player_speech[0] == '') and (not npc_speech):
            if self.get_all_player_speech(dialog, after_game):
                npc_speech.append(tuple(['-2', 'Что-нибудь еще?']))

        if not npc_speech:
            request = 'SELECT npc_number_speech, npc_speech FROM speech WHERE ' \
                      'location = "{}" AND level = "{}" AND npc != "" AND npc_number_speech = "-1" ' \
                      'AND is_after_game = "{}"'.format(dialog.location, dialog.level, after_game)
            self.cur.execute(request)
            npc_speech = self.cur.fetchall()
            if not npc_speech:
                if not after_game:
                    npc_speech.append(tuple(['-1', 'Я занят.']))
                else:
                    npc_speech.append(tuple(['-1', 'Еще увидимся!']))

        if len(npc_speech) > 1:
            pass

        dialog.current_npc_speech = npc_speech[0]

        self.set_speech_is_completed(dialog)

        dialog.all_player_speech = self.get_all_player_speech(dialog, after_game)

    def get_all_player_speech(self, dialog, after_game):
        request = 'SELECT npc_number_speech, is_available_by_rating, is_available_by_speech, player_number_speech ' \
                  'FROM speech WHERE location = "{}" AND level = "{}" AND npc != "" AND is_completed = "0" ' \
                  'AND is_after_game = "{}" AND is_canceled = "0"'.format(dialog.location, dialog.level, after_game)

        self.cur.execute(request)
        available_npc_speech = list(self.cur.fetchall())
        available_npc_speech_copy = available_npc_speech.copy()
        npc_speech_numbers = [s[0] for s in available_npc_speech]
        for sp in available_npc_speech_copy:
            for num in npc_speech_numbers:
                if num in sp[2]:
                    available_npc_speech.remove(sp)
                    break

        available_player_speech_numbers = [s[3] for s in available_npc_speech]

        request = 'SELECT player_number_speech, player_speech FROM speech WHERE ' \
                  'location = "{}" AND level = "{}" AND npc = "" AND player_number_speech IN ({})' \
            .format(dialog.location, dialog.level, str(available_player_speech_numbers)[1:-1])

        self.cur.execute(request)
        return list(self.cur.fetchall())

    def set_speech_is_completed(self, dialog):
        request = 'UPDATE speech SET is_completed = "1" WHERE ' \
                  'location = "{}" AND level = "{}" AND player_number_speech = "{}" ' \
                  'AND npc_number_speech = "{}"'.format(dialog.location, dialog.level, dialog.current_player_speech[0],
                                                        dialog.current_npc_speech[0])
        self.cur.execute(request)

        request = 'SELECT alternatives FROM speech WHERE location = "{}" AND level = "{}" ' \
                  'AND npc_number_speech = "{}"'.format(dialog.location, dialog.level, dialog.current_npc_speech[0])

        self.cur.execute(request)
        try:
            alternatives = self.cur.fetchall()[0][0]
        except IndexError:
            alternatives = list()
        if alternatives:
            alternatives = alternatives.split(' ')
        for npc_number_speech in alternatives:
            request = 'UPDATE speech SET is_canceled = "1" WHERE ' \
                      'location = "{}" AND level = "{}" AND npc_number_speech = "{}"'\
                .format(dialog.location, dialog.level, npc_number_speech)
            self.cur.execute(request)

        self.commit()

    def clear_is_completed(self):
        self.cur.execute('UPDATE speech SET is_completed = "0" WHERE npc_number_speech != "-1"')

    def commit(self, *l):
        self.con.commit()

    def table_is_empty(self, table='speech'):
        request = 'SELECT COUNT(*) as count FROM {}'.format(table)
        self.cur.execute(request)
        return self.cur.fetchall()[0][0] == 0

    def delete_table(self, table='speech'):
        self.cur.execute('DROP TABLE IF EXISTS {}'.format(table))
        self.commit()


db = Database()
