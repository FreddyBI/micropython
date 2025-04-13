from time import ticks_ms, ticks_add,ticks_diff

class Gen:
  def __init__(self,gen): # hold generator and start generator and get first yield value
    self.gen=gen
    self.next=next(gen) 

class Async: # async running coroutines
    
  def __init__(self): # create list used for automatic remove finished generators en next values  
    self.gens=[] 

  def add(self,*thisgens): # add generators to list gens
    for gen in thisgens:
      self.gens.append(Gen(gen))
      
  def run(self): # run all tasks generators 

    while self.gens:
      for data in self.gens:
        try:
          data.next=data.gen.send(data.next)
        except StopIteration:
          self.gens.remove(data)

def sleepms(ms): # sleep milliseconds non blocking
  now = ticks_ms()
  stoptime= ticks_add(now,ms)
  while ticks_diff(stoptime,ticks_ms()) > 0:
    yield
