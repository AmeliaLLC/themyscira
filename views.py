import sys

from BeautifulSoup import BeautifulSoup
from klein import resource, route
from twisted.internet.defer import succeed

import db


resource #Shut up pyflakes
pool = db.DBPool()

@route('/')
def admin_index(request):

    def callback(results):
        for crash in results:
            request.write(
                '<li><strong>%s</strong> %s</li>' % (str(crash[0]), str(crash[3])))
        request.write('</ul></body></html>')
        request.finish()
    request.write('<!DOCTYPE html><html><head><title>Roti</title></head><body><ul>')
    return pool.getCrashes().addCallback(callback)


@route('/crash', methods=['POST'])
def report_crash(request):
    xml = request.args.get('xmlstring', '')[0]
    crashes = BeautifulSoup(xml).findAll('crash')
    for crash in crashes:
        pool.insertCrashFromXML(crash)

    # TODO: this should return a meaningful error code
    return '<?xml version="1.0" encoding="UTF-8"?><result>0</result>'
