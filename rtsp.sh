#!/bin/bash -x
HOST=localhost:5554
source param.sh
#ffmpeg -i cake.png -rtsp_transport tcp -i $rtsp_stream -tune zerolatency -filter_complex "overlay=10:10" -vcodec libx264 -pix_fmt + -c:v copy -c:a aac -strict experimental -f $dest
ffmpeg  -f lavfi -i anullsrc -i cake.png -rtsp_transport tcp -i $rtsp_stream -tune zerolatency -f $dest
