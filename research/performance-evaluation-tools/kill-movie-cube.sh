#!/bin/sh

kill `ps a | grep MovieCube | head -n 1 | awk '{print $1}'`
