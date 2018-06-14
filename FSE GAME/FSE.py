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
LEVEL3back=image.load("images/Level3Back.png")
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
music_List = ["Music/Menu music.mp3", "Music/Level1.wav", "Music/How to music.mp3", "Music/StoryMusic.mp3", "Music/Level2 music.mp3", "Music/Ending credits.mp3", "Music/Level3 music.mp3"] # This is the music list 
enemy = 10
XP = 0
fill = [2,2,2,2,2]

BATMAN = [540,650,0,True]  # Batmans position in the game
HEALTH = 100 ## health of the player orignally = 100
HEALTH_Constant = 100
heal = 400 ## this is the width of the players health bar
Energy = 100 ## this is the players energy for special moves
energy = 215
Dir = 1 # this is the direction used in bullets and bullets2 list
FLASH = [4050,650,0,True]  # This is FLASH's position in the game
FLASH_HEALTH = 150
Iron_man = [4050,650,0,True]
Iron_Health = 250
Boss = False ## This is a temporary boolean var to check if boss spawns or not
############## MAKING THE ALIEN'S RECTS #################################
aliens = [[randint(1100,4000),650] for x in range(enemy)] # 2d list with random x values
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

def moveIronman(name,start,end): # Moving for flash
    move4 = []

    for i in range(start,end+1):
        move4.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move4

def moveBatman(BATMAN): # This function deals with all of batman's movements
    global Boss, newMove, Dir, aliensRect, rapid, bullets, bullets2, frame, move, offset, running
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
    if keys[K_b] and Dir == 1:
        newMove = Punch

    if keys[K_b] and Dir == -1:
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

def move_Flash(FLASH):
    global newMove3, frame3, offset, BATMAN, running, move3, batRect, Dir, HEALTH, heal
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    #################### MOVING FLASH #######################
    newMove3 = -1
    if Boss == True:

        if (BATMAN[X]) < FLASH[X] and FLASH[X] > 540:
            newMove3 = LEFT
            Dir = -1
            FLASH[X] -=10

        elif (BATMAN[X]) > FLASH[X] and FLASH[X] < 4050:
            newMove3 = RIGHT
            Dir = 1
            FLASH[X] +=10

        else:
            newMove3 = -1
            frame3 = 0

        if move3 == newMove3:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame3 = frame3 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame3 >= len(Epics[move2]):
                frame3 = 1
        elif newMove3 != -1:     # a move was selected
            move3 = newMove3      # make that our current move
            frame3 = 0

def move_Iron(Iron_man):
    global newMove4, frame4, offset, BATMAN, running, move4, batRect, Dir, HEALTH, heal
    for evnt in event.get():          
            if evnt.type == QUIT:
                running = False

    keys = key.get_pressed()
    #################### MOVING FLASH #######################
    newMove4 = -1
    if Boss == True:

        if (BATMAN[X]) < Iron_man[X] and Iron_man[X] > 540:
            newMove4 = LEFT
            Dir = -1
            Iron_man[X] -=10

        elif (BATMAN[X]) > Iron_man[X] and Iron_man[X] < 4050:
            newMove4 = RIGHT
            Dir = 1
            Iron_man[X] +=10

        else:
            newMove4 = -1
            frame4 = 0

        if move4 == newMove4:     # 0 is a standing pose, so we want to skip over it when we are moving
            frame4 = frame4 + 0.4 # adding 0.2 allows us to slow down the animation
            if frame4 >= len(Epics[move2]):
                frame4 = 1
        elif newMove4 != -1:     # a move was selected
            move4 = newMove4      # make that our current move
            frame4 = 0

