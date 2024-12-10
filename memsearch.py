#!/usr/bin/env python3

import re
import sys
import os
import binascii
from subprocess import PIPE, Popen

def get_mem(pid):
  with open(f"/proc/{pid}/maps", "r") as maps_file:
    memmap = maps_file.readlines()
  mem_file = open(f"/proc/{pid}/mem", "rb", 0)
  out_maps = {}
  for line in memmap:
    m = re.match('([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
    if m.group(3) == 'r':
      start = int(m.group(1), 16)
      end = int(m.group(2), 16)
      try:
        pos = mem_file.seek(start)
        chunk = mem_file.read(end - start)
        out_maps[line.strip()] = chunk
      except:
        continue
  mem_file.close()
  return out_maps

def get_proc_name(pid):
  assert(type(pid) == int)
  with Popen(f'ps -q {pid} -o comm=', shell=True, stdout=PIPE) as p:
    return p.communicate()[0].decode().strip()

def usage():
  print(f'usage: {sys.argv[0]} <pid> <search_string>')
  print(' search_string formats:')
  print('  0xdeadbeef    - search for hex string "deadbeef"')
  print('  Lsearchstring - search for literal string "searchstring"')


def main():
  if len(sys.argv) != 3:
    usage()
    exit(1)

  try:
    pid = int(sys.argv[1])
    search_string = sys.argv[2]
    if search_string.startswith('0x'):
      search_string = binascii.unhexlify(search_string[2:])
    elif search_string.startswith('L'):
      search_string = search_string[1:].encode()
    else:
      usage()
      exit(3)
  except:
    usage()
    exit(3)

  try:
    memmap = get_mem(pid)
  except:
    exit(2)
  for chunk in memmap.keys():
    idx = memmap[chunk].find(search_string)
    if idx >= 0:
      chunk_printable = re.sub(r'\s+', ' ', chunk)
      pname = get_proc_name(pid)
      print(f'[!] string found in pid [{pid} - {pname}] at chunk [{chunk_printable}] at idx 0x{idx:02x}')

if __name__ == '__main__':
  main()
