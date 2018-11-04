import cherrypy
import re, json
class DictionaryController(object):
	def __init__(self):
		self.myd = dict()
	def GET(self, key):
		output = {}
		try:
			output['result'] = 'success'
			val = self.myd[key]
			output['key'] = str(key)
			output['value'] = val
		except KeyError as ex:
			output['result'] = 'error'
			output['message'] = 'key not found'
		
		return json.dumps(output)

	def DELETE_INDEX(self):
		try:
			self.myd = {}
		except:
			return json.dumps({"result": "error"})
		return json.dumps({"result": "success"})

	def DELETE(self, key):
		try:
			self.myd.pop(key)
		except:
			return json.dumps({"result": "error"})
		return json.dumps({"result": "success"})


	def GET_INDEX(self):
		try:
			ret = {}
			ret['result'] = "success"
			ret['entries'] = []
			for i in self.myd:
				ret['entries'].append({"key": i, "value": self.myd[i]})
		except:
			json.dumps({"result": "error"})
		return json.dumps(ret)

	def POST(self):
		try:
			payload = cherrypy.request.body.read()
			payload = json.loads(payload)
			self.myd[str(payload['key'])] = str(payload['value'])
		except:
			json.dumps({"result": "error"})
		return json.dumps({"result":"success"})

	def PUT(self, key):
		try:
			payload = cherrypy.request.body.read()
			payload = json.loads(payload)
			self.myd[str(key)] = str(payload['value'])
		except:
			json.dumps({"result": "error"})
		return json.dumps({"result":"success"})