def drawscene(screen,BATMAN,level):

    global LEVEL1back, LEVEL2back, LEVEL3back, offset, batmobilepic, frame, move, frame2, move2, frame3, move3, FLASH, Flashrect, aliensRect, batRect, aliens, Iron_man, IronRect, move4, frame4
    offset = 540 - BATMAN[X]
    if level == "1":
        screen.blit(LEVEL1back,(offset,0))
        screen.blit(batmobilepic,((50 + offset),622))
    elif level == "2":
        screen.blit(LEVEL2back,(offset,0))
        pic2 = Epics[move2][int(frame2)]
        for i in range(20):
            aliensRect[i].move(offset,0)
            screen.blit(pic2,aliensRect[i])
            draw.rect(screen,RED,aliensRect[i],2)

    elif level == "3":
        screen.blit(LEVEL3back,(offset,0))

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
    Flashrect = Rect((FLASH[X] + offset),FLASH[Y],40,70)
    IronRect = Rect((Iron_man[X] + offset),Iron_man[Y],45,70)
    if Boss == True and level == "1":
        pic_3 = FlashPics[move3][int(frame3)]
        pic3 = transform.scale(pic_3,(40,70))
        screen.blit(pic3,Flashrect)
        draw.rect(screen,WHITE,Flashrect,2)

    elif Boss == True and level == "2":
        pic_4 = IronPics[move4][int(frame4)]
        pic4 = transform.scale(pic_4,(45,70))
        screen.blit(pic4,IronRect)
        draw.rect(screen,WHITE,IronRect,2)

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

    enemyHealth()
    health()
    display_XP()
    display.flip()   

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

    if move2 == newMove2:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame2 = frame2 + 0.2 # adding 0.2 allows us to slow down the animation
        if frame2 >= len(Epics[move2]):
            frame2 = 1
    elif newMove2 != -1:     # a move was selected
        move2 = newMove2      # make that our current move
        frame2 = 1  

def Game():
    mixer.music.stop()
    mixer.music.load(music_List[1])
    mixer.music.play(-1)
    running = True
    myClock = time.Clock()
    global aliens,dead_counter, batRect, aliensRect, FLASH, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, FLASH_HEALTH, XP, Flashrect, BATMAN, HEALTH, heal, heal2, Energy, energy, HEALTH_Constant, fill, enemy
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    while running:
        print(dead_counter,len(aliensRect),enemy)
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        ##############################################
        ######## Checking for collide with bullets and alien ###########
        keys = key.get_pressed()
        for m in range(10):

            if aliensRect[m].colliderect(batRect): ## Checking for collide between the aliens and Batman
                newMove2 = -1
                frame2 = 0
                aliensRect[m][0] +=0
                if HEALTH > 0:
                    HEALTH -=5
                    heal = int(heal * (HEALTH/HEALTH_Constant))

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0:
                EhealthList[m] -= 100
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                Energy -= 25
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1
                    XP +=100
            if keys[K_b] and Boss == True and batRect.colliderect(Flashrect) and Energy > 0:
                FLASH_HEALTH -=100
                Energy -= 25
                energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets[bullets.index(i)]
                    EhealthList[m] -= 100
                    # print(EhealthList)
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        XP += 100
                if Boss == True:
                    if r.colliderect(Flashrect):
                        del bullets[bullets.index(i)]
                        FLASH_HEALTH -= 100


            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -=100
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        XP += 100

                if Boss == True:
                    if c.colliderect(Flashrect):
                        del bullets2[bullets2.index(i)]
                        FLASH_HEALTH -= 100

            if EhealthList[m] == 0:
                aliensRect[m].top = 1500
            if dead_counter == len(aliensRect):
                Boss = True
            if batRect.colliderect(aliensRect[m]):
                pass
            if Boss == True:
                if FLASH_HEALTH <= 0:
                    FLASH[Y] = 1500
                    XP += 500
                    dead_counter = 0
                    print("boss False")
                    Boss = False
        if FLASH_HEALTH <=0 and Boss == False:
            enemy = 20
            aliens=[]
            aliens = [[randint(1100,4000),650] for x in range(enemy)] # 2d list with random x values
            aliensRect = [] # this is going to be a 2d list that will hold the rects
            for i in range(enemy):
                aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
            EhealthList = [100 for x in range(enemy)] # this is the aliens health starting at 100
            ehealList = [35 for x in range(enemy)] # this is the width of the alien health bar
            BATMAN = [540,650,0,True]  # Batmans position in the game
            heal = 400
            HEALTH = 200 ## health of the player orignally = 100
            HEALTH_Constant = 200
            Energy = 100
            fill[0] = 0
            dead_counter = 0
            return "game2"
        moveBatman(BATMAN)
        moveAliens(aliensRect)
        move_Flash(FLASH)
        drawscene(screen,BATMAN,"1")
        myClock.tick(25)
    
    return "menu"

