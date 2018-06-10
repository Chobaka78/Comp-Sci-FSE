#FSE.py
from pygame import * # importing pygame
from datetime import datetime
from math import * # importing math 
from random import * # importing random to make random numbers, etc.
from tkinter import * # importing tkinter
from pprint import pprint # importing pretty print for tracing program, etc.
init()
root=Tk()
root.withdraw() # this gets rid of the extra window

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30" # centering the game

offset = 0 ## this is the offset based on the screen and the player x 
size = width, height = 1080, 720 ## size of the screen
screen = display.set_mode(size)

############### COLOURS ##############
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,139)
LightBLue = (66, 238, 244)
WHITE=(255,255,255)    ## basic colors that doesnt change in capital
BLACK=(0,0,0)
YELLOW=(255,255,0)

X=0 # X = 0
Y=1 # Y = 1
VY=2 # velocity y = 2
ONGROUND=3 # ounground 

################ LOADING ALL MAIN IMAGES ################
firstBack = image.load("images/firstBack.png")
cont_button = image.load("images/continue-button.png")
LEVEL1back=image.load("images/Level1Back.png")
LEVEL2back=image.load("images/Level2Back.png")
bullet = image.load("Bullet/bullet.png")
batmobile = image.load("images/batmobile.jpg")
batmobilepic = transform.scale(batmobile,(225,75))
bullet1 = transform.flip(bullet,True,False)
backgroundRect=Rect(0,0,1080,720)
buttonRect = Rect(940,10,130,50)
display.set_caption("THE AVENGERS AND JUSTICE LEAGUE")  #naming the program
arialFont=font.SysFont("Arial",38)

bullets = []
bullets2 = []
rapid = 10
music_List = ["Music/Game music 1.mp3", "Music/Game music 2.mp3", "Music/Game music.mp3", "Music/StoryMusic.mp3"] # This is the music list 
enemy = 5
XP = 0

level = "1" ## level originally = 1
HEALTH = 100 ## health of the player orignally = 100
heal = 290 ## this is the width of the players health bar
Dir = 1 # this is the direction used in bullets and bullets2 list
BATMAN = [540,650,0,True]  # Batmans position in the game
FLASH = [4050,650,0,True]  # This is FLASH's position in the game
FLASH_HEALTH = 150
Boss = False ## This is a temporary boolean var to check if boss spawns or not
############## MAKING THE ALIEN'S RECTS #################################
aliens = [[randint(1100,2000),650] for x in range(enemy)] # 2d list with random x values
aliensRect = [] # this is going to be a 2d list that will hold the rects
for i in range(enemy):
    aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
dead_counter = 0 ## this is the enemy dead counter checks how many are dead

def menu(): # function for the menu screen
    global music_List, arialFont
    mixer.music.load(music_List[0])
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
                
def makeMove(name,start,end): ## Moving for batman
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))        
    return move

def moveEnemy(name,start,end): ## Moving for aliens 
    move2 = []

    for i in range(start,end+1):
        move2.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move2

def moveFlash(name,start,end): # Moving for flash
    move3 = []

    for i in range(start,end+1):
        move3.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move3 

def moveBatman(BATMAN): # This function deals with all of batman's movements
    global Boss, newMove, Dir, aliensRect, rapid, bullets, bullets2, frame, move, offset, running, enemy
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    newMove = -1   
    ############ MOVING BATMAN ###############   
    if keys[K_LEFT] and BATMAN[X] > 540: # checking if batman's x is greater 540 
        newMove = LEFT # making the newMove  = LEFT for animation
        Dir = -1 # changing the direction of the player
        BATMAN[X] -= 13 # subtracting 13 from the current X
        for i in range(enemy):
            aliensRect[i][0] +=13 # adding 13 to the current alien's X values

    if keys[K_RIGHT] and BATMAN[X] < 4050:
        newMove = RIGHT
        Dir = 1
        BATMAN[X] += 13
        for i in range(enemy):
            aliensRect[i][0] -=10

    if keys[K_UP] and BATMAN[ONGROUND]: # checks if the player is on the ground
        newMove = Jump
        BATMAN[VY] = -10
        BATMAN[ONGROUND]=False

    if keys[K_SPACE]:
        if Dir == 1:
            if rapid < 10:
                rapid+=1
            if keys[K_SPACE] and rapid==10:
                rapid = 0
                VX = 10
                VY1 = 0
                bullets.append([(BATMAN[X] + offset),BATMAN[Y]+20,VX,VY1])
        elif Dir == -1:
            if rapid < 10:
                rapid+=1
            if keys[K_SPACE] and rapid==10:
                rapid = 0
                VX1 = -10
                VY2 = 0
                bullets2.append([(BATMAN[X] + offset),BATMAN[Y]+20,VX1,VY2])


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

