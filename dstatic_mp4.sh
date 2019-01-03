#!/bin/bash -x
#HOST=localhost:5554
source param_mine.sh
#ffmpeg -i cake.png -rtsp_transport tcp -i $rtsp_stream -tune zerolatency -filter_complex "overlay=10:10" -vcodec libx264 -pix_fmt + -c:v copy -c:a aac -strict experimental -f $dest
docker run --name ffmpeg-static_mp4 -v $PWD:/data jrottenberg/ffmpeg -re -stream_loop -1 -i /data/input.ts -c copy -bsf:a aac_adtstoasc -f $dest
