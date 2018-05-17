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

firstBack = image.load("images/firstBack.png")
LEVEL1back=image.load("images/Level1Back.png")
backgroundRect=Rect(0,0,1080,720)
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

def moveBatman():
    ''' movebatman controls the location of batman as well as adjusts the move and frame
        variables to ensure the right picture is drawn.
    '''
    global move, frame
    keys = key.get_pressed()
    newMove = -1        
    if keys[K_RIGHT]:
        newMove = RIGHT
        BATMAN[0] += 5

    elif keys[K_LEFT]:
        newMove = LEFT
        BATMAN[0] -= 5
    elif keys[K_SPACE] and BATMAN[1] >= 635:
        newMove = UP
        BATMAN[1] -= 10

    else:
        frame = 0
        BATMAN[1]= 675

    #print(move,newMove)

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.3# adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
        print("hello")

def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move

def drawScene():
    screen.blit(LEVEL1back,backgroundRect)
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
    screen.blit(pic,(BATMAN[0]-pic.get_width()//2,BATMAN[1]-pic.get_height()//2))
    print(move,frame)           
    display.flip()


def simpleGame():
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
        mb = mouse.get_pressed()
        keys = key.get_pressed()

        moveBatman()          
        drawScene()
        myClock.tick(50)
        display.flip()
    
    return "menu"


RIGHT = 0 # These are just the indices of the moves
LEFT = 1
UP = 2

pics = [] #2d list
pics.append(makeMove("batman",0,9))      # RIGHT
pics.append(makeMove("batman",10,18))    # LEFT
pics.append(makeMove("batman",20,24))

print(len(pics[0]),len(pics[1]),len(pics[2]))


frame=0     # current frame within the move
move=0      # current move being performed (right, down, up, left)

BATMAN=[10,675]  #batman position

def instructions():
    mixer.music.stop()
    mixer.music.load("Music/Game music.mp3")
    mixer.music.play(-1)
    running = True
    inst = image.load("images/instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
        
def credit():
    running = True
    cred = image.load("images/credits.png")
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
    

def story():
    mixer.music.stop()
    mixer.music.load("Music/StoryMusic.mp3")
    mixer.music.play(-1)
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
        display.flip()
    return "menu"














running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = simpleGame()    
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()    
    
quit()

