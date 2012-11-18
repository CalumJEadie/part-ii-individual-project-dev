#!/bin/bash

# YouTube Download Experiment.
# Times how long it takes to download a video from YouTube.

if [ $# != 2 ]; then
    echo "Usage: `basename $0` <format> <youtube url>"
    exit 1
fi

url=`youtube-dl --get-url --format $1 $2`
temp_file=`mktemp`
time wget -O $temp_file \'$url\'
