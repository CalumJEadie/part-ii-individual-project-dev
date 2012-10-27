# Must be run from JOGL directory.

java -cp jar/jogl-all.jar:jar/gluegen-rt.jar:/usr/share/java/junit4.jar:jar/jogl-test.jar \
com/jogamp/opengl/test/junit/jogl/demos/es2/av/MovieCube \
-time 400000 -width 1980 -height 1080
