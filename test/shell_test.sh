#!/bin/bash

TMPDIR=`mktemp -d`

close() {
  kill $PID $TS1
  kill $TS1
}

trap close INT

( while [ 0 ]; do 
date|nc -l -p 9999
echo 'Step done'
sleep 3
done ) &
TS1=$!

../src/twister.py localhost 9999 &
PID=$!


sleep 15
close

wait





