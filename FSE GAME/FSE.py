#FSE.py
## BY: USMAN FAROOQI AND YOUSSEF ELSAFADI
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
screen = display.set_mode(size) # size of the screen

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
LEVEL3back=image.load("images/Level3Back.png")
LEVEL4back=image.load("images/Level4Back.png")
bullet = image.load("Bullet/bullet.png")
batmobile = image.load("images/batmobile.jpg")
bandage = image.load("images/bandage.png")
energyPic = image.load("images/Energy.png")
################# TRANSFORMING/RECTS ################### 
batmobilepic = transform.scale(batmobile,(225,75))
bullet1 = transform.flip(bullet,True,False)
backgroundRect=Rect(0,0,1080,720)
buttonRect = Rect(940,10,130,50)
display.set_caption("THE AVENGERS AND JUSTICE LEAGUE")  #naming the program
arialFont=font.SysFont("Arial",38)
################ VARIABLES #################### 
bullets = [] ## right shooting bullets list 
bullets2 = [] ## Left shooting bullets list
rapid = 27 ## rapid determines how many bullets are shot 
music_List = ["Music/Menu music.mp3", "Music/Level1.mp3", "Music/How to music.mp3", "Music/StoryMusic.mp3", "Music/Level2 music.mp3", "Music/Ending credits.mp3", "Music/Level3 music.mp3", "Music/Level4 music.mp3"] # This is the music list 
enemy = 10 ## this variable determines how many enemies will be blit 
boss = 0 ## this is an index that tells the program the current boss used for the health bar
XP = 0 ## This is the xp 
fill = [2,2,2,2,2] ## this will will the gems once a level is complete

BATMAN = [540,655,0,True]  # Batmans position in the game
HEALTH = 100 ## health of the player orignally = 100
HEALTH_Constant = 100
heal = 400 ## this is the width of the players health bar
Energy = 100 ## this is the players energy for special moves
energy = 215 ## this is the width of the energy bar

Dir = 1 # this is the direction used in bullets and bullets2 list
EDir = -1 # this is the direction of the enemy boss
Count = 0 #3 this is a counter variable that makes it so boss cant spam moves
BossHealth = [200, 400, 800, 1000] ## list of all the boss health
bossHeal = -400 ## this is the width of the boss health bar negative due to it being on the right side of the screen
############### POSITION OF BOSS'S #########################
FLASH = [4050,650,0,True]
Iron_man = [4050,650,0,True]
Super_man = [4050,640,0,True]
Thanos = [4050,590,0,True]
#############################################
Boss = False ## This is a temporary boolean var to check if boss spawns or not
############## MAKING THE ALIEN'S RECTS #################################
aliens = [[randint(1100,4000),650] for x in range(enemy)] # 2d list with random x values
aliensRect = [] # this is going to be a 2d list that will hold the rects
for i in range(enemy):
    aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
dead_counter = 0 ## this is the enemy dead counter checks how many are dead
################## RECTS FOR ALL THE PLATFORMS
plats = [Rect(1000,635,100,5),Rect(1500,635,100,5),Rect(1250,570,80,5),
        Rect(1010,500,80,5),Rect(1510,500,80,5),Rect(2000,635,100,5),
        Rect(2500,635,100,5),Rect(2250,570,100,5),Rect(2010,500,80,5),
        Rect(2510,500,80,5),Rect(3000,635,100,5),Rect(3500,635,100,5),
        Rect(3250,570,100,5),Rect(3010,500,80,5),Rect(3510,500,80,5),
        Rect(1000,365,100,5),Rect(1500,365,100,5),Rect(1250,435,80,5),
        Rect(1010,365,80,5),Rect(1510,365,80,5),Rect(2500,365,100,5),
        Rect(2250,435,100,5),Rect(2010,365,100,5),Rect(3000,365,100,5),
        Rect(3250,435,100,5),Rect(3510,365,100,5)] # rects for platforms
#################################################################

numBandages=6 ### this is the number of bandeges that will be blit on to screen
bandages = [Rect(1032,463,35,35),Rect(1032,328,35,35), Rect(2032,463,35,35),Rect(2032,328,35,35), Rect(3032,463,35,35),Rect(3032,328,35,35)]
## above is the rect for bandages 
numEnergy=6 ## this is the number of energy refills that will be blit on to the screen
energies = [Rect(1532,463,35,35),Rect(1532,328,35,35), Rect(2532,463,35,35),Rect(2532,328,35,35), Rect(3532,463,35,35), Rect(3532,328,35,35)]

def menu(): # function for the menu screen
    global music_List, arialFont 
    mixer.music.load(music_List[0]) ## loading music 
    mixer.music.play(-1) ## playing music 
    running = True
    myClock = time.Clock()
    buttons = [Rect(85,y*80+420,130,50) for y in range(4)] ## this is a list of button rects
    vals = ["game","instructions","story","credits"] ## these are names used to call each menu screen
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
        ##### CHECKING FOR COLLISION BETWEEN MOUSE AND BUTTON #############
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

def moveIronman(name,start,end): # Moving for IRON MAN
    move4 = []

    for i in range(start,end+1):
        move4.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move4

def moveSuperman(name,start,end): # Moving for SUPERMAN
    move5 = []

    for i in range(start,end+1):
        move5.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move5
    
