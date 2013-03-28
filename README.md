iTunes Frequency Mapper
=======
This script reads an iTunes Library.xml file and creates an html page
which displays the name of each artist in a randomized location, scaled
by the number of tracks by each artist.

See sample_output.html for an example of the end result.

Usage
-----

Run the script by placing it in the same directory as an iTunes Library.xml
file and use the following command:

	python FrequencyMapMaker.py

This will create a file called output.html in the same directory with the results.

The following command line arguments provide some additional flexibility:

	-w [the width, in pixels, of the generated page. Default: 1880]
	-d [the density of the text. .7 is default. .5 <= x <= .75 recommended]
	-l [Full path to Library.xml. If not given, script looks in same directory]
	-o [Full path to place output.html. If not given, will be same directory]
