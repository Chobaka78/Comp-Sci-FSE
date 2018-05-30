#FSE.py
from pygame import *
from datetime import datetime
from math import *
from random import *
from tkinter import *
from pprint import pprint
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
cont_button = image.load("images/continue-button.png")
backgroundRect=Rect(0,0,1080,720)
buttonRect = Rect(940,10,130,50)
display.set_caption("THE AVENGERS AND JUSTICE LEAGUE")  #naming the program
## Global varaiables
bullets = []
rapid = 10

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
        # print(mpos)
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
                
def makeMove(name,start,end):
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))        
    return move

def moveEnemy(name,start,end):
    move2 = []

    for i in range(start,end+1):
        move2.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move2

def health():
    draw.rect(screen,BLUE,(5,5,300,25),0)
    draw.rect(screen,BLUE,(5,35,225,20),0)
    draw.rect(screen,RED,(10,10,heal,15),0)
    draw.rect(screen,LightBLue,(10,40,215,10),0)
    Gems = [Rect(5+x*40,45+20,35,15) for x in range(5)]
    for i in range (len(Gems)):
        draw.rect(screen,BLACK,Gems[i],2)

    # print(heal,HEALTH)
aliens = [[randint(1080,1500),650] for x in range(5)]
aliensRect = []
for i in range(5):
    aliensRect.append(Rect(aliens[i][0],650,44,60))
##pprint(aliens)

