#!/bin/bash

TMPDIR=`mktemp -d`

seq 1 10|nc -l -p 9999 &


src/twister.py tcp:interface=localhost:9999 tcp:interface=localhost:8888 &
PID=$!

nc localhost 8888|tee $TMPDIR/test.out

seq 1 10|diff - $TMPDIR/test.out
if [ $? == 0 ];then
  echo Test OK
else
  echo Test Failed
fi

kill $PID
wait





