import sys

from BeautifulSoup import BeautifulSoup
from twisted.internet import reactor
from twisted.python import log
from twisted.web import server, resource

import db


log.startLogging(sys.stdout)
pool = db.DBPool()

class CrashEndpoint(resource.Resource):
    '''The crash uploading endpoint.'''

    def render_POST(self, request):
        soup = BeautifulSoup(request.args['xmlstring'][0]);
        for _crash in soup.findAll('crash'):
            crash = db.Crash(_crash)
            pool.insertCrash(crash)


class AdminEndpoint(resource.Resource):
    '''The admin endpoint.'''

    def render_GET(self, request):
        def callback(results):
            for crash in results:
                request.write(
                    '<li><strong>%s</strong> %s</li>' % (str(crash[0]), str(crash[3])))
            request.write('</ul></body></html>')
            request.finish()
        pool.getCrashes().addCallback(callback)
        request.write('<html><head><title>Crashes</title></head><body><ul>')
        return server.NOT_DONE_YET

root = resource.Resource()
root.putChild('', CrashEndpoint())
root.putChild('crash', CrashEndpoint())
root.putChild('admin', AdminEndpoint())

site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()
