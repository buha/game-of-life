#!/bin/sh
# This script assumes imagemagick is installed
# and converts the latest generated
lastfolder=$(ls 'recordings' | tail -n 1)
cd "recordings/$lastfolder"
convert -delay 20 -loop 0 *png animation.gif
