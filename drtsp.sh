#!/bin/bash -x
#HOST=localhost:5554
source param.sh
#ffmpeg -i cake.png -rtsp_transport tcp -i $rtsp_stream -tune zerolatency -filter_complex "overlay=10:10" -vcodec libx264 -pix_fmt + -c:v copy -c:a aac -strict experimental -f $dest
docker run --name ffmpeg-rtsp ffmpeg-loop -f lavfi -i anullsrc -rtsp_transport tcp -i $rtsp_stream -tune zerolatency -vcodec mpeg4 -pix_fmt + -c:v copy -c:a aac -f $dest
