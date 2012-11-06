# Streams video directly from YouTube.
# Must be run from JOGL root direcotry.

# Usage: _ <format> <youtube url>

if [ $# -ne 2 ]
then
	echo "Usage: `basename $0` <format> <youtube url>

See youtube-dl --format parameter for format codes"
	exit 1
fi

# Get the url for streaming the video.
stream_url=`youtube-dl -f $1 -g $2`

echo "Streaming from $stream_url"

java -cp jar/jogl-all.jar:jar/gluegen-rt.jar:/usr/share/java/junit4.jar:jar/jogl-test.jar \
com/jogamp/opengl/test/junit/jogl/demos/es2/av/MovieCube \
-time 400000 -width 1980 -height 1080 -url $stream_url