def moveThanos(name,start,end): # Moving for THANOS
    move6 = []

    for i in range(start,end+1):
        move6.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move6

def moveBatman(BATMAN): # This function deals with all of batman's movements
    global Boss, newMove, Dir, aliensRect, rapid, bullets, bullets2, frame, move, offset, running, Edir
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    newMove = -1   
    ############ MOVING BATMAN ###############   
    if keys[K_LEFT] and BATMAN[X] > 540: # checking if batman's x is greater 540 
        newMove = LEFT # making the newMove  = LEFT for animation
        Dir = -1 # changing the direction of the player
        EDir = -1 # chinging the direction of the boss
        BATMAN[X] -= 13 # subtracting 13 from the current X
        for i in range(enemy):
            aliensRect[i][0] +=13 # adding 13 to the current alien's X values

    if keys[K_RIGHT] and BATMAN[X] < 4050: ## checking for key right 
        newMove = RIGHT # move right 
        Dir = 1 ## making the dir 1 this is used in bullets 
        EDir = 1 ## making the direction of the boss 1 as well 
        BATMAN[X] += 13
        for i in range(enemy):
            aliensRect[i][0] -=13 ## making the aliens move 10 pixels left for offset

    if keys[K_UP] and BATMAN[ONGROUND]: # checks if the player is on the ground
        BATMAN[VY] = -10 ## if up key is pressed then jump 
        BATMAN[ONGROUND]=False

    if keys[K_SPACE] and Dir == 1: ## if space key and player direction 1 
        newMove = Shoot ## if move is shoot for animation 
        if rapid < 27:
            rapid+=3 ## shoot 3 bullets rapidly 
        if keys[K_SPACE] and rapid==27:
            rapid = 0
            VX = 10
            VY1 = 0
            bullets.append([(BATMAN[X] + offset) + 10,BATMAN[Y]+20,VX,VY1]) ## offseting te bullets with batman
    elif keys[K_SPACE] and Dir == -1:
        newMove = ShootLeft ## if shoot is left for animation 
        if rapid < 27:
            rapid+=3
        if keys[K_SPACE] and rapid==27:
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
    if keys[K_b] and Dir == 1: ## checking if b is pressed and if the players direction is 1
        newMove = Punch

    if keys[K_b] and Dir == -1: ## checking is b is pressed and if player direction is -1
        newMove = Punchleft

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

