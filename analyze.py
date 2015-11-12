import csv
import datetime
import time
from dateutil import parser
from datetime import date, timedelta
import operator


def convert_to_datetime(timestampString):
	datetime = parser.parse(timestampString)
	return datetime


articleURLS = []
subjectKeywords = {}


def create_datetime_dict(byMonth=True):
	dt_dict = {}
	for i in range(2006,2016):
		if byMonth:
			dt_dict[i] = {}
			for j in range(1,13):
				dt_dict[i][j] = 0
		else:
			dt_dict[i] = 0
	return dt_dict

#  0   1        2			3		 4			 5		6		  7			  8		 
# ID,URL,Category,Subcategory,Headline,Subheadline,Byline,Timestamp,TagsSubject,TagsState,TagsOrganization,TagsPeople,TagsEvent,TagsLocation

def populateTimeSeriesDictionary(dictionary, key, year, month=False):
	key = key.title().strip()
	if key not in dictionary:
		dictionary[key] = create_datetime_dict() if month!=False else create_datetime_dict(byMonth=False)
	if month==False:
		dictionary[key][year] += 1
	else:
		dictionary[key][year][month] += 1
	return dictionary


def stringarray_to_array(stringArray):
	return stringArray.replace("[u'","").replace("', u'",",").replace("']","").split(',')


tagsTimeseries = {}
tagsTimeseriesYearly = {}
tagsCount = {}

with open('articles.csv', 'rb') as f:
    reader = csv.reader(f)
    categorymapping = {'Category': 2, 'Authors': 6, 'Tags_Subjects': 8, 'Tags_States': 9, 'Tags_Orgs': 10, 'Tags_People': 11, 'Tags_Events': 12, 'Tags_Location': 13}
    for category in categorymapping.keys():
    	tagsTimeseries[category]= {"Summary-Total": create_datetime_dict()}
    	tagsTimeseriesYearly[category] = {"Summary-Total": create_datetime_dict(byMonth=False)}
    	tagsCount[category] = {}
    for row in reader:
    	timestamp = convert_to_datetime(row[7])
    	for category in categorymapping.keys():
    		for tag in stringarray_to_array(row[categorymapping[category]]):
    			tag = tag.replace("\n","").strip()
    			tagsTimeseries[category] = populateTimeSeriesDictionary(tagsTimeseries[category], tag, timestamp.year, timestamp.month)

    			tagsTimeseriesYearly[category] = populateTimeSeriesDictionary(tagsTimeseriesYearly[category], tag, timestamp.year)
    			tagsTimeseriesYearly[category] = populateTimeSeriesDictionary(tagsTimeseriesYearly[category], "Summary-Total", timestamp.year)
    			if tag not in tagsCount[category]:
    				tagsCount[category][tag] = 1
    			else:
    				tagsCount[category][tag] += 1


# Top SUBJECTS tags

def printMostPopularTags(d):
	for w in sorted(d, key=d.get, reverse=True):
	    print w, d[w]

printMostPopularTags(tagsCount['Tags_Subjects'])