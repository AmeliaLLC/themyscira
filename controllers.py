from BeautifulSoup import BeautifulSoup
from klein import resource, route

import db
import template


resource #Shut up pyflakes
pool = db.DBPool()


@route('/')
def admin_index(request):

    def callback(crashes):
        request.write(template.render(
            'templates/admin_index.handlebars',
            {'crashes': crashes}
        ))
        request.finish()
    return pool.getCrashes().addCallback(callback)

@route('/crash', methods=['POST'])
def report_crash(request):
    xml = request.args.get('xmlstring', '')[0]
    crashes = BeautifulSoup(xml).findAll('crash')
    for crash in crashes:
        pool.insertCrashFromXML(crash)

    # TODO: this should return a meaningful error code
    return '<?xml version="1.0" encoding="UTF-8"?><result>0</result>'
