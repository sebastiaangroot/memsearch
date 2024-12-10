#!/bin/bash

if [ $# -ne 1 ]; then
  echo "usage: $0 <search_string>"
  echo " search_string formats:"
  echo '  0xdeadbeef    - search for hex string "deadbeef"'
  echo '  Lsearchstring - search for literal string "searchstring"'
  exit 1
fi

if [ $(id -u) -ne 0 ]; then
  echo "[!] you probably want to run this as root" 1>&2
fi

PIDS=$(ps -eo pid | grep -oE "[0-9]+")
for pid in $PIDS; do
  if [ -n "$pid" ]; then
    ./memsearch.py "$pid" "$1"
  fi
done
