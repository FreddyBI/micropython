# micropython
micropython files

To start: 

import shell

-->

 0 lsr(path="/"):# Lists files recursive
 1 ls(path="/"):# Lists files
 2 cd(path="."):# Change directory
 3 cat(f,find=""):# Display file contents
 4 mkdir(target=""):# Create a directory
 5 pwd():# Display full pathname of the current working
 6 rm(f):# Remove a file
 7 run(f):# Run micropython code from file
 8 sys_info():# Display machine info
c execute micropython command
e ed()
h help()
lm print(dir()) # Loaded modules
m help('modules')
q quit
r from machine import reset;reset()
sd import uos;print(uos.listdir("/sd"))

Action? 
