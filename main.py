#!/usr/bin/env python

# (c) 2015 MICHAEL KRAUSE, TJHSST CLASS OF 2018

# Now works with Ion!

import urllib2, json
import webapp2, logging

def timeToInt(formTime):
	hour = int(formTime[0:formTime.find(":")])
	minute = int(formTime[formTime.find(":")+1:])
	if (hour <= 4): hour += 12
	return (hour*60) + minute

def getSchedule():
	response = urllib2.urlopen('https://ion.tjhsst.edu/api/schedule?format=json')
	data = json.load(response)
	blocks = data['results']['day_type']['blocks']
	periodNames = [len(blocks)]
	for tmpPd in blocks:
		periodNames.append(
			{
				'name': tmpPd['name'],
				'startForm': tmpPd['start'],
				'endForm': tmpPd['end'],
				'startInt': timeToInt(tmpPd['start']),
				'endInt': timeToInt(tmpPd['end'])
			}
		)
	return json.dumps(periodNames)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json' 
		self.response.write(getSchedule())

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