def move_Flash(FLASH):
    global newMove3, frame3, offset, BATMAN, running, move3
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    #################### MOVING FLASH #######################
    newMove3 = -1
    if Boss == True:
        if (BATMAN[X] + offset) > FLASH[X] and FLASH[X] < 4050:
            newMove3 = RIGHT
            FLASH[X] +=10

        if (BATMAN[X] + offset) < FLASH[X] and FLASH[X] > 10:
            newMove3 = LEFT
            FLASH[X] -=10

        if move3 == newMove3:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame3 = frame3 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame3 >= len(Epics[move2]):
                frame3 = 1
        elif newMove3 != -1:     # a move was selected
            move3 = newMove3      # make that our current move
            frame3 = 0

def drawscene(screen,BATMAN):
    global dead_counter, LEVEL1back, offset,enemy, batmobilepic, frame, frame2, frame3, batRect, aliensRect, FLASH, level, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, enemy, FLASH_HEALTH, XP, Flashrect
    offset = 540 - BATMAN[X]
    if level == "1":
        screen.blit(LEVEL1back,(offset,0))
    elif level == "2":
        screen.blit(LEVEL2back,(offset,0))
    screen.blit(batmobilepic,((50 + offset),622))

    draw.rect(screen,(130, 73, 0),(0,705,4050,15))
    
    ###### Blitting batman
    pic = pics[move][int(frame)]
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)      
    draw.rect(screen,WHITE,Rect(BATMAN[X]+offset,BATMAN[Y],40,70),1)
    draw.rect(screen,LightBLue,batRect,2)
    screen.blit(pic, (540,BATMAN[Y]))
    
    ###### Blitting The ALiens
    pic2 = Epics[move2][int(frame2)]
    for i in range(enemy):
        aliensRect[i].move(offset,0)
        screen.blit(pic2,aliensRect[i])
        draw.rect(screen,RED,aliensRect[i],2)
    # print(offset,batRect.x,aliensRect[i],BATMAN[X])
    ######### BLitting FLash########
    if Boss == True:
        pic_3 = FlashPics[move3][int(frame3)]
        pic3 = transform.scale(pic_3,(40,70))
        Flashrect = Rect((FLASH[X] + offset),FLASH[Y],40,70)
        screen.blit(pic3,Flashrect)
        draw.rect(screen,WHITE,Flashrect,2)

    ############# MOVING THE BULLETS #############
    for b in bullets[:]:
        b[0]+=b[2]
        b[1]+=b[3]

        if max(b) > 1080 or min(b) < -0:
            bullets.remove(b)

    for b in bullets:
        screen.blit(bullet,(int(b[0]),int(b[1])))

    for o in bullets2[:]:
        o[0]+=o[2]
        o[1]+=o[3]

    for i in bullets2:
        screen.blit(bullet1,(int(i[0]),int(i[1])))
    ##############################################
    ######## Checking for collide with bullets and alien ###########
    for m in range(enemy):
        for i in bullets:
            r = Rect(i)
            if r.colliderect(aliensRect[m]): 
                # print('alien killed')
                del bullets[bullets.index(i)]
                EhealthList[m] -= 10
                print(EhealthList)
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                if EhealthList[m] <= 0:
                    dead_counter += 1
                    XP += 100
            if Boss == True:
                if r.colliderect(Flashrect):
                    del bullets[bullets.index(i)]
                    FLASH_HEALTH -= 10

        for i in bullets2:
            c = Rect(i)
            if c.colliderect(aliensRect[m]): 
                # print('alien killed')
                del bullets2[bullets2.index(i)]
                EhealthList[m] -=10
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                if EhealthList[m] <= 0:
                    dead_counter += 1
                    XP += 100

            if Boss == True:
                if c.colliderect(Flashrect):
                    del bullets2[bullets2.index(i)]
                    FLASH_HEALTH -= 10

        if EhealthList[m] == 0:
            aliensRect[m].top = 1500
        if dead_counter == len(aliensRect):
            Boss = True
        if batRect.colliderect(aliensRect[m]):
            pass
    if Boss == True:   
        if FLASH_HEALTH == 0:
                FLASH[Y] = 1500
                level = "2"
                XP += 500
                Boss = False
    print(level)
    enemyHealth()
    health()
    display_XP()      


def moveAliens(aliensRect):
    global newMove2, frame2, BATMAN, offset, HEALTH, heal, running, move2, enemy 
    ############ MOVING THE ENEMY ###################
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    for i in range(enemy):
        newMove2 = -1
        if (BATMAN[X] + offset) < aliensRect[i][0] and aliensRect[i][0] > 10: ## Checking if Batman's x is greater than alien's x
            newMove2 = LEFT
            eV=randint(1,7)
            aliensRect[i][0] -= eV
            
        if (BATMAN[X] + offset) > aliensRect[i][0] and aliensRect[i][0] < 2090: ## Checking if Batman's x is less than the alien's x
            newMove2 = RIGHT
            eV=randint(1,7)
            aliensRect[i][0] += eV
        
        if aliensRect[i].colliderect(batRect): ## Checking for collide between the aliens and Batman
            newMove2 = -1
            frame2 = 0
            aliensRect[i][0] +=0
            if HEALTH > 0:
                HEALTH -=5
                heal = int(heal * (HEALTH/100))

    if move2 == newMove2:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame2 = frame2 + 0.2 # adding 0.2 allows us to slow down the animation
        if frame2 >= len(Epics[move2]):
            frame2 = 1
    elif newMove2 != -1:     # a move was selected
        move2 = newMove2      # make that our current move
        frame2 = 1  

