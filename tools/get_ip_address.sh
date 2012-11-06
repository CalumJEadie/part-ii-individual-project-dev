#!/bin/bash

# http://www.cyberciti.biz/tips/read-unixlinux-system-ip-address-in-a-shell-script.html

ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'

n=60
read -p "Waiting for $n seconds..." -t $n var
