#!/usr/bin/env python

# (c) 2015 MICHAEL KRAUSE, TJHSST CLASS OF 2018

import urllib2, json
import webapp2, logging

def timeToInt(time):
	hour = int(time[0:time.find(":")])
	minute = int(time[time.find(":")+1:])
	if (hour <= 4): hour += 12
	return (hour*60) + minute

def twelveHourify(time):
	hour = int(time[0:time.find(":")])
	minute = str(time[time.find(":")+1:])
	if(hour > 12): hour = hour%12
	return "{}:{}".format(hour, minute)

def getSchedule():
	response = urllib2.urlopen('https://ion.tjhsst.edu/api/schedule?format=json')
	data = json.load(response)
	blocks = data['results'][0]['day_type']['blocks']
	periodNames = [len(blocks)]
	for tmpPd in blocks:
		periodNames.append(
			{
				'name': tmpPd['name'],
				'startForm': twelveHourify(tmpPd['start']),
				'endForm': twelveHourify(tmpPd['end']),
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
], debug=False)
