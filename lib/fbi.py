from os import stat,listdir,mkdir
from random import randint
from uctypes import addressof

# ---- Basic file func ----
def exists(fname): # return False or True if filename exists
  try:
    with open(fname):
      pass
    return True
  except OSError:
    return False

def isfile(fname):  # return False or True if filename exists
  return exists(fname)

def isdir(path): # return False or True if path is a directory
  try:
    listdir(path)
    return True
  except:
    return False

def filecp(sfile, pfile, blocksize=4096): # copy sfile to pfile
  with open(sfile, 'rb') as sf:
    with open(pfile, 'w+') as pf:
      while pf.write(sf.read(blocksize)):
        pass

def filesize(fname): # return the file size from filname 
  if isfile(fname):
    return stat(fname)[6]
  else:
    return None

def makedirs(path): # create a directory
  _path = ''
  if path[0] == '/':
    path = path.strip('/').split('/')
    for i in path:
      _path += '/' + i
      try:
        mkdir(_path)
      except:
        pass
  else:
    path = path.split('/')
    for i in path:
      _path += i
      try:
        mkdir(_path)
        _path += '/'
      except:
        pass
    
# Find all function names from list starts with string, '' -> all
# Return list function names, [] if no names found
# Example print(funcstartswith(open("dir.py", 'r'),'f_'))
# Freddy Biesemans 25/09/2020

def funcstartswith(l,swith=''): # return function(s) (start with string) from filelines. Example print(funcstartswith(open("dir.py", 'r'),'f_'))
  lfn=[]
  for s in [line.strip() for line in l]:
    s=s.strip()
    if s[:4]=="def ":
      e=s[4:].find('(')
      if e > -1:
        n=s[4:4+e].strip()
        if n.startswith(swith):
          lfn.append(n)
  return lfn    

def map(x,in_min,in_max,out_min,out_max): # integer mapping with in_min,in_max values
  return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

def roundint(f) : # round float to int
  return int(f+0.5) if f > 0.0 else int(f-0.5)

def clamp(num, min_value, max_value): # limit the value in min_value and max_value
  num = max(min(num, max_value), min_value)
  return num

def rangepingpong(start, stop=None, step=None): # ping pong range generator
  p1=0 if stop is None else start
  p2=start if stop is None else stop
  p3=1 if step is None else step
  i=None
  for i in range(p1,p2,p3):
    yield i
  previ=i  
  if i is not None:
    for i in reversed(range(p1,p2,p3)):
      if not previ == i:
        yield i
        
def loopshuffle(start, stop=None, step=None): # continue loop shuffel numbers
  p1=0 if stop is None else start
  p2=start if stop is None else stop
  p3=1 if step is None else step
  l=[i for i in range(p1,p2,p3)]
  n=len(l)
  i=None
  while True:
    for _ in range(n):
      l.append(l.pop(randint(0,n-1)))
    if i == l[0]: l.append(l.pop(0)) # last i = new first i append at end  
    for _ in range(n):
      i=l[0]  
      yield i
      l.append(l.pop(0))

def generators(*args): # execute all given generators (yield from gen)
  for gen in args:
    yield from gen 

#def loopthis(gen,f,*args, **kwargs):
#  for _ in gen:
#     f(*args,**kwargs)
     
def genlooplist(l): # generator while all list values continue
  while True:  
    for v in l:
      yield v      
