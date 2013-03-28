import plistlib
import math
import time
import sys
import os.path
from random import randint

#Consider constant, can only be changed by command line arg.
PAGE_WIDTH = 1880
LIBRARY_FILE = 'Library.xml'
OUTPUT_FILE = 'output.html'
DENSITY = .70

#True constants
MIN_FONT_SIZE = 10
VISIBLE_FONT_HEIGHT = 6
VISIBLE_FONT_WIDTH = 3
CHARACTER_HEIGHT = 1
CHARACTER_PAGE_WIDTH = .6
FULL = 1
EMPTY = 0

def isfloat(obj):
	try:
		float(obj)
		return True
	except:
		return False

def main(argv):
	global LIBRARY_FILE, PAGE_WIDTH, OUTPUT_FILE, DENSITY
	argv.pop(0)
	argv += [None]
	opts = zip(argv[0::2], argv[1::2])
	for opt, arg in opts:
		if opt == '-w' and arg.isdigit():
			PAGE_WIDTH = int(arg)
		elif opt == '-d' and isfloat(arg):
			DENSITY = float(arg)
		elif opt == '-l':
			LIBRARY_FILE = arg
		elif opt == '-o':
			OUTPUT_FILE = arg
		else:
			show_help()
			return

	for path in [LIBRARY_FILE, OUTPUT_FILE]:
		if '/' not in path and '\\' not in path:
			"%s\\%s" % (os.getcwd(), path)

	print 'Starting load...', time.time()
	tracks = plistlib.readPlist(LIBRARY_FILE)['Tracks']
	print 'Load complete', time.time()
	artist_track_counts = count_tracks_per_artist(tracks)
	artist_ratings = get_average_artist_rating(tracks)
	print 'Tracks counted', time.time()

	#Scale the entries so that the differences in proportion are reasonable
	artist_list, volume = scale_entries(artist_track_counts)
	print 'Entries scaled', time.time()

	#Sort the list from largest to smallest so that we can place the big elements first
	artist_list = sorted(artist_list, key=lambda artist: artist[1], reverse=True)
	print 'List sorted', time.time()
	max_count, min_count = artist_list[-1][1], artist_list[0][1]
	print_artists(artist_list, max_count, min_count, volume)

def get_average_artist_rating(tracks):
	ratings = {}
	for key, track in tracks.items():
		if track.has_key('Artist') and track.has_key('Rating'):
			artist = track['Artist']
			if ratings.has_key(artist):
				ratings[artist].append(track['Rating'])
			else:
				ratings[artist] = [track['Rating']]
	for artist, rating in ratings.items():
		ratings[artist] = sum(rating) / float(len(rating))
	print ratings


def count_tracks_per_artist(tracks):
	counts = {}

	for key, track in tracks.items():
		if track.has_key('Artist'):
			if counts.has_key(track['Artist']):
				counts[track['Artist']] += 1
			else:
				counts[track['Artist']] = 1
	return counts

def scale_entries(artist_track_counts):
	artist_list = []
	volume = 0

	for artist, count in artist_track_counts.items():
		if count == 1:
			count = MIN_FONT_SIZE
		else:
			count = (.5  + math.log(count)) * MIN_FONT_SIZE

		element_height = int(math.ceil(CHARACTER_HEIGHT * count))
		element_width = int(math.ceil(CHARACTER_PAGE_WIDTH * count)) * len(artist)
		volume += element_height * element_width
		artist_list.append([artist, count])

	return artist_list, volume

def print_artists(artists, max_count, min_count, volume):

	f = open(OUTPUT_FILE, 'w+')
	f.write("<body background='bg.jpg'>")
	successes = 0
	failures = 0

	page_height = int(math.ceil(volume / DENSITY / PAGE_WIDTH))
	matrix = [[EMPTY for y in range(PAGE_WIDTH)] for x in range(page_height)]
	print 'Matrix initialized', time.time()

	for artist, scale in artists:
		element_height = int(math.ceil(CHARACTER_HEIGHT * scale))
		element_width = int(math.ceil(CHARACTER_PAGE_WIDTH * scale)) * len(artist)
		top, left = find_empty_submatrix(
			matrix, page_height, PAGE_WIDTH, element_height, element_width)

		if top:
			fill_submatrix(matrix, top, left, element_height, element_width)
			successes += 1
			f.write(
				"<div style='font-family: courier; font-weight: bold;position:absolute; top:%dpx; left:%dpx; font-size:%dpx'>%s</div>"
				% (top, left, scale, artist.encode("utf8")))
		else:
			failures += 1
	f.close()
	print 'Page generated', time.time()
	print 'Placed', successes, 'elements'
	print 'Failures ', failures
	available_volume = page_height * PAGE_WIDTH
	print 'Available Volume', available_volume
	print 'Required Volume', volume
	print 'Percent Used', float(volume) / available_volume

def find_empty_submatrix(
	matrix, page_height, PAGE_WIDTH, element_height, element_width):

	top, left =  page_height, PAGE_WIDTH
	while element_width + left > PAGE_WIDTH: left = randint(0, PAGE_WIDTH)
	while element_height + top > page_height: top = randint(0, page_height)

	#Move the element around the matrix until we find a spot that is empty
	for i in range(page_height / element_height):
		for j in range(PAGE_WIDTH / element_width):

			if is_submatrix_empty(
					matrix, top, left, element_height, element_width):
				return [top, left]
			else:
				left = (left + element_width) % (PAGE_WIDTH - element_width)

		top = (top + element_height) % (page_height - element_height)
	return [None, None]

def is_submatrix_empty(matrix, top, left, element_height, element_width):
	for i in range(0, element_height, VISIBLE_FONT_HEIGHT):
		for j in range(0, element_width, VISIBLE_FONT_WIDTH):
			if (matrix[top + i][left + j] == FULL):
				return False
	return True

def fill_submatrix(matrix, top, left, element_height, element_width):
	for i in range(element_height):
		for j in range(element_width):
			matrix[top + i][left + j] = FULL

def show_help():
	print 'Valid Arguments:'
	print '-w [width of the generated page, in pixels]'
	print '-d [The density of the words. Recommend between .5 and .7]'
	print '-o [The folder you want the output placed in. Default is current directory]'
	print '-l [Full path to your library file/filename.xml, or just filename if in current directory. Default is Library.xml in current directory]'

if __name__ == '__main__':
    main(sys.argv)
