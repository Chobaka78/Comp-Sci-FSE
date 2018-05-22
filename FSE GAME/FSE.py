#FSE.py
from pygame import *
from datetime import datetime
from math import *
from random import *
from tkinter import *
init()
root=Tk()
root.withdraw()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"

size = width, height = 1080, 720
screen = display.set_mode(size)

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,139)
LightBLue = (66, 238, 244)
WHITE=(255,255,255)    ## basic colors that doesnt change in capital
BLACK=(0,0,0)
YELLOW=(255,255,0)

X=0 
Y=1
VY=2
ONGROUND=3

firstBack = image.load("images/firstBack.png")
LEVEL1back=image.load("images/Level1Back.png")
cont_button = image.load("images/continue-button.png")
backgroundRect=Rect(0,0,1080,720)
buttonRect = Rect(940,10,130,50)
display.set_caption("THE AVENGERS AND JUSTICE LEAGUE")  #naming the program

def menu():
    mixer.music.load("Music/Game music 1.mp3")
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    buttons = [Rect(85,y*80+420,130,50) for y in range(4)]
    vals = ["game","instructions","story","credits"]
    vals2 = ["  START ","HOW TO","  STORY"," CREDIT"]
    arialFont=font.SysFont("Arial",38)

    while running:
        for evt in event.get():          
            if evt.type == QUIT:
                return "exit"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()

        keys = key.get_pressed()

        screen.blit(firstBack,backgroundRect)
        print(mpos)
        for i in range(len(buttons)):
            title=arialFont.render(vals2[i],True,BLUE)
            draw.rect(screen,WHITE,buttons[i])
            screen.blit(title,buttons[i])
            if buttons[i].collidepoint(mpos):
                title=arialFont.render(vals2[i],True,BLACK)
                draw.rect(screen,BLACK,buttons[i],2)
                screen.blit(title,buttons[i])

                if mb[0]==1:
                    return vals[i]
            else:
                draw.rect(screen,YELLOW,buttons[i],2)            
        display.flip()
        
def moveBATMAN(BATMAN):
    keys = key.get_pressed()
    global move, frame
    newMove = -1        
    if keys[K_LEFT] and BATMAN[X] > 10:
        newMove = LEFT
        BATMAN[X] -= 10
        if BATMAN[SCREENX] > 10:
            BATMAN[SCREENX] -= 10

    if keys[K_RIGHT] and BATMAN[X] < 2090:
        newMove = RIGHT
        BATMAN[X] += 10
        if BATMAN[SCREENX] < 1000:
            BATMAN[SCREENX] += 10

    if keys[K_SPACE] and BATMAN[ONGROUND]:
        newMove = Jump
        BATMAN[VY] = -10
        BATMAN[ONGROUND]=False

    BATMAN[Y]+=BATMAN[VY]     # add current speed to Y
    if BATMAN[Y] >= 650:
       BATMAN[Y] = 650
       BATMAN[VY] = 0
       BATMAN[ONGROUND]=True
    BATMAN[VY]+=.7     # add current speed to Y

    if keys[K_b]:
        newMove = Punch

    elif newMove == -1:
        frame = 0

    print(BATMAN[X],BATMAN[Y])

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.4 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
                
def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))        
    return move

def drawScene(screen,BATMAN):
    """ draws the current state of the game """
    offset = BATMAN[SCREENX] - BATMAN[X]
    screen.blit(LEVEL1back,(offset,0))
        ### This will be later moved into a function#############
    draw.rect(screen,BLUE,(5,5,300,25),0)
    draw.rect(screen,RED,(10,10,290,15),0)
    draw.rect(screen,BLUE,(5,35,225,20),0)
    draw.rect(screen,LightBLue,(10,40,215,10),0)
    Gems = [Rect(5+x*40,45+20,35,15) for x in range(5)]
    for i in range (len(Gems)):
        draw.rect(screen,BLACK,Gems[i],2)
    ######################################################
    

    pic = pics[move][int(frame)]
    screen.blit(pic, (BATMAN[SCREENX],BATMAN[Y]))

    display.flip()

'''
    The guy's x position is where he is in the "world" we then draw the map
    at a negative position to compensate.
'''

def Level1():
    BATMAN = [10,650,0,True,10]  # Batmans position in the game
    mixer.music.stop()
    mixer.music.load("Music/Game music 2.mp3")
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        mx, my = mouse.get_pos()
        print(mx,my)

        keys = key.get_pressed()

        moveBATMAN(BATMAN)        
        #checkCollide(BATMAN,plats)
        drawScene(screen,BATMAN)
        display.update()
        myClock.tick(25)
        display.flip()
    
    return "menu"

RIGHT = 0 # These are just the indices of the moves
LEFT = 1
Jump = 2
Punch = 3

pics = [] #2d list
pics.append(makeMove("batman",0,16))# RIGHT
pics.append(makeMove("batman",26,34))# LEFT
pics.append(makeMove("batman",35,38))# Jumping
pics.append(makeMove("batman",39,49))# Punching

frame=0     # current frame within the move
move=0      # current move being performed (right, down, up, left)

def instructions():
    mixer.music.stop()
    mixer.music.load("Music/Game music.mp3")
    mixer.music.play(-1)

    inst = image.load("images/instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    running = True
    
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if buttonRect.collidepoint(mx,my):
            draw.rect(screen,BLUE,buttonRect,2)
        else:
            draw.rect(screen,WHITE,(940,10,150,50))

        if mb[0] == 1:
            return "game"

        screen.blit(cont_button,(940,10)) # blitting the button

        display.flip()
    return "menu"
        
def credit():
    running = True
    cred = image.load("images/credits.png")
    cred = transform.smoothscale(cred, screen.get_size())
    buttonRect1 = Rect(940,660,130,50)
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if buttonRect1.collidepoint(mx,my):
            draw.rect(screen,BLUE,buttonRect1,2)
        else:
            draw.rect(screen,WHITE,buttonRect1)
        if mb[0] == 1:
            return "game"

        screen.blit(cont_button,(940,660)) # blitting the button
        display.flip()
    return "menu"

def story():
    mixer.music.stop()
    mixer.music.load("Music/StoryMusic.mp3")
    mixer.music.play(-1)
    buttonRect2 = Rect(940,0,130,50)
    running = True
    story = image.load("images/story.png")
    storyLine = image.load("images/Storyline.png")
    story = transform.smoothscale(story, screen.get_size())
    screen.blit(story,(0,0))
    screen.blit(storyLine,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        if buttonRect2.collidepoint(mx,my):
            draw.rect(screen,WHITE,buttonRect2,2)
        else:
            draw.rect(screen,BLACK,buttonRect2)
        if mb[0] == 1:
            return "game"

        screen.blit(cont_button,(940,0)) # blitting the button
        display.flip()
    return "menu"

X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4

BATMAN = [10,650,0,True,10]  # Batmans position in the game
running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = Level1()    
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()    
    
quit()

# This is the change
