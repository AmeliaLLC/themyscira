from BeautifulSoup import BeautifulSoup
from klein import resource, route
from twisted.internet.defer import DeferredList
from twisted.web.static import File

import db
from template import render


resource #Shut up pyflakes

@route('/crash/<int:crashID>')
def view_crash(request, crashID):
    def callback(crash):
        request.write(
            render('templates/view_crash.handlebars', {'crash': crash})
        )
    return db.Crash.find(id=crashID).addCallback(callback)

@route('/crash', methods=['POST'])
def report_crash(request):
    def finishRequest(_):
        # TODO: this should return a meaningful error code
        request.write(
            '<?xml version="1.0" encoding="UTF-8"?><result>0</result>')

    xml = request.args.get('xmlstring', '')[0]
    crashes = BeautifulSoup(xml).findAll('crash')

    deferreds = []
    for crashXML in crashes:
        crash = db.Crash(
            applicationname=crashXML.applicationname.text,
            bundleidentifier=crashXML.bundleidentifier.text,
            contact=crashXML.contact.text,
            description=crashXML.description.text,
            log=crashXML.log.text,
            platform=crashXML.platform.text,
            senderversion=crashXML.senderversion.text,
            systemversion=crashXML.systemversion.text,
            user=crashXML.userid.text,
            version=crashXML.version.text
        )
        deferreds.append(crash.save())
    deferredList = DeferredList(deferreds)
    return deferredList.addCallback(finishRequest)

@route('/static/')
def assets(request):
    return File('static')

@route('/')
def admin_index(request):
    def callback(crashes):
        request.write(
            render('templates/admin_index.handlebars', {'crashes': crashes})
        )
    return db.Crash.all().addCallback(callback)

