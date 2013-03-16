#!/bin/sh

kill `ps ax | grep test_editor.py | head -n 1 | awk '{print $1}'`