def move_Flash(FLASH): ## this is the movement for flash 
    myClock = time.Clock()
    global newMove3, frame3, offset, BATMAN, running, Count, move3, batRect, Dir, HEALTH, heal, EDir
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    #################### MOVING FLASH #######################
    newMove3 = -1
    if Boss == True:

        if (BATMAN[X]) < FLASH[X] and FLASH[X] > 540 and not Flashrect.colliderect(batRect): ## checking if batman x is less than flash's X and if there is no collision
            newMove3 = LEFT
            EDir = -1
            FLASH[X] -=12 ## moving 13 pixels to the left 

        elif (BATMAN[X]) > FLASH[X] and FLASH[X] < 4050 and not Flashrect.colliderect(batRect): ## checking if batman X is greater than flash's and there is no collision
            newMove3 = RIGHT
            EDir = 1
            FLASH[X] +=12 ## moving 13 pixels to the right

        elif Flashrect.colliderect(batRect) and EDir == -1: ## checking if flash collides with batman with a -1 direction (left)
            newMove3 = Punchleft ## move is punch 
            FLASH[X] += 0 ## makes the boss stop
            Count += 1 ## count increases
            if HEALTH > 0 and Count == 2: # if the health is greater than 0 so there is no negative val and the count is 2 
                HEALTH -=10 ## subtract 10 from health
                heal = int(heal * (HEALTH/HEALTH_Constant)) ## take percentage and multiple by width
                Count = 0 ## set count 2 0 so the attack cant be spammed 
        ################ EXACT SAME AS ABOVE WITH RIGHT DIRECTION
        elif Flashrect.colliderect(batRect) and EDir == 1:
            newMove3 = Punch
            FLASH[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 2:
                HEALTH -=10
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        else:
            newMove3 = -1
            frame3 = 0

        if move3 == newMove3:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame3 = frame3 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame3 >= len(FlashPics[move3]):
                frame3 = 1
        elif newMove3 != -1:     # a move was selected
            move3 = newMove3      # make that our current move
            frame3 = 0
########## THE MOVEMENT FOR IRONMAN HAS THE SAME FORMAT AS FLASH'S MOVEMENT ####################
def move_Iron(Iron_man): ### MOVING IRONMAN
    global newMove4, frame4, offset, BATMAN, running, Count, move4, batRect, EDir, HEALTH, heal
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    newMove4 = -1
    if Boss == True:

        if (BATMAN[X]) < Iron_man[X] and Iron_man[X] > 540 and not IronRect.colliderect(batRect):
            newMove4 = LEFT
            EDir = -1
            Iron_man[X] -=10

        elif (BATMAN[X]) > Iron_man[X] and Iron_man[X] < 4050 and not IronRect.colliderect(batRect):
            newMove4 = RIGHT
            EDir = 1
            Iron_man[X] +=10

        elif IronRect.colliderect(batRect) and EDir == -1:
            newMove4 = Punchleft
            Iron_man[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 15:
                HEALTH -=60
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        elif IronRect.colliderect(batRect) and EDir == 1:
            newMove4 = Punch
            Iron_man[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 15:
                HEALTH -= 60
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        else:
            newMove4 = -1
            frame4 = 0

        if move4 == newMove4:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame4 = frame4 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame4 >= len(IronPics[move4]):
                frame4 = 1
        elif newMove4 != -1:     # a move was selected
            move4 = newMove4      # make that our current move
            frame4 = 0
########### THE MOVEMENT FOR SUPERMAN HAS THE SAME FORMAT AS FLASH'S MOVEMENT #############
def move_Super(Super_man): ## MOVING SUPERMAN
    global newMove5, frame5, offset, BATMAN, running, Count, move5, batRect, EDir, HEALTH, heal
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    #################### MOVING Super man #######################
    newMove5 = -1
    if Boss == True:

        if (BATMAN[X]) < Super_man[X] and Super_man[X] > 540 and not SuperRect.colliderect(batRect):
            newMove5 = LEFT
            EDir = -1
            Super_man[X] -=10

        elif (BATMAN[X]) > Super_man[X] and Super_man[X] < 4050 and not SuperRect.colliderect(batRect):
            newMove5 = RIGHT
            EDir = 1
            Super_man[X] +=10

        elif SuperRect.colliderect(batRect) and EDir == -1:
            newMove5 = Punchleft
            Super_man[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 15:
                HEALTH -= 60
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        elif SuperRect.colliderect(batRect) and EDir == 1:
            newMove5 = Punch
            Super_man[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 15:
                HEALTH -= 60
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        else:
            newMove5 = -1
            frame5 = 0

        if move5 == newMove5:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame5 = frame5 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame5 >= len(SuperPics[move5]):
                frame5 = 1
        elif newMove5 != -1:     # a move was selected
            move5 = newMove5      # make that our current move
            frame5 = 0
#THE MOVEMENT FOR THANOS HAS THE SAME FORMAT AS FLASH'S MOVEMENT
def Mover_Thanos(Thanos): ### MOVING THANOS 
    global newMove6, frame6, offset, BATMAN, running, Count, move6, batRect, EDir, HEALTH, heal, ThanosRect
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    newMove6 = -1
    if Boss == True:

        if (BATMAN[X]) < Thanos[X] and Thanos[X] > 540 and not ThanosRect.colliderect(batRect):
            newMove6 = LEFT
            EDir = -1
            Thanos[X] -=10

        elif (BATMAN[X]) > Thanos[X] and Thanos[X] < 4050 and not ThanosRect.colliderect(batRect):
            newMove6 = RIGHT
            EDir = 1
            Thanos[X] +=10

        elif ThanosRect.colliderect(batRect) and EDir == -1:
            newMove6 = Punchleft
            Thanos[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 5:
                HEALTH -=80
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        elif ThanosRect.colliderect(batRect) and EDir == 1:
            newMove6 = Punch
            Thanos[X] += 0
            Count += 1
            if HEALTH > 0 and Count == 5:
                HEALTH -=80
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

        else:
            newMove6 = -1
            frame6 = 0

        if move6 == newMove6:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame6 = frame6 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame6 >= len(ThanosPics[move6]):
                frame6 = 1
        elif newMove6 != -1:     # a move was selected
            move6 = newMove6      # make that our current move
            frame6 = 0

def moveAliens(aliensRect): # MOVING THE ALIENS 
    global newMove2, frame2, BATMAN, offset, HEALTH, heal, running, move2, enemy, HEALTH_Constant
    ############ MOVING THE ENEMY ###################
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    for i in range(enemy):
        newMove2 = -1
        if (BATMAN[X] + offset) < aliensRect[i][0]: ## Checking if Batman's x is greater than alien's x
            newMove2 = LEFT
            eV=randint(1,7) # RANDOM SPEEDS SO THEY DONT PILE UP 
            aliensRect[i][0] -= eV
            
        if (BATMAN[X] + offset) > aliensRect[i][0]: ## Checking if Batman's x is less than the alien's x
            newMove2 = RIGHT
            eV=randint(1,7)
            aliensRect[i][0] += eV

    if move2 == newMove2:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame2 = frame2 + 0.2 # adding 0.2 allows us to slow down the animation
        if frame2 >= len(Epics[move2]):
            frame2 = 1
    elif newMove2 != -1:     # a move was selected
        move2 = newMove2      # make that our current move
        frame2 = 1

def drawscene(screen,BATMAN,level): ## THIS IS THE DRAW SCREEN

    global LEVEL1back, LEVEL2back, LEVEL3back, LEVEL4back, offset, Super_man, Thanos, batmobilepic, frame, move, frame2, move2, frame3, move3, FLASH, Flashrect, aliensRect, batRect, aliens, Iron_man, IronRect, move4, frame4, Diff, HEALTH, HEALTH_Constant, heal, Energy, energy, SuperRect, ThanosRect, move5, frame5, move6, frame6, numBandages, numEnergy
    offset = 540 - BATMAN[X]
    if level == "1": # IF LEVEL IS 1 
        screen.blit(LEVEL1back,(offset,0)) # BLIT THE FIRST LEVEL BACKGROUND
        screen.blit(batmobilepic,((50 + offset),622))
    elif level == "2": # IF LEVEL IS 2 
        screen.blit(LEVEL2back,(offset,0)) # BLIT THE SECOND LEVEL BACKGROUND

    elif level == "3": # IF LEVEL IS 3 
        screen.blit(LEVEL3back,(offset,0)) # BLIT THE THIRD LEVEL BACKGROUND

    elif level == "4": # IF LEVEL IS 4 
        screen.blit(LEVEL4back,(offset,0)) # BLIT THE 4TH LEVEL BACKGROUND

    for pl in plats: ## MOVING THE PLATS WITH OFFSET 
        p = pl.move(offset,0) #move horizentally only
        draw.rect(screen,(100,110,230),p)
    
    for m in range(numBandages): ## MOVING THE BANDAGES WITH OFFSET 
        for ba in bandages:
            b = ba.move(offset,0) #move horizentally only
    
            screen.blit(bandage,b)
            if b.colliderect(batRect): #and HEALTH < HEALTH_Constant:
                if HEALTH < HEALTH_Constant: ## IF HEALTH IS LESS THAN THE CONSTANT HEALTH WHICH STAYS THE SAME
                    HEALTH = HEALTH_Constant # MAKE HEALTH FULL
                    heal = 400 # MAKE THE WIDTH OF THE BAR FULL
                bandages[m].top = 1500 # SEND THE BANDAGE PIC TO A DIFFERENT Y LOCATION
                ############# SAME FORMAT AS THE BANDAGE
    for m in range(numEnergy):
        for en in energies:
            e = en.move(offset,0) #move horizentally only
            screen.blit(energyPic,e)
            if e.colliderect(batRect):# and HEALTH < HEALTH_Constant:
                if Energy < 100:
                    Energy = 100
                    energy = 225
                energies[m].top = 1500
    
    ###### Blitting batman
    pic = pics[move][int(frame)]
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)      
    screen.blit(pic, (540,BATMAN[Y]))
    
    ###### Blitting The ALiens
    pic_2 = Epics[move2][int(frame2)]
    pic2 = transform.scale(pic_2,(60,47))
    for i in range(enemy):
        aliensRect[i].move(offset,0)
        screen.blit(pic2,aliensRect[i])

    ################# THESE ARE THE RECTS FOR ALL THE BOSS'S
    Flashrect = Rect((FLASH[X] + offset),FLASH[Y],40,70)
    IronRect = Rect((Iron_man[X] + offset),Iron_man[Y],50,90)
    SuperRect = Rect((Super_man[X] + offset),Super_man[Y],50,90)
    ThanosRect = Rect((Thanos[X] + offset),Thanos[Y],50,90)

    if Boss == True and level == "1": # IF LEVEL IS 1 AND BOSS IS TRUE THEN BLIT FLASH
        pic_3 = FlashPics[move3][int(frame3)]
        pic3 = transform.scale(pic_3,(40,70))
        screen.blit(pic3,Flashrect)

    elif Boss == True and level == "2": # IF LEVEL IS 2 AND BOSS TRUE BLIT IRONMAN
        pic_4 = IronPics[move4][int(frame4)]
        pic4 = transform.scale(pic_4,(36,70))
        screen.blit(pic4,IronRect)

    elif Boss == True and level == "3": # IF LEVEL 3 AND BOSS TRUE THEN BLIT IRONMAN
        pic_5 = SuperPics[move5][int(frame5)]
        pic5 = transform.scale(pic_5,(36,70))
        screen.blit(pic5,SuperRect)

    elif Boss == True and level == "4": # IF LEVEL 4 AND BOSS TRUE THEN BLUT THANOS
        pic6 = ThanosPics[move6][int(frame6)]
        screen.blit(pic6,ThanosRect)
##################### THE CODE BELOW IS MOVEMENT FOR THE BULLETS ###############
    for b in bullets[:]: #CHECK FOR EACH BULLET
        b[0]+=b[2]
        b[1]+=b[3]

        if max(b) > 1080 or min(b) < -0: ## CHECKS IF THE BULLETS IS NO LONGER IN THE SCREEN
            bullets.remove(b) ## REMOVES THE BULLET FROM THE SCREEN
#################### SAME AS ABOVE JUST FOR LEFT SIDE
    for b in bullets:
        screen.blit(bullet,(int(b[0]),int(b[1])))

    for o in bullets2[:]:
        o[0]+=o[2]
        o[1]+=o[3]

        if max(o) < 0 or min(o) > 1080:
            bullets2.remove(o)

    for i in bullets2:
        screen.blit(bullet1,(int(i[0]),int(i[1])))

    enemyHealth()
    health()
    Boss_health()
    display_XP()
    display.flip()    

def checkCollide(BATMAN,plats): # THIS CHECKS FOR COLLISION WITH BATMAN AND THE PLATS
    batRect = Rect(BATMAN[X],BATMAN[Y],34,58)
    for p in plats:
        if batRect.colliderect(p):
                #falling down 
            if BATMAN[VY]>0 and batRect.move(0,-BATMAN[VY]).colliderect(p)==False:
                BATMAN[ONGROUND]=True
                BATMAN[VY] = 0
                BATMAN[Y] = p.y - 58 #size of player 

def Game(): # THIS IS LEVEL 1 OF THE GAME
    mixer.music.stop()
    mixer.music.load(music_List[1]) # PLAYING THE MUSIC 
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    global aliens,dead_counter, batRect, aliensRect, FLASH, Count, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, BossHealth, bossHeal, boss, XP, Flashrect, BATMAN, HEALTH, heal, heal2, Energy, energy, HEALTH_Constant, fill, enemy, Flashrect, numBandages, numEnergy, bandages, energies
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70) # MAKING THE BAT RECT
    Flashrect = Rect((FLASH[X] + offset),FLASH[Y],40,70) # MAKING THE FLASH RECT
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        ##############################################
        ######## Checking for collide with bullets and alien ###########
        keys = key.get_pressed()

        for m in range(enemy): # CHECKS IN RANGE OF ENEMY 

            if aliensRect[m].colliderect(batRect): # IF ALIENS COLLIDE WITH BATMAN
                newMove2 = Punchleft # PUNCH ANIMATION
                aliensRect[m][0] += 0 # STOP MOVING
                Count += 1 # COUNT INCREASES


            if HEALTH > 0 and Count == 30: # IF THE HEALTH IS GREATER THAN 0 AND COUNT IS 30
                HEALTH -=5 # REDUCE 5 FROM THE HEALTH 
                heal = int(heal * (HEALTH/HEALTH_Constant)) # TAKE THE PERCENTAGE AND MULTIPLY BY WIDTH
                Count = 0

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0: # IF THE B BUTTON IS PUSHED
                EhealthList[m] -= 100 # SUBTRACT 100 FROM THE ALIENS HEALTH LIST
                ehealList[m] = ehealList[m] * (EhealthList[m]/100) # TAKE PERCENTAGE AND MULTIPLY BY THE WIDTH
                Energy -= 25 # REDUCE THE AMOUNT OF ENERGY SO YOU CANT SPAM THE MOVE
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1 # INCREASE THE AMOUNT OF DEAD ALIENS BY 1
                    aliensRect[m].top = 1500 ## SEND THE ALIEN TO DIFFERENT y
                    XP +=100
                ### SAME FORMAT WITH ALIENS
            if keys[K_b] and Boss == True and batRect.colliderect(Flashrect) and Energy > 0:
                BossHealth[boss] -=50 ## TAKING THE BOSS INDEX 
                bossHeal += 100
                Energy -= 25
                energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i) # MAKE RECTS OF THE PICS 
                if r.colliderect(aliensRect[m]): ## IF COLLIDE
                    del bullets[bullets.index(i)] ## REMOVE 
                    EhealthList[m] -= 20
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1 ## INCREASE AMOUNT OF ALIENS DEAD
                        aliensRect[m].top = 1500 ## SEND THE ALIEN TO DIFFERENT y
                        XP += 100
                if Boss == True: ## IF BOSS IS TRUE
                    if r.colliderect(Flashrect): # IF THERE IS A COLLISION WITH FLASH
                        del bullets[bullets.index(i)] # DELETE BULLET
                        BossHealth[boss] -=10 # REDUCE THE HEALTH
                        bossHeal += 20

            ################ SAME FORMAT AS ABOVE JUST FOR LEFT SHOOTING ######################
            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -= 20
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500 ## SEND THE ALIEN TO DIFFERENT y
                        XP += 100

                if Boss == True:
                    if c.colliderect(Flashrect):
                        del bullets2[bullets2.index(i)]
                        BossHealth[boss] -=10
                        bossHeal += 20

            if dead_counter == len(aliensRect): # IF THE AMIUNT OF DEAD ALIENS = THE AMOUNT OF ALIENS
                Boss = True ## BOSS IS TRUE - SPAWN IN THE BOSS
            if batRect.colliderect(aliensRect[m]): # F BATMAN COLLIDES WITH ALIENN 
                pass # DONT DO ANYTHING
            if Boss == True: # IF BOSS IS TRUE 
                if BossHealth[0] <= 0: # IF THE HEALTH IS 0
                    FLASH[Y] = 1500 # SEND THE Y TO 1500
                    XP += 500 # INCREASE XP
                    Boss = False # SET BOSS TO BE FALSE
        if BossHealth[0] <=0 and Boss == False: ## IF BOSS IS FALSE AND THE HEALTH IS 0 
        ####################### THIS RESETS ALL THE VALUES AND POSITIONS 
            enemy = 20 # INCREASE THE NUMBER OF ALIENS BEING MADE
            aliens=[]
            aliens = [[randint(1100,4000),650] for x in range(enemy)] # 2d list with random x values
            aliensRect = [] # this is going to be a 2d list that will hold the rects
            for i in range(enemy):
                aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
            EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
            ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
            BATMAN = [540,650,0,True]  # Batmans position in the game
            heal = 400
            HEALTH = 200 ## INCREASE THE HEALTH 
            HEALTH_Constant = 200
            Energy = 100
            energy = 215
            fill[0] = 0 # FILL IN A WHITE CHEM
            dead_counter = 0 ## SET DEAD ALIENS TO 0 
            bandages=[] # MAKE BANDAGES EMPTY LIST
            energies=[] # EMPTY LIST
            ## CREATING NEW BANDAGES
            bandages = [Rect(1032,463,35,35),Rect(2032,463,35,35), Rect(3032,463,35,35),Rect(1032,328,35,35),Rect(2032,328,35,35),Rect(3032,328,35,35)]
            energies = [Rect(1532,463,35,35),Rect(2532,463,35,35),Rect(3532,463,35,35), Rect(1532,328,35,35),Rect(2532,328,35,35),Rect(3532,328,35,35)]
            numBandages=6
            numEnergy=6
            bossHeal = -400 ## RESETING BOSS HEALTH WIDTH 
            boss = 1 ## BOSS INDEX IS NOW 1 FOR BOSS HEALTH
            return "game2" ## CALL PAGE = GAME2

        if HEALTH <= 0: ## IF PLAYER HEALTH IS 0
            return "credits" # GAME OVER
        checkCollide(BATMAN,plats) # CALLING COLLISION
        moveBatman(BATMAN) # CALLING BATMAN MOVEMENT
        moveAliens(aliensRect) # CALLING ALIENS MOVEMENT 
        move_Flash(FLASH) # CALLING FLASH MOVEMENT 
        drawscene(screen,BATMAN,"1") # CALLING DRAWSCENE
        myClock.tick(25)
####################### THE FORMAT FOR GAME 2 IS THE SAME WITH MORE ENEMIES AND HARDER BOSS    
    return "menu" # RETURN MENU 

def Game2():
    mixer.music.stop()
    mixer.music.load(music_List[4]) # PLAY MUSIC
    mixer.music.play(-1)
    myClock = time.Clock()
    running = True
    global aliens,dead_counter, batRect, aliensRect, Count, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, XP, HEALTH, heal, HEALTH_Constant, IronRect, Iron_man, Boss_health, bossHeal, boss, Energy, BATMAN, energy, enemy, numBandages, numEnergy, bandages, energies
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "menu"

        keys = key.get_pressed()
        for m in range(enemy):

            if aliensRect[m].colliderect(batRect):
                newMove2 = Punchleft
                aliensRect[m][0] += 0
                Count += 1


            if HEALTH > 0 and Count == 40:
                HEALTH -=15
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0:
                EhealthList[m] -= 100
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                Energy -= 25
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1
                    aliensRect[m].top = 1500
                    XP +=100

            if keys[K_b] and Boss == True and batRect.colliderect(IronRect) and Energy > 0:
                BossHealth[boss] -=15
                bossHeal += 15
                Energy -= 25
                energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    del bullets[bullets.index(i)]
                    EhealthList[m] -= 20
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500
                        XP += 100

                if Boss == True:
                    if r.colliderect(IronRect):
                        del bullets[bullets.index(i)]
                        BossHealth[boss] -=15
                        bossHeal += 15

            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -= 20
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500
                        XP += 100

                if Boss == True:
                    if c.colliderect(IronRect):
                        del bullets2[bullets2.index(i)]
                        BossHealth[boss] -=15
                        bossHeal += 15

            if dead_counter == len(aliensRect):
                Boss = True
            if batRect.colliderect(aliensRect[m]):
                pass

            if Boss == True:
                if BossHealth[boss] <= 0:
                    Iron_man[Y] = 1500
                    XP += 1000
                    Boss = False
        if BossHealth[boss] <=0 and Boss == False:
            enemy = 30
            aliens=[]
            aliens = [[randint(1100,4000),650] for x in range(enemy)] # 2d list with random x values
            aliensRect = [] # this is going to be a 2d list that will hold the rects
            for i in range(enemy):
                aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
            EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
            ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
            BATMAN = [540,650,0,True]  # Batmans position in the game
            heal = 400
            HEALTH = 300 ## health of the player orignally = 100
            HEALTH_Constant = 300
            Energy = 100
            energy = 215
            fill[1] = 0
            dead_counter = 0
            bandages=[]
            energies=[]
            bandages = [Rect(1032,463,35,35),Rect(2032,463,35,35), Rect(3032,463,35,35),Rect(1032,328,35,35),Rect(2032,328,35,35),Rect(3032,328,35,35)]
            energies = [Rect(1532,463,35,35),Rect(2532,463,35,35),Rect(3532,463,35,35), Rect(1532,328,35,35),Rect(2532,328,35,35),Rect(3532,328,35,35)]
            numBandages=6
            numEnergy=6
            bossHeal = -400
            boss = 2
            return "game3"

        if HEALTH <= 0: # IF PLAYER DEAD
            return "credits" # GAME OVER 

        checkCollide(BATMAN,plats)    
        moveBatman(BATMAN)
        moveAliens(aliensRect)
        move_Iron(Iron_man) # CALLING MOVEMENT FOR IRONMAN
        drawscene(screen,BATMAN,"2")
        myClock.tick(25)
    return "menu"
############## FORMAT FOR LEVEL3 IS SAME AS 1 AND 2 
def Game3():
    mixer.music.stop()
    mixer.music.load(music_List[6]) # PLAY LEVEL 3 MUSIC 
    mixer.music.play(-1)
    myClock = time.Clock()
    running = True
    global aliens,dead_counter, batRect, aliensRect, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, XP, HEALTH, heal, HEALTH_Constant, Energy, BATMAN, enemy, energy, SuperRect, Super_man, bossHeal, BossHealth, boss, Count, numBandages, numEnergy, bandages, energies
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "menu"

        keys = key.get_pressed()
        for m in range(enemy):

            if aliensRect[m].colliderect(batRect):
                newMove2 = Punchleft
                aliensRect[m][0] += 0
                Count += 1


            if HEALTH > 0 and Count == 40:
                HEALTH -=5
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0:
                EhealthList[m] -= 100
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                Energy -= 25
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1
                    aliensRect[m].top = 1500
                    XP +=100

            if keys[K_b] and Boss == True and batRect.colliderect(SuperRect) and Energy > 0:
                BossHealth[boss] -=20
                bossHeal += 10
                Energy -= 25
                energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    del bullets[bullets.index(i)]
                    EhealthList[m] -= 20
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500
                        XP += 100

                if Boss == True:
                    if r.colliderect(SuperRect):
                        del bullets[bullets.index(i)]
                        BossHealth[boss] -=13
                        bossHeal += 10

            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -= 20
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500
                        XP += 100

                if Boss == True:
                    if c.colliderect(SuperRect):
                        del bullets2[bullets2.index(i)]
                        BossHealth[boss] -=13
                        bossHeal += 10

            if EhealthList[m] == 0:
                aliensRect[m].top = 1500
            if dead_counter == len(aliensRect):
                Boss = True
            if batRect.colliderect(aliensRect[m]):
                pass

            if Boss == True:
                if BossHealth[boss] <= 0:
                    Super_man[Y] = 1500
                    XP += 5000
                    Boss = False
        if BossHealth[boss] <=0 and Boss == False:
            enemy = 40
            aliens=[]
            aliens = [[randint(1100,4000),650] for x in range(enemy)] # 2d list with random x values
            aliensRect = [] # this is going to be a 2d list that will hold the rects
            for i in range(enemy):
                aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
            EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
            ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
            BATMAN = [540,650,0,True]  # Batmans position in the game
            heal = 400
            HEALTH = 500 ## health of the player orignally = 100
            HEALTH_Constant = 500
            Energy = 100
            energy = 215
            fill[2] = 0 # ADD ANOTHER FILLED GEM 
            dead_counter = 0
            bandages=[]
            energies=[]
            bandages = [Rect(1032,463,35,35),Rect(2032,463,35,35), Rect(3032,463,35,35),Rect(1032,328,35,35),Rect(2032,328,35,35),Rect(3032,328,35,35)]
            energies = [Rect(1532,463,35,35),Rect(2532,463,35,35),Rect(3532,463,35,35), Rect(1532,328,35,35),Rect(2532,328,35,35),Rect(3532,328,35,35)]
            numBandages=6
            numEnergy=6
            bossHeal = -400
            boss = 3
            return "game4"

        if HEALTH <= 0:
            return "credits"

        checkCollide(BATMAN,plats)    
        moveBatman(BATMAN)
        moveAliens(aliensRect)
        move_Super(Super_man) # CALLING SUPERMAN MOVEMENT 
        drawscene(screen,BATMAN,"3")
        myClock.tick(25)
########################## FORMAT FOR LEVE4 IS SAME AS 1 2 AND 3 
def Game4():
    mixer.music.stop()
    mixer.music.load(music_List[7]) # PLAY MUSIC 
    mixer.music.play(-1)
    myClock = time.Clock()
    running = True
    global aliens,dead_counter, batRect, aliensRect,Count, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, XP, HEALTH, heal, HEALTH_Constant, Energy, BATMAN, enemy, energy, bossHeal, BossHealth, boss,  bandages, energies, numEnergy, numBandages
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    while running:  
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "menu"
        keys = key.get_pressed()
        for m in range(enemy):

            if aliensRect[m].colliderect(batRect):
                newMove2 = Punchleft
                aliensRect[m][0] += 0
                Count += 1


            if HEALTH > 0 and Count == 40:
                HEALTH -=5
                heal = int(heal * (HEALTH/HEALTH_Constant))
                Count = 0

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0:
                EhealthList[m] -= 100
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                Energy -= 25
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1
                    aliensRect[m].top = 1500
                    XP +=100

            if keys[K_b] and Boss == True and batRect.colliderect(ThanosRect) and Energy > 0:
                BossHealth[boss] -=100
                bossHeal += 10
                Energy -= 25
                energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    del bullets[bullets.index(i)]
                    EhealthList[m] -= 50
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500
                        XP += 100

                if Boss == True:
                    if r.colliderect(ThanosRect):
                        del bullets[bullets.index(i)]
                        BossHealth[boss] -=10
                        bossHeal += 4

            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -=100
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        aliensRect[m].top = 1500
                        XP += 100

                if Boss == True:
                    if c.colliderect(ThanosRect):
                        del bullets2[bullets2.index(i)]
                        BossHealth[boss] -=10
                        bossHeal += 4

            if batRect.colliderect(aliensRect[m]):
                pass
        if dead_counter == len(aliensRect):
            Boss = True

        if Boss == True:
            if BossHealth[boss] <= 0:
                Thanos[Y] = 1500
                XP += 10000
                Boss = False
                    
        if BossHealth[boss] <=0 and Boss == False: # IF THE BOSS IS DEAD
            return "credits" # GAME OVER

        if HEALTH <= 0: # IF THE PLAYER IS DEAD 
            return "credits" # GAME OVER

        checkCollide(BATMAN,plats)  
        moveBatman(BATMAN)
        moveAliens(aliensRect)
        Mover_Thanos(Thanos)
        drawscene(screen,BATMAN,"4")
        myClock.tick(25)
    return "menu"    

def health(): # This is the player health function
    global fill, heal, energy
    draw.rect(screen,BLUE,(5,5,410,25),0)
    draw.rect(screen,BLUE,(5,35,225,20),0)
    draw.rect(screen,RED,(10,10,heal,15),0)
    draw.rect(screen,LightBLue,(10,40,energy,10),0)
    Gems = [Rect(5+x*40,45+20,35,15) for x in range(4)] ## This creates a row of rectangles 
    for i in range (len(Gems)):
        draw.rect(screen,WHITE,Gems[i],fill[i])

def Boss_health(): # This is the BOSS health function
    global BossHealth, bossHeal, boss, Boss
    if Boss == True:
        draw.rect(screen,BLUE,(1075,5,-410,25),0)
        draw.rect(screen,RED,(1070,10,bossHeal,15),0)

def enemyHealth(): # THIS IS THE ENEMY HEALTH FUNCTION
    global ehealList, enemy
    for i in range(enemy):
        draw.rect(screen,RED,(aliensRect[i][0],aliensRect[i][1]-20,35,5),0)
        draw.rect(screen,GREEN,(aliensRect[i][0],aliensRect[i][1]-20,ehealList[i],5),0)

def display_XP(): # THIS FUNCTION DISPLAYS THE XP 
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
Punch = 2
Punchleft = 3
Shoot = 4
ShootLeft = 5

pics = [] #2d list
pics.append(makeMove("Run",0,16))# RIGHT
pics.append(makeMove("RunLeft",0,16))# LEFT
pics.append(makeMove("Punch",0,11))# Punching
pics.append(makeMove("Punchleft",0,11))# Punching
pics.append(makeMove("Shoot",0,5))# Shooting
pics.append(makeMove("ShootLeft",0,5))# Shooting

Epics=[]
Epics.append(moveEnemy("alien",1,7))# RIGHT
Epics.append(moveEnemy("alien",8,14))# LEFT
Epics.append(moveEnemy("AlienPunch",0,8))# PUNCH
Epics.append(moveEnemy("AlienPunchLeft",0,8))# PUNCH LEFT

FlashPics = []
FlashPics.append(moveFlash("FlashRun",0,6))# Right 
FlashPics.append(moveFlash("FlashRunLeft",0,6))# Left
FlashPics.append(moveFlash("FlashPunch",0,4)) # Punch Right
FlashPics.append(moveFlash("FlashPunchLeft",0,4))# Punch Left

IronPics = []
IronPics.append(moveIronman("Ironman",0,6)) # RIGHT
IronPics.append(moveIronman("IronmanLeft",0,6)) # LEFT 
IronPics.append(moveIronman("IronmanPunch",0,4)) # PUNCH RIGHT 
IronPics.append(moveIronman("IronmanPunchLeft",0,4)) # PUNCH LEFT 

SuperPics = []
SuperPics.append(moveSuperman("SupermanRun",0,6)) # RIGHT 
SuperPics.append(moveSuperman("SupermanRunLeft",0,6)) # LEFT 
SuperPics.append(moveSuperman("SupermanPunch",0,4)) # PUNCH RIGHT 
SuperPics.append(moveSuperman("SupermanPunchLeft",0,4)) # PUNCH LEFT

ThanosPics = []
ThanosPics.append(moveThanos("ThanosRun",0,20)) # RIGHT 
ThanosPics.append(moveThanos("ThanosRunLeft",0,20)) # LEFT 
ThanosPics.append(moveThanos("ThanosPunch",0,12)) # PUNCH 
ThanosPics.append(moveThanos("ThanosPunchLeft",0,12)) # PUNCH LEFT

frame = 0     # current frame within the move
frame2 = 0
frame3 = 0
frame4 = 0
frame5 = 0
frame6 = 0

move = 0      # current move being performed (right, down, up, left)
move2 = 0
move3 = 0
move4 = 0
move5 = 0
move6 = 0

def instructions(): # INSTRUCTIONS SCREEN
    global music_List
    mixer.music.stop()
    mixer.music.load(music_List[2])
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

        if mb[0] == 1 and buttonRect.collidepoint(mx,my):
            return "game"

        screen.blit(cont_button,(940,10)) # blitting the button

        display.flip()
    return "menu"
        
def credit():
    global music_List
    mixer.music.stop()
    mixer.music.load(music_List[5])
    mixer.music.play(-1)
    running = True
    cred = image.load("images/credits.png")
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

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

running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = Game()    
    if page == "game2":
        page = Game2()
    if page == "game3":
        page = Game3()
    if page == "game4":
        page = Game4()
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()
    if page == "game_over":
        page == Game_over()

quit()
