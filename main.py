#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#(c) 2015 MICHAEL KRAUSE, TJHSST CLASS OF 2018
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
        response = urllib2.urlopen('https://ion.tjhsst.edu/schedule/embed?iodine')
        html = response.read()
        table = html[html.find('<table class="bellschedule-table"'):html.find("</table>")]
        pdCount = table.count("<tr>")
        periodNames = []
        periodNames.append(pdCount)
        for x in range (0, pdCount):
           tmpPd = table[table.find("<th>")+4:table.find("</th>")]
           tmpTime = table[table.find("<td>")+4:table.find("</td>")]
           tmpStart = tmpTime[0:tmpTime.find(" - ")]
           tmpEnd = tmpTime[tmpTime.find(" - ")+3:]
           periodNames.append(dict([('name', tmpPd.replace(":", "")), ('startForm', tmpStart), ('endForm', tmpEnd), ('startInt', timeToInt(tmpStart)), ('endInt', timeToInt(tmpEnd))]))
           table = table[table.find("</tr>")+4:len(table)]
        jsonValues = json.dumps(periodNames)
        #print(jsonValues)
        return(jsonValues)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json' 
        self.response.write(getSchedule())

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
