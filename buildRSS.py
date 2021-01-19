"""
buildRSS.py v0.95.1
Used to build an RSS feed by scrapping the working directory for recent html files
Assembles the html files by last modified, includes up to 50 entries

v 0.95
Updated to pull first paragraph and second image into the body of the RSS entry

v 0.95.1
Stripped .html for article titles

Credits:
Uses PyRSS2Gen copyright (c) by Andrew Dalke Scientific, AB BSD license
Uses BeautifulSoup MIT license
"""

import os
import datetime
import PyRSS2Gen as buildrss
from bs4 import BeautifulSoup

print("\nRaw Files:\n")

files = os.scandir(".")
lastTime = 0
highestTime = 0
highestElement = 0
orderedList = []
orderedDates = []

for i in range(50):
    for time in os.scandir("."):
        timestamp = os.path.getmtime(time)
        if (timestamp < lastTime or lastTime == 0) and timestamp > highestTime:
            highestTime = timestamp
            highestElement = time

    if highestTime == 0:
        break;
    lastTime = highestTime
    print(highestElement.name, highestTime)
    highestTime = 0

    if(highestElement.name.endswith('.html')):
        orderedList.append(highestElement.name)
        orderedDates.append(datetime.datetime.fromtimestamp(lastTime))
    else:
        i = i - 1

print("\n Ordered Files: \n")

for i in range(len(orderedList)):
    print(orderedList[i], orderedDates[i])

print("\n Generated Descriptions: \n")

orderedDescriptions = []
for i in orderedList:
    soup = BeautifulSoup(open(i), 'html.parser')
    ptag = soup.find("p")
    if ptag:
        ptag = ptag.string
    else:
        ptag = ""
    image = soup.find_all("img")
    if len(image) > 1:
        image = "<a href=\"" + i + "\"" + "> <img src=\" https://jatas.org/" + image[1].get("src") + "\" ></a>"
    else:
        image = ""
    orderedDescriptions.append((image + ptag))

for i in orderedDescriptions:
    print(i)

i = 0
orderedGeneratedItems = []
for files in orderedList:
    linkName = "https://jatas.org/" + files
    orderedGeneratedItems.append( buildrss.RSSItem(
        title=files.rsplit(".")[0],
        link=linkName,
        pubDate=orderedDates[i],
        description=orderedDescriptions[i]
    ))
    i = i + 1

rss = buildrss.RSS2(
    title="JATAS",
    link="https://jatas.org",
    description="The personal website of Alec Jackson and Ryan Taylor",
    language="en-us",
    image=buildrss.Image(
        url="https://jatas.org/images/JTIconRSS.png",
        title="JATAS",
        link="https://jatas.org"
    ),
    lastBuildDate=datetime.datetime.now(),
    items=orderedGeneratedItems
)

print()
rss.write_xml(open("RSS.xml", "w"))
