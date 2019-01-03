#!/bin/bash
echo "Starting ffmpeg"
while ! ffmpeg "$@";do 
	echo "FFMpeg exited with error, retrying...."
done

