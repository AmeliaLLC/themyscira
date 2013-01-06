from datetime import datetime
import os
import sqlite3

from twistar.registry import Registry
from twistar.dbobject import DBObject
from twisted.enterprise import adbapi

__all__ = ('Crash',)

DB_FILENAME = 'crashdb'
Registry.DBPOOL = adbapi.ConnectionPool('sqlite3', DB_FILENAME)
if not os.path.exists(DB_FILENAME):
    commands = []
    commands.append('''
    CREATE TABLE crash (
        applicationname TEXT NOT NULL,
        bundleidentifier TEXT NOT NULL,
        contact TEXT NOT NULL,
        description TEXT NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log TEXT NOT NULL,
        platform TEXT NOT NULL,
        senderversion TEXT NOT NULL,
        systemversion TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        user TEXT NOT NULL,
        version TEXT NOT NULL
    );''')
    commands.append(
        'CREATE INDEX bundleidentifier_idx ON crash (bundleidentifier);')
    commands.append('CREATE INDEX platform_idx ON crash (platform);')
    commands.append('CREATE INDEX senderversion_idx ON crash (senderversion);')
    commands.append('CREATE INDEX timestamp_idx ON crash (timestamp);')

    # TODO: This should probably use Registry.DBPOOL.runQuery
    database = sqlite3.connect(DB_FILENAME)
    curs = database.cursor()
    for command in commands:
        curs.execute(command)
    database.commit()
    database.close()

class _DBObject(DBObject):

    def get(self, key, *args, **kwargs):
        return self.__dict__.get(key, None)

class Crash(_DBObject):

    TABLENAME = 'crash'

    def beforeSave(self):
        self.timestamp = datetime.now()

