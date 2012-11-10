#!/bin/sh

kill `ps a | grep omxplayer.bin | head -n 1 | awk '{print $1}'`
