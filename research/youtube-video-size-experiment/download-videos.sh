#!/bin/sh

out_dir=/tmp/youtube-video-size-experiment
[ -d $out_dir ] || mkdir $out_dir

# Test data - YouTube Music Top 30 Tracks - 08/02/2013
# http://www.youtube.com/music
videos='http://www.youtube.com/watch?v=QK8mJJJvaes
http://www.youtube.com/watch?v=9bZkp7q19f0
http://www.youtube.com/watch?v=HsfY8iFbYjE
http://www.youtube.com/watch?v=vNoKguSdy4Y
http://www.youtube.com/watch?v=T4cdfRohhcg
http://www.youtube.com/watch?v=kYtGl1dX5qI
http://www.youtube.com/watch?v=OpQFFLBMEPI
http://www.youtube.com/watch?v=ifRoMGG8Wvs
http://www.youtube.com/watch?v=D1gl46hh3sQ
http://www.youtube.com/watch?v=lWA2pjMjpBs
http://www.youtube.com/watch?v=JHDbvMtMsbg
http://www.youtube.com/watch?v=Ys7-6_t7OEQ
http://www.youtube.com/watch?v=bek1y2uiQGA
http://www.youtube.com/watch?v=xGPeNN9S0Fg
http://www.youtube.com/watch?v=cN4fNaUAMbA
http://www.youtube.com/watch?v=CqPU7NSVQwY
http://www.youtube.com/watch?v=e-fA-gBCkj0
http://www.youtube.com/watch?v=FOjdXSrtUxA
http://www.youtube.com/watch?v=bqIxCtEveG8
http://www.youtube.com/watch?v=-6YLi0GNBTk
http://www.youtube.com/watch?v=F90Cw4l-8NY
http://www.youtube.com/watch?v=WA4iX5D9Z64
http://www.youtube.com/watch?v=cOQDsmEqVt8
http://www.youtube.com/watch?v=G_miGclPFGs
http://www.youtube.com/watch?v=4aQDOUbErNg
http://www.youtube.com/watch?v=1y6smkh6c-0
http://www.youtube.com/watch?v=fwK7ggA3-bU
http://www.youtube.com/watch?v=dPKG1-3LXBs
http://www.youtube.com/watch?v=R4em3LKQCAQ
http://www.youtube.com/watch?v=7iHd6uOGqII'

for video in $videos; do
    youtube-dl --output "$out_dir/%(id)s.%(ext)s" $video &
done