def Game2():
    mixer.music.stop()
    mixer.music.load(music_List[4])
    mixer.music.play(-1)
    myClock = time.Clock()
    running = True
    global aliens,dead_counter, batRect, aliensRect, FLASH, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, XP, HEALTH, heal, HEALTH_Constant, IronRect, Iron_man, Iron_Health, Energy, BATMAN, energy, enemy
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    while running:
        print(dead_counter,len(aliensRect),enemy)
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "menu"

        keys = key.get_pressed()
        for m in range(enemy):

            if aliensRect[m].colliderect(batRect): ## Checking for collide between the aliens and Batman
                newMove2 = -1
                frame2 = 0
                aliensRect[m][0] +=0
                if HEALTH > 0:
                    HEALTH -=5
                    heal = int(heal * (HEALTH/HEALTH_Constant))

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0:
                EhealthList[m] -= 100
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                Energy -= 25
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1
                    XP +=100

            if keys[K_b] and Boss == True and batRect.colliderect(IronRect) and Energy > 0:
                Iron_Health -=100
                Energy -= 25
                energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets[bullets.index(i)]
                    EhealthList[m] -= 100
                    # print(EhealthList)
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        XP += 100

                if Boss == True:
                    if r.colliderect(IronRect):
                        del bullets[bullets.index(i)]
                        Iron_Health -= 100

            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -=100
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        XP += 100

                if Boss == True:
                    if c.colliderect(IronRect):
                        del bullets2[bullets2.index(i)]
                        Iron_Health -= 100

            if EhealthList[m] == 0:
                aliensRect[m].top = 1500
            if dead_counter == len(aliensRect):
                Boss = True
            if batRect.colliderect(aliensRect[m]):
                pass

            if Boss == True:
                if Iron_Health <= 0:
                    Iron_man[Y] = 1500
                    XP += 500
                    dead_counter = 0
                    print("boss False")
                    Boss = False
        if Iron_Health <=0 and Boss == False:
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
            fill[1] = 0
            dead_counter = 0
            return "game3"

        moveBatman(BATMAN)
        moveAliens(aliensRect)
        move_Iron(Iron_man)
        drawscene(screen,BATMAN,"2")
        myClock.tick(25)
    return "menu"

def Game3():
    mixer.music.stop()
    mixer.music.load(music_List[6])
    mixer.music.play(-1)
    myClock = time.Clock()
    running = True
    global aliens,dead_counter, batRect, aliensRect, FLASH, bullets, bullets2, bullet, bullet1, EhealthList, ehealList, Boss, XP, HEALTH, heal, HEALTH_Constant, Energy, BATMAN, enemy, energy
    batRect = Rect((BATMAN[X] + offset),BATMAN[Y],40,70)
    while running:
        #print("Hello from l2")
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "menu"

        keys = key.get_pressed()
        for m in range(enemy):

            if aliensRect[m].colliderect(batRect): ## Checking for collide between the aliens and Batman
                newMove2 = -1
                frame2 = 0
                aliensRect[m][0] +=0
                if HEALTH > 0:
                    HEALTH -=5
                    heal = int(heal * (HEALTH/HEALTH_Constant))

            if  keys[K_b] and batRect.colliderect(aliensRect[m]) and Energy > 0:
                EhealthList[m] -= 100
                ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                Energy -= 25
                energy = energy * (Energy/100)
                if EhealthList[m] <=0:
                    dead_counter += 1
                    XP +=100

            # if keys[K_b] and Boss == True and batRect.colliderect(IronRect) and Energy > 0:
            #     Iron_Health -=100
            #     Energy -= 25
            #     energy = energy * (Energy/100)

            for i in bullets:
                r = Rect(i)
                if r.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets[bullets.index(i)]
                    EhealthList[m] -= 100
                    # print(EhealthList)
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        XP += 100

                # if Boss == True:
                #     if r.colliderect(IronRect):
                #         del bullets[bullets.index(i)]
                #         Iron_Health -= 100

            for i in bullets2:
                c = Rect(i)
                if c.colliderect(aliensRect[m]): 
                    # print('alien killed')
                    del bullets2[bullets2.index(i)]
                    EhealthList[m] -=100
                    ehealList[m] = ehealList[m] * (EhealthList[m]/100)
                    if EhealthList[m] <= 0:
                        dead_counter += 1
                        XP += 100

                # if Boss == True:
                #     if c.colliderect(IronRect):
                #         del bullets2[bullets2.index(i)]
                #         Iron_Health -= 100

            if EhealthList[m] == 0:
                aliensRect[m].top = 1500
            if dead_counter == len(aliensRect):
                Boss = True
            if batRect.colliderect(aliensRect[m]):
                pass

            # if Boss == True:
            #     if Iron_Health <= 0:
            #         Iron_man[Y] = 1500
            #         XP += 500
            #         dead_counter = 0
            #         print("boss False")
            #         Boss = False
        # if Iron_Health <=0 and Boss == False:
        #     aliens=[]
        #     aliens = [[randint(1100,4000),650] for x in range(30)] # 2d list with random x values
        #     aliensRect = [] # this is going to be a 2d list that will hold the rects
        #     for i in range(30):
        #         aliensRect.append(Rect(aliens[i][0],660,44,60)) ## taking the x value and appending y,w,h values
        #     EhealthList = [100 for x in range(30)] # this is the aliens health starting at 100
        #     ehealList = [35 for x in range(30)] # this is the width of the alien health bar
        #     BATMAN = [540,650,0,True]  # Batmans position in the game
        #     heal = 400
        #     HEALTH = 300 ## health of the player orignally = 100
        #     HEALTH_Constant = 300
        #     Energy = 100
        #     fill[2] = 0
        #     dead_counter = 0
        #     return "game3"

        moveBatman(BATMAN)
        moveAliens(aliensRect)
        drawscene(screen,BATMAN,"3")
        myClock.tick(25)
    return "menu"    

