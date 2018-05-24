# scroll3
# simple example of a scrolling background. This one uses just one picture that
# is drawn to a negative position.
from pygame import *
from random import randint


init()
size = width, height = 500, 500
screen = display.set_mode(size)
backPic = image.load("back.JPG")
guyPic = image.load("guy.png")

def drawScene(screen,guy):
    """ draws the current state of the game """
    offset = guy[SCREENX] - guy[X]
    screen.blit(backPic, (offset,0))
    for pl in plats:
        p = pl.move(offset,0)        
        draw.rect(screen,(111,111,111),p)
    screen.blit(guyPic, (guy[SCREENX],guy[Y]))
        
    display.flip()

'''
    The guy's x position is where he is in the "world" we then draw the map
    at a negative position to compensate.
'''
def moveGuy(guy):
    keys = key.get_pressed()
    
    if keys[K_LEFT] and guy[X] > 50:
        guy[X] -= 10
        if guy[SCREENX] > 50:
            guy[SCREENX] -= 10
    if keys[K_RIGHT] and guy[X] < 3950:
        guy[X] += 10
        if guy[SCREENX] <450:
            guy[SCREENX] += 10
    if keys[K_SPACE] and guy[ONGROUND]:
        guy[VY] = -10
        guy[ONGROUND]=False

    guy[Y]+=guy[VY]     # add current speed to Y
    if guy[Y] >= 450:
        guy[Y] = 450
        guy[VY] = 0
        guy[ONGROUND]=True
    guy[VY]+=.7     # add current speed to Y
    
def checkCollide(guy,plats):
    rec = Rect(guy[X],guy[Y],20,31)
    for p in plats:
        if rec.colliderect(p):
            if guy[VY]>0 and rec.move(0,-guy[VY]).colliderect(p)==False:
                guy[ONGROUND]=True
                guy[VY] = 0
                guy[Y] = p.y - 31
              


running = True         
myClock = time.Clock()

X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4
guy = [250,450,0,True,250]

plats=[Rect(280,430,60,10),Rect(310,450,60,10)]

##plats = []
##for i in range(20):
##    plats.append(Rect(randint(100,2000),randint(250,480),60,10))

while running:
    for evnt in event.get():               
        if evnt.type == QUIT:
            running = False

    moveGuy(guy)        
    checkCollide(guy,plats)
    drawScene(screen, guy)
    myClock.tick(60)
    #print(guy)
    #print (guy[ONGROUND])

quit()
b