import sqlite3


class DB:
    # TODO:
    # try:
    #     execute(sql)
    # except sqlite3.DatabaseError as err:
    #     print("Error: ", err)
    # else:
    #     commit()

    def __init__(self, name=None):
        self._db = name
        self._conn = None
        self._curs = None

    def connect(self):
        if self._db:
            self._conn = sqlite3.connect(self._db)
            self._curs = self._conn.cursor()
        return self._db

    def close_connection(self):
        if self._conn:
            self._conn.close()

    def _sql(self, sql):
        self._curs.execute(sql)
        return self._curs.fetchall()

    def create_table(self, name, fields_tuple, ref_list=[]):
        fields = ', '.join(
            [f'"{fname}" {ftype} {fmody}' for fname, ftype, fmody in fields_tuple] + ref_list
        )
        self._curs.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(self._scrub(name), fields))

    def get_data(self, table, fields, where_cond=None):
        if where_cond:
            self._curs.execute(
                "SELECT {} FROM {} WHERE {}".format(
                    ', '.join(fields),
                    self._scrub(table),
                    where_cond
                )
            )
        else:
            self._curs.execute(
                "SELECT {} FROM {}".format(
                    ', '.join(fields),
                    self._scrub(table)
                )
            )
        return self._curs.fetchall()

    def insert_data(self, table, fields, data):
        if self._is_plain_list(data):
            self._curs.execute(
                "INSERT OR IGNORE INTO {} ({}) VALUES ({})".format(
                    self._scrub(table),
                    ', '.join([self._scrub(i) for i in fields]),
                    ', '.join("'{}'".format(self._scrub_data(i)) for i in data)),
            )
            self._conn.commit()
            self._curs.execute(
                "SELECT id FROM {} WHERE {} = '{}'".format(self._scrub(table), self._scrub(fields[0]), self._scrub_data(data[0]))
            )
            return self._curs.fetchall()[0][0]
        else:
            self._curs.executemany(
                "INSERT INTO {} ({}) VALUES ({})".format(
                    self._scrub(table),
                    ', '.join([self._scrub(i) for i in fields]),
                    ','.join(['?']*len(data[0]))), data
            )
            self._conn.commit()
            return None

    def update_data(self, table, set_field, set_data, where_field, where_data):
        self._curs.execute(
            "UPDATE {} SET {} = :set_data WHERE {} = :where_data".format(
                self._scrub(table), self._scrub(set_field), self._scrub(where_field)
            ),
            {'set_data': set_data, 'where_data': where_data}
        )
        self._conn.commit()

    def delete_data(self, table, where_field, where_data):
        self._curs.execute(
            "DELETE FROM {} WHERE {} = :where_data".format(
                self._scrub(table), self._scrub(where_field)
            ),
            {'where_data': where_data}
        )
        self._conn.commit()

    @staticmethod
    def _is_plain_list(data):
        for i in data:
            if isinstance(i, (list, tuple)):
                return False
        return True

    @staticmethod
    def _scrub(string):
        if isinstance(string, (int, float)) or string is None:
            return string
        return ''.join(c for c in string if c.isalnum() or c in ('_',))

    @staticmethod
    def _scrub_data(string):
        if isinstance(string, (int, float)) or string is None:
            return string
        return ''.join(c for c in string if c.isalnum() or c in ('_', ' '))

