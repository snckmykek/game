import sqlite3


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database_cubes.db')
        self.cur = self.con.cursor()
        self.sqlite_create_db()

    def close(self):
        self.cur.close()
        self.con.close()

    def sqlite_create_db(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS completed_levels(location TEXT,level TEXT,is_completed BOOLEAN)')

    def insert_completed_level(self, location, level, is_completed=True):
        self.cur.execute('INSERT INTO completed_levels VALUES("{0}","{1}","{2}")'.format(location, level, is_completed))
        self.con.commit()

    def get_levels(self, location, is_completed=True):
        request = 'SELECT level FROM completed_levels WHERE location = "{}" AND is_completed = "{}"'.format(location,
                                                                                                            is_completed)
        self.cur.execute(request)
        return [x[0] for x in self.cur.fetchall()]


db = Database()
