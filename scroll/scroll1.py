#scroll1.py
# simple example of a scrolling background. This one uses just one picture that
# is drawn to a negative position.
from pygame import *
from random import randint

X=0
Y=1
VY=2

init()
size = width, height = 500, 500
screen = display.set_mode(size)
backPic = image.load("back.JPG")
guyPic = image.load("guy.png")


def drawScene(screen,guy):
    """ draws the current state of the game """
    screen.blit(backPic, (-guy[X],0))
    screen.blit(guyPic, (250,guy[Y]))
        
    display.flip()

'''
    The guy's x position is where he is in the "world" we then draw the map
    at a negative position to compensate.
'''
def moveGuy(guy):
    keys = key.get_pressed()
    
    if keys[K_LEFT] and guy[X] > 0:
        guy[X] -= 10
    if keys[K_RIGHT] and guy[X] < 3500:
        guy[X] += 10
    if keys[K_SPACE] and guy[Y]==450:
        guy[VY] = -10

    guy[Y]+=guy[VY]     # add current speed to Y
    if guy[Y] >= 450:
        guy[Y] = 450
        guy[VY] = 0
    guy[VY]+=.7     # add current speed to Y
    
    


running = True          
myClock = time.Clock()  
guy = [0,450,0]

while running:
    for evnt in event.get():                
        if evnt.type == QUIT:
            running = False

    moveGuy(guy)
    print(guy)
        
    drawScene(screen, guy)
    myClock.tick(60)

quit()
