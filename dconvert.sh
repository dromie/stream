#!/bin/bash -x
#HOST=localhost:5554
source param.sh
#ffmpeg -i cake.png -rtsp_transport tcp -i $rtsp_stream -tune zerolatency -filter_complex "overlay=10:10" -vcodec libx264 -pix_fmt + -c:v copy -c:a aac -strict experimental -f $dest
docker run --name ffmpeg-convert -v $PWD:/data jrottenberg/ffmpeg -f lavfi -i anullsrc -loop 1 -f image2 -i /data/logo.jpg  -c:a aac -c:v libx264 -x264-params keyint=60 -r 60 -g 300 -bufsize 500k /data/test.mp4
