import os
import sqlite3

from twisted.enterprise.adbapi import ConnectionPool


DB_FILENAME = 'crashdb'

class DBPool(object):

    def __init__(self):
        if not os.path.exists(DB_FILENAME):
            database = sqlite3.connect(DB_FILENAME)
            curs = database.cursor()
            curs.execute('''CREATE TABLE crash (
                application text,
                bundle text,
                systemversion text,
                platform text,
                senderversion text,
                data text,
                user text,
                contact text,
                description text
            )''')
            database.commit()
            database.close()
        self.pool = ConnectionPool('sqlite3', DB_FILENAME)

    def insertCrashFromXML(self, xmlobject):
        query = 'INSERT INTO crash VALUES (?,?,?,?,?,?,?,?,?)'
        return self.pool.runQuery(query, (
            xmlobject.applicationname.text,
            xmlobject.bundleidentifier.text,
            xmlobject.systemversion.text,
            xmlobject.platform.text,
            xmlobject.senderversion.text,
            xmlobject.log.text,
            xmlobject.userid.text,
            xmlobject.contact.text,
            xmlobject.description.text
        ))

    def getCrashes(self):
        query = 'SELECT * FROM crash'
        return self.pool.runQuery(query)
