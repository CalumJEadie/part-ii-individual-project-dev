#!/bin/sh

if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` <stats file>"
  exit 1
fi

callgraph=`mktemp -t callgraph`.svg
python gprof2dot.py -f pstats $1 | dot -Tsvg -o $callgraph
open -a Google\ Chrome $callgraph