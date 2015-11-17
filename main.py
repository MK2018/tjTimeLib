#!/usr/bin/env python
#
#
#(c) 2015 MICHAEL KRAUSE, TJHSST CLASS OF 2018
#
#Now works with Ion!
#
import json
import webapp2
import urllib2
import logging

def timeToInt(formTime):
	hour = int(formTime[0:formTime.find(":")])
	minute = int(formTime[formTime.find(":")+1:])
	if(hour <= 4):
		hour += 12
	ret = (hour*60)+minute
	return ret


def getSchedule():
        response = urllib2.urlopen('https://ion.tjhsst.edu/schedule/embed')
        html = response.read()
        table = html[html.find('<table class="bellschedule-table"'):html.find("</table>")]
        table = table[table.find('>'):]
        pdCount = table.count("<tr ")
        periodNames = []
        periodNames.append(pdCount)
        for x in range (0, pdCount):
           tmpPd = table[table.find("<tr ")+4:table.find('">')]
           name = tmpPd[tmpPd.find("data-block-name=")+17:tmpPd.find("data-block-start=")-2]
           name = name.strip()
           tmpStart = tmpPd[tmpPd.find("data-block-start=")+18:tmpPd.find("data-block-end=")-2]
           tmpStart = tmpStart.strip()
           tmpEnd = tmpPd[tmpPd.find("data-block-end=")+16:tmpPd.find("data-block-order=")-2]
           tmpEnd = tmpEnd.strip()
           periodNames.append(dict([('name', name), ('startForm', tmpStart), ('endForm', tmpEnd), ('startInt', timeToInt(tmpStart)), ('endInt', timeToInt(tmpEnd))]))
           table = table[table.find("</tr>")+4:len(table)]
        jsonValues = json.dumps(periodNames)
        return(jsonValues)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json' 
        self.response.write(getSchedule())

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
