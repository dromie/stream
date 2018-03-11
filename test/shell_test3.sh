#!/bin/bash

TMPDIR=`mktemp -d`

close() {
  kill $PID $TS1
  kill $TS1
}

trap close INT

( while [ 0 ]; do 

( while [ 0 ]; do 
date
echo 'Step done'
sleep 1
done )|nc -l -p 9999 &
echo $! >$TMPDIR/nc.pid
wait
done ) &

TS1=$!

../src/twister.py localhost 9999 "$PWD/testclient,{host},{port}" &
PID=$!

sleep 3

kill `cat $TMPDIR/nc.pid`

sleep 5

kill `cat $TMPDIR/nc.pid`

sleep 8

kill `cat $TMPDIR/nc.pid`


wait





