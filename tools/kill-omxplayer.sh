#!/bin/sh

kill `ps ax | grep omxplayer.bin | head -n 1 | awk '{print $1}'`
