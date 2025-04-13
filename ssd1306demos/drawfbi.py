from drawfbi import *

fill=o.fill
draw=o.draw
draw=o.draw
show=o.show
width=o.width
pixel=o.pixel
vline=o.vline

fill(0)
draw(triangle((0,0),(31,31),(0,62)))
draw(triangle((0,0),(128,31),(0,62)))
draw(polygon(63,31,5,31))

for r in range(2,18,3):
  draw(circle(31,31,r))
show()
sleep(2)

fill(0)
for x in range(width):
  vline(x,0,64,1)
  show()
  
fill(0)  
for _ in range(0,181,10):
  for h in [0,45,90,135]:  
    draw(polygon(63,31,4,32,_+h))
  show()
  fill(0)

