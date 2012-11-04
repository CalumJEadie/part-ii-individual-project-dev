#!/bin/sh

JOGAMP_DIR=/opt/diss/jogamp

# Based on instructions from Xerxes

# Prepare install location
rm -rfv $JOGAMP_DIR
mkdir -v $JOGAMP_DIR

# Download and install
sudo apt-get install openjdk-7-jre p7zip-full libav-tools junit4
wget http://jogamp.org/deployment/archive/master/gluegen_600-joal_366-jogl_833-jocl_691-signed/archive/jogamp-all-platforms.7z -O /tmp/jogamp.7z
7z x /tmp/jogamp.7z -o$JOGAMP_DIR
