#! /usr/bin/env python3

import cherrypy
from working_no_melody import MelodyController
#from cherrypy.lib.caching import tools
#from MelodyController import MelodyController

def start_service():
	
        mc = MelodyController()
        dispatcher = cherrypy.dispatch.RoutesDispatcher()
	
        dispatcher.connect('post_melody', '/', controller=mc, action='POST', conditions=dict(method=['POST']))
        dispatcher.connect('get_index', '/', controller=mc, action='GET', conditions=dict(method=['GET']))
        dispatcher.connect('get_key', '/:key', controller=mc, action='GET_KEY', conditions=dict(method=['GET']))
	
        #dispatcher.connect('get_melody', '/test/', controller=mc, action = 'POST_TEST', conditions=dict(method=['POST']))

        conf = { 'global' : {'server.socket_host': 'localhost',
        	'server.socket_port': 8080,},
                '/' : {'request.dispatch': dispatcher, 'tools.caching.on': False} }

        cherrypy.config.update(conf)
        app = cherrypy.tree.mount(None, config=conf)
        cherrypy.quickstart(app)


if __name__ == '__main__':
        start_service()
#        m2 = MelodyController()
#        m2.watsonSpeak("Hello", 10)
#        print(m2.POST())