def Game():
    global BATMAN, heal, HEALTH, ALIEN, move, frame, rapid, bullets, bullet, move2, frame2, HEALTH, heal, bullets, Ehealth, eheal, Dir, hit, aliens
    level = "1"
    HEALTH = 100
    Ehealth = 100
    eheal = 35
    heal = 290
    Alive = True
    Dir = 1
    BATMAN = [10,650,0,True,10]  # Batmans position in the game
    mixer.music.stop()
    mixer.music.load("Music/Game music 2.mp3")
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    ## Loading all images
    bullet = image.load("batman/bullet.png")
    bullet1 = image.load("batman/bullet1.png")
    ###########################################

    if level == "1":
        LEVEL1back=image.load("images/Level1Back.png")
    
    while running:

        offset = BATMAN[SCREENX] - BATMAN[X]
        screen.blit(LEVEL1back,(offset,0))

        pic = pics[move][int(frame)]
        batRect = pic.get_rect()
        batRect.x, batRect.y = BATMAN[SCREENX],BATMAN[Y]
        screen.blit(pic, (BATMAN[SCREENX],BATMAN[Y]))

        if Alive == True:
            alienRectX = []
            alienRectY = []
            alienRect = []
            pic2 = Epics[move2][int(frame2)]
            for i in range(5):
                screen.blit(pic2,aliensRect[i])

        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
                
        keys = key.get_pressed()
        newMove = -1   
        ############ MOVING BATMAN ###############     
        if keys[K_LEFT] and BATMAN[X] > 10:
            newMove = LEFT
            Dir = -1
            BATMAN[X] -= 10
            if BATMAN[SCREENX] > 10:
                BATMAN[SCREENX] -= 10

        if keys[K_RIGHT] and BATMAN[X] < 2090:
            newMove = RIGHT
            Dir = 1
            BATMAN[X] += 10
            if BATMAN[SCREENX] < 1000:
                BATMAN[SCREENX] += 10

        if keys[K_UP] and BATMAN[ONGROUND]:
            newMove = Jump
            BATMAN[VY] = -10
            BATMAN[ONGROUND]=False

        if keys[K_SPACE] and Dir == 1:
            if rapid < 10:
                rapid+=1
            if keys[K_SPACE] and rapid==10:
                rapid = 0
                VX = 10
                VY1 = 0
                bullets.append([BATMAN[X],BATMAN[Y]+20,VX,VY1])

        elif keys[K_SPACE] and Dir == -1:
            if rapid < 10:
                rapid+=1
            if keys[K_SPACE] and rapid==10:
                rapid = 0
                VX = -10
                VY1 = 0
                bullets.append([BATMAN[X],BATMAN[Y]+20,VX,VY1])

        BATMAN[Y]+=BATMAN[VY]     # add current speed to Y
        if BATMAN[Y] >= 650:
           BATMAN[Y] = 650
           BATMAN[VY] = 0
           BATMAN[ONGROUND]=True
        BATMAN[VY]+=.7     # add current speed to Y
        ################################################################

        ######## BATMAN PUNCH #######
        if keys[K_b]:
            newMove = Punch

        elif newMove == -1:
            frame = 0
        ##############################

        ########## ANIMATION FOR BATMAN ############
        if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame = frame + 0.4 # adding 0.2 allows us to slow down the animation
            if frame >= len(pics[move]):
                frame = 1
        elif newMove != -1:     # a move was selected
            move = newMove      # make that our current move
            frame = 1
        ############################################

        mx, my = mouse.get_pos() 

        ############ MOVING THE ENEMY ###################
        if Alive == True:
            for i in range(5):
                newMove2 = -1
                if BATMAN[X] < aliensRect[i][0] and aliensRect[i][0] > 10:
                    newMove2 = LEFT
                    aliensRect[i][0] -= 5

                if BATMAN[X] > aliensRect[i][0] and aliensRect[i][0] < 2090:
                    newMove2 = RIGHT
                    aliensRect[i][0] += 5
                if batRect.colliderect(aliensRect[i]):
                    newMove2 = -1
                    frame2 = 0
                    aliensRect[i][0] +=0
                    if HEALTH > 0:
                        HEALTH -=5
                        heal = int(heal * (HEALTH/100))

            if move2 == newMove2:     # 0 is a standing pose, so we want to skip over it when we are moving
                frame2 = frame2 + 0.4 # adding 0.2 allows us to slow down the animation
                if frame2 >= len(Epics[move2]):
                    frame2 = 1
            elif newMove2 != -1:     # a move was selected
                move2 = newMove2      # make that our current move
                frame2 = 1     
        ##########################################################

        ############# MOVING THE BULLETS #############
        if Dir == 1:
            for b in bullets[:]:
                b[0]+=b[2]
                b[1]+=b[3]

                if max(b) > 1080 or min(b) < -0:
                    bullets.remove(b)

            for b in bullets:
                screen.blit(bullet,(int(b[0]),int(b[1])))
        elif Dir == -1:
            for b in bullets[:]:
                b[0]+=b[2]
                b[1]+=b[3]

                if max(b) > 1080 or min(b) < -0:
                    bullets.remove(b)

            for b in bullets:
                screen.blit(bullet1,(int(b[0]),int(b[1])))
        ##############################################
        ######## Checking for collide with bullets and alien ###########
        for m in range(5):
            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets[bullets.index(i)]
                    Ehealth -=10
                    eheal = eheal * (Ehealth/100)

        # print(Ehealth, eheal)            
            if batRect.colliderect(aliensRect[m]):
                pass

            if Ehealth <= 1:
                Alive = False

            else:
                Alive = True
                enemyHealth()
        ################################################################
        health()
        display.update()
        myClock.tick(25)
        display.flip()
    
    return "menu"

def enemyHealth():
    global Ehealth, eheal, hit
    for i in range(5):
        draw.rect(screen,RED,(aliensRect[i][0],aliensRect[i][1]-20,35,5),0)
        draw.rect(screen,GREEN,(aliensRect[i][0],aliensRect[i][1]-20,eheal,5),0)

RIGHT = 0 # These are just the indices of the moves
LEFT = 1
Jump = 2
Punch = 3

pics = [] #2d list
pics.append(makeMove("batman",0,16))# RIGHT
pics.append(makeMove("batman",26,34))# LEFT
pics.append(makeMove("batman",35,38))# Jumping
pics.append(makeMove("batman",39,49))# Punching

Epics=[]
Epics.append(moveEnemy("alien",1,7))# RIGHT
Epics.append(moveEnemy("alien",8,14))# LEFT

frame = 0     # current frame within the move
move = 0      # current move being performed (right, down, up, left)
frame2 = 0
move2 = 0

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
running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = Game()    
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()    
    
quit()
