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

    def create_table(self, name, field_names, field_types):
        fields = ', '.join([f'{fname} {ftype}' for fname, ftype in zip(field_names, field_types)])
        self._curs.execute("CREATE TABLE {} (:fields)".format(self._scrub(name)), {'fields': fields})

    def insert_data(self, table, data):
        if self._is_plain_list(data):
            self._curs.execute(
                "INSERT INTO {} VALUES ({})".format(self._scrub(table), ', '.join("'{}'".format(i) for i in data))
            )
        else:
            self._curs.executemany(
                "INSERT INTO {} VALUES ({})".format(self._scrub(table), ','.join(['?']*len(data[0]))), data
            )
        self._conn.commit()

    def update_data(self, table, set_field, set_data, where_field, where_data):
        self._curs.execute(
            "UPDATE {} SET {} = :set_data' WHERE {} = :where_data".format(
                self._scrub(table), self._scrub(set_field), self._scrub(where_field)
            ),
            {'set_field': set_data, 'where_field': where_data}
        )
        self._conn.commit()

    def delete_data(self, table, where_field, where_data):
        self._curs.execute(
            "DELETE FROM {} WHERE {} = :where_data".format(
                self._scrub(table), self._scrub(where_field)
            ),
            {'where_field': where_data}
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
        return ''.join(c for c in string if c.isalnum())
