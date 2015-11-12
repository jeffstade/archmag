# Jeff Stern
# Scrapes Architecture Mag

from bs4 import BeautifulSoup
from urllib import FancyURLopener

import urllib2
import os
import re
import csv
import sys
import datetime
import time
from dateutil import parser
from datetime import date, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

def parse_html(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	content = response.read()
	return BeautifulSoup(content, "html.parser")

def get_current_date_string():
	return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

def get_images(site):
	media = site.find("div","media")
	images = []
	if media:
		images = media.find_all("img")
		photoset = media.find("iframe","photoset")
		if photoset:
			photosetPage = parse_html(photoset['src'])
			images = images + photosetPage.find_all("img")
	return images

def get_copy(site):
	return site.find("div","copy")

def convert_to_plain_text(copy):
	return copy.text

def get_all_attr(elementList, attr):
	return [a[attr] for a in elementList]

def get_tags(site):
	tags = site.find("dl","tags")
	if tags:
		return [a.text for a in tags.find_all("a")]
	else:
		return []

def convert_to_datetime(timestampString):
	datetime = parser.parse(timestampString)
	return datetime


## GET ALL ARTICLE URLS

f = open("articlelist.csv","wb")
output = csv.writer(f)


i = 0
total = 10180

while i <= total:
	site = parse_html("http://www.architectmagazine.com/latest-featured-articles?offset="+str(i))
	urls = site.find_all("a","headline2")
	for url in urls:
		print(url['href'])
		output.writerow([url['href']])
	print(i)
	i += 10

f.close()


## CREATING POSTS TABLE

articleURLS = []
with open('articlelist.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	articleURLS.append(row[0])

f = open("articles.csv", "wb")
output = csv.writer(f)
i = 2602
for articleURL in articleURLS[i:]:
	site = parse_html(articleURL)
	headline = site.find("h1","headline2").text
	altHeadline = site.find("h3","headline3").text if site.find("h3","headline3") else ""
	section = site.find("h4","section-title").text if site.find("h4","section-title") else ""
	eyebrow = site.find("span","eyebrow").text if site.find("span","eyebrow") else ""
	byline = ""
	if site.find("div","byline"):
		if site.find("div","byline").find("a"):
			byline = site.find("div","byline").find("a").text
		else:
			byline = site.find("div","byline").text
	timestamp = convert_to_datetime(site.find("time")['datetime']) if site.find("time") else ""
	#content = site.find("div","article-body")
	#contentNoHTML = content.text
	#contentHTML = str(content)
	tagCategs = site.find("div","article-tags").find_all("dt") if site.find("div","article-tags") else []
	possibleTagTypes = ['Subject', "Organization","People","Event","Location","State"]
	allTags = {'Subject': [], 'Organization': [], 'People': [], 'Event': [], 'Location': [], 'State': []}
	for categ in tagCategs:
		tags = categ.parent.find_all("dd")
		for tag in tags:
			allTags[categ.text[:-1]].append(tag.text) 

	data = [i, articleURL, section, eyebrow, headline, altHeadline, byline, timestamp, str(allTags['Subject']), str(allTags['State']), str(allTags['Organization']), str(allTags['People']), str(allTags['Event']), str(allTags['Location'])]
	output.writerow([unicode(s).encode("utf-8") for s in data])
	print(i)
	i += 1
f.close()