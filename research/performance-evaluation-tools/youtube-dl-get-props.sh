#!/bin/sh

youtube-dl --get-title $1
youtube-dl --list-formats $1
