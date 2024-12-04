from random import randint

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
      
def roundint(f) : # round float to int
  return int(f+0.5) if f > 0.0 else int(f-0.5)
