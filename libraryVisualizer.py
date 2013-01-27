import plistlib
import math
import time
import sys
import os.path
from random import randint

PAGE_WIDTH = 2540
MIN_FONT_SIZE = 10
VISIBLE_FONT_HEIGHT = 6
VISIBLE_FONT_WIDTH = 3
CHARACTER_HEIGHT = 1
CHARACTER_PAGE_WIDTH = .6
DENSITY = .70
FULL = 1
EMPTY = 0
LIBRARY_FILE = 'Library.xml'
OUTPUT_FILE = 'output.html'

def main(argv):
	global LIBRARY_FILE, PAGE_WIDTH, OUTPUT_FILE
	argv.pop(0)
	argv += [None]
	opts = zip(argv[0::2], argv[1::2]) 
	for opt, arg in opts:
		if opt == '-w' and arg.isdigit(): PAGE_WIDTH = int(arg)
		elif opt == '-d' and arg.isdigit(): DENSITY = float(arg)
		elif opt == '-l': LIBRARY_FILE = arg
		elif opt == '-o': OUTPUT_FILE = arg
		else: 
			showHelp()
			return

	for path in [LIBRARY_FILE, OUTPUT_FILE]:
		if '/' not in path and '\\' not in path: path = os.getcwd() +  '\\' + path

	print 'Starting load...', time.time()
	plist = plistlib.readPlist(LIBRARY_FILE)
	print 'Load complete', time.time()
	artistTrackCounts = countTracksPerArtist(plist['Tracks'])
	print 'Tracks counted', time.time()

	#Scale the entries so that the differences in proportion are reasonable
	artistList, volume = scaleEntries(artistTrackCounts)
	print 'Entries scaled', time.time()

	#Sort the list from largest to smallest so that we can place the big elements first
	artistList = sorted(artistList, key=lambda someArtist: someArtist[1], reverse=True)
	print 'List sorted', time.time()
	maxCount, minCount = artistList[-1][1], artistList[0][1]
	printArtists(artistList, maxCount, minCount, volume)

def showHelp():
	print 'Valid Arguments:'
	print '-w [width of the generated page, in pixels]'
	print '-d [The density of the words. Recommend between .5 and .7]'
	print '-o [The folder you want the output placed in. Default is current directory]'
	print '-l [Full path to your library file/filename.xml, or just filename if in current directory. Default is Library.xml in current directory]'

def isSubmatrixEmpty(matrix, top, left, elementHeight, elementWidth):
	for i in range(0, elementHeight, VISIBLE_FONT_HEIGHT):
		for j in range(0, elementWidth, VISIBLE_FONT_WIDTH):
			if (matrix[top + i][left + j] == FULL): return False
	return True

def fillSubmatrix(matrix, top, left, elementHeight, elementWidth):
	for i in range(elementHeight):
		for j in range(elementWidth):
			matrix[top + i][left + j] = FULL

def findEmptySubmatrix(matrix, pageHeight, PAGE_WIDTH, elementHeight, elementWidth):
	badPosition = True
	attempts = 0

	top, left =  pageHeight, PAGE_WIDTH
	while elementWidth + left > PAGE_WIDTH: left = randint(0, PAGE_WIDTH)
	while elementHeight + top > pageHeight: top = randint(0, pageHeight)

	#Move the element around the matrix until we find a spot that is empty
	for i in range(pageHeight / elementHeight):
		for j in range(PAGE_WIDTH / elementWidth):
			if isSubmatrixEmpty(matrix, top, left, elementHeight, elementWidth):
				return [top, left]
			else:
				left = (left + elementWidth) % (PAGE_WIDTH - elementWidth)
		top = (top + elementHeight) % (pageHeight - elementHeight)
	#Failure :(
	return [-1, -1]

def printArtists(artists, maxCount, minCount, volume):

	f = open(OUTPUT_FILE, 'w+')
	f.write("<body background='bg.jpg'>")
	successes = 0
	failures = 0

	pageHeight = int(math.ceil(volume / DENSITY / PAGE_WIDTH))
	matrix = [[EMPTY for y in range(PAGE_WIDTH)] for x in range(pageHeight)]
	print 'Matrix initialized', time.time()

	for artist, scale in artists:
		elementHeight, elementWidth = int(math.ceil(CHARACTER_HEIGHT * scale)), int(math.ceil(CHARACTER_PAGE_WIDTH * scale)) * len(artist)
		top, left = findEmptySubmatrix(matrix, pageHeight, PAGE_WIDTH, elementHeight, elementWidth)

		if top > -1:
			fillSubmatrix(matrix, top, left, elementHeight, elementWidth)
			successes += 1
			f.write("<div style='font-family: courier; font-weight: bold;position:absolute; top:" 
				+ str(top) + "px; left:" + str(left) + "px; font-size:" + str(scale) + "px'>" + artist.encode("utf8") + "</div>")
		else:
			failures += 1
	f.close()
	print 'Page generated', time.time()
	print 'Placed', successes, 'elements'
	print 'Failures ', failures
	availableVolume = pageHeight * PAGE_WIDTH
	print 'Available Volume', availableVolume
	print 'Required Volume', volume
	print 'Percent Used', float(volume) / availableVolume

def scaleEntries(artistTrackCounts):
	artistList = []
	volume = 0

	for artist, count in artistTrackCounts.items():
		if count == 1: count = MIN_FONT_SIZE
		else: count = (.5  + math.log(count)) * MIN_FONT_SIZE
		elementHeight = int(math.ceil(CHARACTER_HEIGHT * count))
		elementWidth = int(math.ceil(CHARACTER_PAGE_WIDTH * count)) * len(artist)
		volume += elementHeight * elementWidth
		artistList.append([artist, count])
	return artistList, volume

def countTracksPerArtist(tracks):
	counts = {}

	for key, track in tracks.items():
		if track.has_key('Artist'):
			if counts.has_key(track['Artist']): counts[track['Artist']] += 1
			else: counts[track['Artist']] = 1
	return counts

main(sys.argv)
