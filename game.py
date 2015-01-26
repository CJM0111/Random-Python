# This is a game in which Pokemon ride hoverboards while avoiding pokeballs
# Author: Chris McDonald
#!/usr/bin/env python
# PyGame module/library
import pygame
import time
import random
# used in every game using PyGame to initialize the library
pygame.init()

# variable for the screen resolution
display_width = 800
display_height = 600
# initializes color variables using RGB
black = (0,0,0)
white = (255,255,255)
red = (255,50,50)
green = (0,255,0)
blue = (0,0,255)
orange = (255,137,0)
light_red = (200,0,0)
light_green = (0,200,0)
yellow = (246,253,28)
orange = (255,171,24)

# pause state
pause = False
# the main frame/screen which houses the game
# the parameter for this function is the resolution/size of the frame
gameDisplay = pygame.display.set_mode((display_width,display_height),0,32)
# game title
pygame.display.set_caption('Python')
# internal game clock
clock = pygame.time.Clock()
# images used inside the game
waterImg = pygame.image.load('PNG/Water Block.png')
grassImg = pygame.image.load('PNG/Grass Block.png')
treeImg = pygame.image.load('PNG/Tree Tall.png')
bushImg = pygame.image.load('PNG/Tree Short.png')
pokeballImg = [pygame.image.load('images/pokeball.png'),pygame.image.load('images/greatball.png'),pygame.image.load('images/ultraball.png'),pygame.image.load('images/masterball.png')]
starImg = pygame.image.load('PNG/Star.png')
hoverImg = pygame.image.load('images/hover.png')
backgroundImg = pygame.image.load('images/space.png')
global msg
global pokemon
# default pokemon - pikachu
pokemon = "25"
msg = "null"
global pokemonImg
pokemonImg = pygame.image.load('images/%s.png' % (pokemon))
# dimensions of the grass block
grass_height = 171
grass_width = 101
# dimensions of the tree
tree_height = 171
tree_width = 101
# initialize a list called forest to hold the x coordinate of a tree
forestX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# initialize a list called forest to hold the y coordinate of a tree
forestY = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# initial layout of the forest
for x in range(0,20):
    forestX[x] = random.randrange(0,display_width)
    forestY[x] = random.randrange(-100,tree_height-100)
# dimensions of the bush
bush_height = 171
bush_width = 101
# initialize a list called shrubbery to hold the x coordinate of a bush
shrubX = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# initialize a list called shrubbery to hold the y coordinate of a bush
shrubY = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# initial layout of the shrubbery
for x in range(0,20):
    shrubX[x] = random.randrange(0,display_width)
    shrubY[x] = random.randrange(-100,tree_height-100)
# dimensions of the pokeball
pokeball_height = 50
pokeball_width = 50
# dimensions of the pokemon
pokemon_height = 96
pokemon_width = 96
# dimensions of the hoverboard
hover_height = 50
hover_width = 50
# initialize the list for the object to dodge (X)
object_startx = [0,0,0]
# initialize the list for the object to dodge (Y)
object_starty = [0,0,0]
# function to display the score
def things_dodged(count):
    font = pygame.font.Font(None,25)
    text = font.render(str(count), True, blue)
    gameDisplay.blit(starImg,(0,-55))
    gameDisplay.blit(text, (33,35))
# function to display the water
def water(w,h):
    gameDisplay.blit(waterImg,(w,h))
# function to display the grass
def grass(w,h):
    gameDisplay.blit(grassImg,(w,h))
# function to display a tree
def tree():
    for x in range(0,20):
        gameDisplay.blit(treeImg,(shrubX[x],shrubY[x]))
# function to display a bush
def bush():
    for x in range(0,20):
        gameDisplay.blit(bushImg,(shrubX[x],shrubY[x]))
# function to display a pokeball
def ball(w,h,x):
    gameDisplay.blit(pokeballImg[x],(w,h))
# function to display a hoverboard
def hover(w,h):
    gameDisplay.blit(hoverImg,(w,h))
# function to display a pokemon
def mypokemon(w,h):
    pokemonImg = pygame.image.load('images/%s.png' % (pokemon))
    gameDisplay.blit(pokemonImg,(w,h))
# function to fill the screen with an object
def fillObject(x,y,xMax,yMax,objectW,objectH):
    y_init = y
    while x < xMax:
        while y < yMax:
            if y < 50 + (grass_height/2):
                grass(x,y)
            else:
                water(x,y)
            y += objectH/2
        x += objectW
        y = y_init
# function to generate random locations for the object to dodge
def objectXY(number):
    # loop to generate a random number of object's coordinates
    for i in range(0,number):
        # initial location of the object to dodge inside the game
        object_startx[i] = random.randrange(-500,-50)
        object_starty[i] = random.randrange(pokeball_height+135,display_height-pokeball_height)
