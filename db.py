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

    def insertCrash(self, crash):
        query = 'INSERT INTO crash VALUES (?,?,?,?,?,?,?,?,?)'
        return self.pool.runQuery(query, (
            crash.application,
            crash.bundle,
            crash.systemversion,
            crash.platform,
            crash.senderversion,
            crash.data,
            crash.user,
            crash.contact,
            crash.description
        ))

    def getCrashes(self):
        query = 'SELECT * FROM crash'
        return self.pool.runQuery(query)


class Crash(object):

    def __init__(self, soup):
        self.application = soup.applicationname.text
        self.bundle = soup.bundleidentifier.text
        self.systemversion = soup.systemversion.text
        self.platform = soup.platform.text
        self.senderversion = soup.senderversion.text
        self.data = soup.log.text
        self.user = soup.userid.text
        self.contact = soup.contact.text
        self.description = soup.description.text