def health(): # This is the player health function
    global fill, heal, energy
    draw.rect(screen,BLUE,(5,5,410,25),0)
    draw.rect(screen,BLUE,(5,35,225,20),0)
    draw.rect(screen,RED,(10,10,heal,15),0)
    draw.rect(screen,LightBLue,(10,40,energy,10),0)
    Gems = [Rect(5+x*40,45+20,35,15) for x in range(5)] ## This creates a row of rectangles 
    for i in range (len(Gems)):
        draw.rect(screen,WHITE,Gems[i],fill[i])

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
Punchleft = 4

pics = [] #2d list
pics.append(makeMove("Run",0,16))# RIGHT
pics.append(makeMove("RunLeft",0,16))# LEFT
pics.append(makeMove("Jump",0,4))# Jumping
pics.append(makeMove("Punch",0,11))# Punching
pics.append(makeMove("Punchleft",0,11))# Punching

Epics=[]
Epics.append(moveEnemy("alien",1,7))# RIGHT
Epics.append(moveEnemy("alien",8,14))# LEFT

FlashPics = []
FlashPics.append(moveFlash("FlashRun",0,6))# Right 
FlashPics.append(moveFlash("FlashRunLeft",0,6))# Left
FlashPics.append(moveFlash("FlashPunch",0,4)) # Punch Right
FlashPics.append(moveFlash("FlashPunchLeft",0,4))# Punch Left

IronPics = []
IronPics.append(moveIronman("Ironman",0,6))
IronPics.append(moveIronman("IronmanLeft",0,6))
IronPics.append(moveIronman("IronmanPunch",0,4))
IronPics.append(moveIronman("IronmanPunchLeft",0,4))

frame = 0     # current frame within the move
move = 0      # current move being performed (right, down, up, left)
frame2 = 0
move2 = 0
frame3 = 0
move3 = 0
frame4 = 0
move4 = 0

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
    mixer.music.load(music_List[5])
    mixer.music.play()
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
    print(page)
    if page == "menu":
        page = menu()
    if page == "game":
        print("starting game")
        page = Game()    
    if page == "game2":
        print("starting level 2")
        page = Game2()
    if page == "game3":
        print("starting level 2")
        page = Game3()
    if page == "instructions":
        page = instructions()    
    if page == "story":
        page = story()    
    if page == "credits":
        page = credit()

quit()
