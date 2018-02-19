#!/bin/bash
source param.sh
socat -d TCP-LISTEN:$PORT,reuseaddr,fork TCP:$HOST