def myLevel1():
    moveBatman(BATMAN)
    moveAliens(aliensRect)
    move_Flash(FLASH)
    drawscene(screen,BATMAN)

def myLevel2():
    level = "2"
    moveBatman(BATMAN)
    drawscene(screen,BATMAN)
    moveAliens(aliensRect)
    
def Game():
    mixer.music.stop()
    mixer.music.load(music_List[1])
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    global level
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

        keys = key.get_pressed()
        if keys[K_o]:
            level = "2"
        mx, my = mouse.get_pos() 

        if level == "1":
            myLevel1()

        if level == "2":
            myLevel2()

        display.update()
        myClock.tick(25)
        display.flip()

    return "menu"

def health(): # This is the player health function
    draw.rect(screen,BLUE,(5,5,300,25),0)
    draw.rect(screen,BLUE,(5,35,225,20),0)
    draw.rect(screen,RED,(10,10,heal,15),0)
    draw.rect(screen,LightBLue,(10,40,215,10),0)
    Gems = [Rect(5+x*40,45+20,35,15) for x in range(6)] ## This creates a row of rectangles 
    for i in range (len(Gems)):
        draw.rect(screen,WHITE,Gems[i],2)

def enemyHealth():
    global ehealList
    for i in range(enemy):
        draw.rect(screen,RED,(aliensRect[i][0],aliensRect[i][1]-20,35,5),0)
        draw.rect(screen,GREEN,(aliensRect[i][0],aliensRect[i][1]-20,ehealList[i],5),0)

def display_XP():
    global XP, arialFont
    arialFont=font.SysFont("Arial",28)
    XpFont = arialFont.render("XP: ",True,WHITE)
    xpfont = arialFont.render(str(XP),True,WHITE)
    Xppic = XpFont
    xppic = xpfont
    screen.blit(Xppic,(5,100))
    screen.blit(xppic,(50,100))


RIGHT = 0 # These are just the indices of the moves
LEFT = 1
Jump = 2
Punch = 3

pics = [] #2d list
pics.append(makeMove("Run",0,16))# RIGHT
pics.append(makeMove("RunLeft",0,16))# LEFT
pics.append(makeMove("Jump",0,4))# Jumping
pics.append(makeMove("Punch",0,11))# Punching

Epics=[]
Epics.append(moveEnemy("alien",1,7))# RIGHT
Epics.append(moveEnemy("alien",8,14))# LEFT

FlashPics = []
FlashPics.append(moveFlash("FlashRun",0,6))# Right 
FlashPics.append(moveFlash("FlashRunLeft",0,6))# Left
FlashPics.append(moveFlash("FlashPunch",0,4)) # Punch Right
FlashPics.append(moveFlash("FlashPunchLeft",0,4))# Punch Left

frame = 0     # current frame within the move
move = 0      # current move being performed (right, down, up, left)
frame2 = 0
move2 = 0
frame3 = 0
move3 = 0

def instructions():
    global music_List
    mixer.music.stop()
    mixer.music.play(-1)
    mixer.music.load(music_List[2])
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

        if mb[0] == 1 and buttonRect.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,10)) # blitting the button

        display.flip()
    return "menu"
        
def credit():
    global music_List
    mixer.music.stop()
    mixer.music.load(music_List[0])
    mixer.music.play()
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
        if mb[0] == 1 and buttonRect1.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,660)) # blitting the button
        display.flip()
    return "menu"

def story():
    global music_List
    mixer.music.stop()
    mixer.music.load(music_List[3])
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
        if mb[0] == 1 and buttonRect2.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,0)) # blitting the button
        display.flip()
    return "menu"

level = "1" ## level originally = 1
HEALTH = 100 ## health of the player orignally = 100
heal = 290 ## this is the width of the players health bar
Dir = 1 # this is the direction used in bullets and bullets2 list
BATMAN = [540,650,0,True]  # Batmans position in the game
FLASH = [4050,650,0,True]  # This is FLASH's position in the game
Boss = False ## This is a temporary boolean var to check if boss spawns or not
if level == "1":
    enemy = 5
elif mylevel() == "2":
    enemy = 10
############## MAKING THE ALIEN'S RECTS #################################
aliens = [[randint(1100,2000),650] for x in range(enemy)] # 2d list with random x values
aliensRect = [] # this is going to be a 2d list that will hold the rects
for i in range(enemy):
    aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values

EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
dead_counter = 0 ## this is the enemy dead counter checks how many are dead 
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
hi