# function for the text objects
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
# function to display messages to the user
def message_display(text):
    largeText = pygame.font.Font('fonts/Capture.ttf', 97)
    TextSurf, TextRect = text_objects(text, largeText, blue)
    TextRect.center = ((display_width/2,display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()
    time.sleep(2)
    game_loop()
# function to handle crashing
def crash():
    global pokemon
    global msg
    largeText = pygame.font.Font('fonts/Capture.ttf', 57)
    TextSurf, TextRect = text_objects('Out of Bounds', largeText, orange)
    TextRect.center = ((display_width/2,display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        button("Play Again",'images/green.png',125,350,100,50,green,light_green,game_loop)
        button("Quit",'images/red.png',525,350,100,50,red,light_red,quitgame)
        if msg == "Squirtle":
            pokemon = "7"
        if msg == "Bulbasaur":
            pokemon = "1"
        if msg == "Charmander":
            pokemon = "4"
        pygame.display.update()
        clock.tick(15)
# function to handle being captured
def captured():
    global msg
    global pokemon
    largeText = pygame.font.Font('fonts/Capture.ttf', 57)
    TextSurf, TextRect = text_objects('You Were Captured', largeText, orange)
    TextRect.center = ((display_width/2,display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        button("Play Again",'images/green.png',125,350,100,50,green,light_green,game_loop)
        button("Quit",'images/red.png',525,350,100,50,red,light_red,quitgame)
        if msg == "Squirtle":
            pokemon = "7"
if msg == "Bulbasaur":
    pokemon = "1"
        if msg == "Charmander":
            pokemon = "4"
    pygame.display.update()
        clock.tick(15)
# function to create buttons
def button(msg,file,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    gameDisplay.blit(pygame.image.load(file),(x,y))
    if x+w+25 > mouse[0] > x and y+h+80 > mouse[1] > y:
        if click[0] == 1 and action != None:
            action()

smallText = pygame.font.Font("fonts/sea.ttf",20)
    textSurf, textRect = text_objects(msg, smallText, blue)
    textRect.center = ( (x+(w/2)+25), (y+(h/2)+50) )
    gameDisplay.blit(textSurf, textRect)
# function to select the starting pokemon for the game
def poke(file,x,y,w,h,ic,ac):
    global pokemon
    global msg
    global msgI
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    gameDisplay.blit(pygame.image.load(file),(x+10,y-pokemon_height-5))
    if x+pokemon_width > mouse[0] > x+10 and y > mouse[1] > y-pokemon_height:
        if click[0] == 1:
            if x == 150:
                pokemon = "7"
                msg = "Squirtle"
            if x == 350:
                pokemon = "1"
                msg = "Bulbasaur"
            if x == 550:
                pokemon = "4"
                msg = "Charmander"
    # gengar
    if 50 > mouse[0] > 0 and 50 > mouse[1] > 0:
        pokemon = "94"
        msg = "null"
    # mew
    if display_width > mouse[0] > display_width-50 and 50 > mouse[1] > 0:
        pokemon = "151"
        msg = "null"
    smallText = pygame.font.Font("fonts/LG.otf",20)
    textSurf, textRect = text_objects(msgI, smallText, white)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
# function to display a message saying the pokemon has evolved
def evolveMessage(N,oN):
    # display original pokemon name
    largeText = pygame.font.Font("fonts/Capture.ttf",57)
    TextSurf, TextRect = text_objects(oN,largeText, white)
    TextRect.center = ((display_width/2),(display_height/4-100))
    gameDisplay.blit(TextSurf, TextRect)
    # evolved
    largeText = pygame.font.Font("fonts/Capture.ttf",57)
    TextSurf, TextRect = text_objects("EVOLVED INTO", largeText, white)
    TextRect.center = ((display_width/2),(display_height/4))
    gameDisplay.blit(TextSurf, TextRect)
    # display evolved pokemon name
    largeText = pygame.font.Font("fonts/Capture.ttf",57)
    TextSurf, TextRect = text_objects(N,largeText, white)
    TextRect.center = ((display_width/2),(display_height/4+100))
    gameDisplay.blit(TextSurf, TextRect)
# function to allow pokemon to evolve - change the image
def evolve(d,x,msg):
    global pokemon
    if d == x and msg == "Squirtle":
        pokemon = "8"
        originalName = "SQUIRTLE"
        name = "WARTORTLE"
        evolveMessage(name, originalName)
    if d == x*2 and msg == "Squirtle":
        pokemon = "9"
        originalName = "WARTORTLE"
        name = "BLASTOISE"
        evolveMessage(name, originalName)
    if d == x and msg == "Bulbasaur":
        pokemon = "2"
        originalName = "BULBASAUR"
        name = "IVYSAUR"
        evolveMessage(name, originalName)
    if d == x*2 and msg == "Bulbasaur":
        pokemon = "3"
        originalName = "IVYSAUR"
        name = "VENUSAUR"
        evolveMessage(name, originalName)
    if d == x and msg == "Charmander":
        pokemon = "5"
        originalName = "CHARMANDER"
        name = "CHARMELEON"
        evolveMessage(name, originalName)
    if d == x*2 and msg == "Charmander":
        pokemon = "6"
        originalName = "CHARMELEON"
        name = "CHARIZARD"
        evolveMessage(name, originalName)
# function to terminate the game
def quitgame():
    pygame.quit()
    quit()
# function to unpause the game
def unpause():
    global pause
    pause = False
# function for pausing the game
def paused():
    largeText = pygame.font.Font("fonts/Capture.ttf",97)
    TextSurf, TextRect = text_objects("Paused", largeText, orange)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue",'images/green.png',125,350,100,50,green,light_green,unpause)
        button("Quit",'images/red.png',525,350,100,50,red,light_red,quitgame)

        pygame.display.update()
        clock.tick(15)
# game menu
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(backgroundImg,(0,0))
        largeText = pygame.font.Font('fonts/f.ttf', 47)
        TextSurf, TextRect = text_objects("POKEMON ON HOVERBOARDS", largeText, orange)
        TextRect.center = ((display_width/2,display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        # displays the buttons for the start menu
        button("Go!",'images/green.png',125,350,100,50, green, light_green, game_loop)
        button("Quit",'images/red.png',525,350,100,50, red, light_red, quitgame)
        # holds the name of the pokemon for the text displayed under said pokemon
        global msgI
        msgI = "Squirtle"
        poke("images/7.png",150,200,100,50, yellow, orange)
        msgI = "Bulbasaur"
        poke("images/1.png",350,200,115,50, yellow, orange)
        msgI = "Charmander"
        poke("images/4.png",550,200,140,50, yellow, orange)
        
        # updates the location of the image
        global pokemonImg
        pokemonImg = pygame.image.load('images/%s.png' % (pokemon))
        pygame.display.update()
        clock.tick(15)
# function for the main game loop
def game_loop():
    
    global pause
    global msg
    # starting location of the pokemon on the hoverboard
    x = display_width - pokemon_width + 10
    y = display_height * 0.55
    # stores the change in the location of the user's character
    y_change = 0
    # initialize the list to hold the maximum number of objects
    numObjects = 3
    objectXY(numObjects)
    # initialize a random number of objects
    numObjects = random.randrange(1,4)
    # initial speed of the object to dodge inside the game
    thing_speed = 15
    # the key repeat is disabled by default
    # set_repeat enables this capability
    pygame.key.set_repeat(1,50)
    # initial score
    dodged = 0
    # movement speed
    speed = 35;
    # initial pokeball type
    pokeballType = [0,0,0]
    # game loop - logic behind the game
    # set of conditions for exiting the game
    gameExit = False
    while not gameExit:
        # retrieves any event that occurs - handled by PyGame
        # event check loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # events for pressing a key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -1*speed
                if event.key == pygame.K_DOWN:
                    y_change = speed
                # option to pause the game
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    y_change = 0
            # changes the location of the pokemon
            y += y_change
        # background color for the window
        gameDisplay.fill(white)
        # fillObject(x,y,xMax,yMax,objectW,objectH)
        # x,y: initial coordinates
        # xMax, yMax: boundary for the object
        # objectW, objectH: dimensions of the object
        fillObject(0,-100,display_width,display_width,grass_width,grass_height)
        # landscape
        tree()
        bush()
        # after a certain interval (x), evolve the pokemon
        evolve(dodged,50,msg)
        # character on the hoverboard
        hover(x,y+35)
        mypokemon(x,y)
        for i in range(0,numObjects):
            ball(object_startx[i],object_starty[i],pokeballType[i])
            object_startx[i] += thing_speed
            things_dodged(dodged)
            # game logic
            # game boundaries
            if object_startx[i] > display_width:
                # resets the position of the pokeballs after they go off the screen
                object_startx[i] = random.randrange(-800,-200)
                object_starty[i] = random.randrange(pokeball_height+135,display_height-pokeball_height)
                # adds 1 to the total score
                dodged += 1
                # increases the speed of the pokeballs to be dodged
                thing_speed += .4
                # after a set number of pokeballs have been dodged, then randomize the # of pokeballs
                if dodged == 20:
                    numObjects = 3
                # changes the pokeball type
                pokeballType[i] = random.randrange(0,4)
            # determines if the pokemon is captured (pokeball collides with the pokemon)
            if x+pokemon_width-75 < object_startx[i]:
                if object_starty[i]+pokeball_height-25 > y and object_starty[i]+pokeball_height < y+pokemon_height or object_starty[i] > y and object_starty[i] < y+pokemon_height:
                    captured()
        # boundaries for the game
        if y-pokemon_height+30 < grass_height/2 or y > display_height - pokemon_height + 25:
            crash()
        # updates the entire screen or updates a specific object by passing a parameter
        # pygame.display.flip() updates the entire window without an option to pass any parameters
        pygame.display.update()
        # FPS
        clock.tick(75)
# start menu for the game
game_intro()
# the main game function
game_loop()
# terminates PyGame properly
pygame.quit()
quit()
