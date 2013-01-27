import plistlib
import math
import time
from random import randint


def checkPosition(slots, elementHeight, elementWidth, top, left):
	for i in range(elementHeight):
		for j in range(elementWidth):
			if (slots[top + i][left + j] == 1):
				return True
	return False

def fillPosition(slots, elementHeight, elementWidth, top, left):
	for i in range(elementHeight):
		for j in range(elementWidth):
			slots[top + i][left + j] = 1

def findGoodPosition(slots, elementHeight, elementWidth, top, left, height, width):
	badPosition = True
	attempts = 0
	while badPosition and attempts < 1000:
		badPosition = checkPosition(slots, elementHeight, elementWidth, top, left)
		attempts += 1
		if badPosition:
			top = (top + (elementHeight / 2)) % (height - elementHeight)
		else:
			return [top, left]

def printArtists(artists, maxCount, minCount):

	minSize = 10
	charHeight = 1
	charWidth = .6

	width = 2500
	height= 3000

	slots = [[0 for y in range(width)] for x in range(height)]

	f = open('D:\Dropbox\Dropbox\Apps\iTunesLibraryVisualizer\output.html', 'w')
	f.write("<body background='bg.jpg'>")
	giveUps = 0
	successes = 0
	totalAttempts = 0
	oobs = 0
	for artist, scale in artists:
		if scale == 1:
			scale = minSize
		else:
			scale = (.5  + math.log(scale)) * minSize

		#Figure out the iehgt/width of this element
		elementHeight = int(math.ceil(charHeight * scale))
		elementWidth = int(math.ceil(charWidth * scale)) * len(artist)


		top =  height
		left = width
		while elementWidth + left > width:
			left = randint(0, width)
		while elementHeight + top > height:
			top = randint(0, height)

		position = findGoodPosition(slots, elementHeight, elementWidth, top, left, height, width)


		if position[0] > 0:
			fillPosition(slots, elementHeight, elementWidth, position[0], position[1])
			successes = successes + 1
			f.write("<div style='font-family: courier; font-weight: bold;position:absolute; top:" + str(position[0]) + "px; left:" + str(position[1]) + "px; font-size:" + str(scale) + "px'>" + artist.encode("utf8") + "</div>")
		else:
			print 'x, y, h, w', top, left, elementHeight, elementWidth
			print artist, scale
			giveUps = giveUps + 1
	f.close()
	print 'totalAttempts', totalAttempts
	print 'oobs', oobs
	print 'successes', successes
	print 'giveups', giveUps

	f = open('D:\Dropbox\Dropbox\Apps\iTunesLibraryVisualizer\slots.txt', 'w')

	for line in slots:
		for char in line:
			f.write(str(char))
		f.write('\n')
	f.close()

plist = plistlib.readPlist('D:\Dropbox\Dropbox\Apps\iTunesLibraryVisualizer\Library.xml')

print 'done with load' + str(time.time())

tracks = plist['Tracks']
artistTrackCounts = {}
ARTIST = 'Artist'
for key, track in tracks.items():
	if track.has_key(ARTIST):
		if artistTrackCounts.has_key(track[ARTIST]):
			artistTrackCounts[track[ARTIST]] += 1
		else:
			artistTrackCounts[track[ARTIST]] = 1

artistList = []
for artist, count in artistTrackCounts.items():
	artistList.append([artist, count])

artistList = sorted(artistList, key=lambda someArtist: someArtist[1])

maxCount = artistList[0][1]
minCount = artistList[-1][1]

printArtists(reversed(artistList), maxCount, minCount)