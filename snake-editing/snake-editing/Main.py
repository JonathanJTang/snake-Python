'''
Project Name:
Authors: Jonathan Tang & Joseph Tang
Created on:

Edited 
'''
import turtle
import time
from ClassCaterpillar import *



pauseGame = False
pauseElapsed = 0
startGame = False
mouseX = 0 # instantaneous mouse x-coordinate
mouseY = 0 # instantaneous mouse y-coordinate
def buttonDetection(x, y):
    print("Mouse clicked")
    global mouseX # instantaneous mouse x-coordinate
    global mouseY # instantaneous mouse y-coordinate
    global startGame
    if mouseX >= 260 and mouseX <= 465 and mouseY >= 165 and mouseY <= 200: # if "Start" button is clicked
        startGame = True

def mouseMove(mousePosition):
    '''Only called when the mouse is moved'''
    global mouseX # had to use global variables
    global mouseY
    # get mouse coordinates (window coordinates)
    mouseX = mousePosition.x 
    mouseY = mousePosition.y
    print('{}, {}'.format(mouseX, mouseY)) # for debugging

def pauseGameHandler():
    """Called whenever the key for pause game is pressed"""
    print("space key pressed") #For debugging
    global textPrinter
    global pauseGame
    global pauseElapsed # stores the total time paused (accumulates with every pause)
    global pauseGameStampID
    '''global firstTime # not the best way, but it makes pauseTimerStart start only once - at the start of the pause
    '''
    if pauseGame == True:
        #unPauseGameGraphics
        #textPrinter.undo() #Remove "game paused" message
        #textPrinter.setpos(300, 200) # where the center of the text is
        textPrinter.clearstamp(pauseGameStampID)
        #textPrinter.clearstamp(pauseGameStampIDlist[-1])
        textPrinter.setpos(300, 110) # where the center of the text is
        
        # delete paused time from currentTime

        # pauseTimeStart is the benchmark of the start of the pause
        # pauseElapsed is the difference between pauseTimeStart and the time stamp of the moment the pause ends
        # pauseElapsed is a global variable. It stores the total time paused (accumulates with every pause)
        ''' NOTE: change variable names if it's confusing'''

        '''# not the best way, but it makes pauseTimerStart start only once - at the start of the pause
        if firstTime == True:
            firstTime = False   '''         
        
        '''###########################################
           ##             SEE HERE                  ##
           ###########################################'''
        # marks the time when the pause starts...or it's supposed to. 
        # It technically marks the time when the spacebar is pressed again to resume the game
        # and that isn't the full pause time
        # but it works, without me knowing why   
        pauseTimeStart = time.perf_counter()            
        
        # Print 3, 2, 1 before game resumes        
        for num in range(3,0,-1):
            # print the fancy 3, 2, 1 images
            textPrinter.shape("gamepaused-" + "{0}".format(num) + ".gif")
            #pauseGameStampIDlist.append(textPrinter.stamp())
            pauseGameStampID = textPrinter.stamp()

            # I don't know why, but removing the textPrinter.write messes up the whole thing. Try for yourself. Joseph
            textPrinter.write("   ", True, align="center", font=("Arial", 48, "normal")) # Display nothing
            
            time.sleep(1)
            textPrinter.undo()
            #textPrinter.clearstamp(pauseGameStampIDlist[-1])
            textPrinter.clearstamp(pauseGameStampID)
            '''                                  
            textPrinter.write("{0}".format(num), True, align="center", font=("Arial", 48, "normal"))
            time.sleep(1)
            textPrinter.undo()  '''
        # resumes game (after the "3, 2, 1")
        pauseGame = False
        # adds pause time interval to be subtracted from the current time
        pauseElapsed += time.perf_counter()-pauseTimeStart
        '''# allow program to start pauseTimer again for the next time the game is paused
        firstTime = True'''
                    
     
    else:
        pauseGame = True # pauses game
        #pauseGameGraphics
        pauseGameStampIDlist = []
        textPrinter.setpos(300, 110) # where the center of the text is
        textPrinter.shape("gamepaused-text.gif")
        pauseGameStampID = textPrinter.stamp()
        #pauseGameStampIDlist.append(textPrinter.stamp())

        #textPrinter.setpos(300, 200) # where the center of the text is
        #textPrinter.write("GAME PAUSED", True, align="center", font=("Arial", 48, "normal"))


def initGraphics(screenWidth, screenHeight):
    '''Initializes graphics for the game. Run only once.
        '''
    #Set up the screen object
    wn = turtle.Screen()
    wn.setup(screenWidth, screenHeight)
    #Bottom left corner (0,screenHeight), top right corner (screenWidth,0)
    #to make javascript-like coordinate system with (0,0) in the top left corner
    wn.setworldcoordinates(0, screenHeight, screenWidth, 0)
    #"""temporarily commented for easier debugging"""
    wn.tracer(0, delay=1) #Turn turtle animation off (only each 0th screen update is performed)
    wn.title("Caterpillar: Game 1") #Include current score in title?
    wn.colormode(255)

    #Set up the turtle objects
    caterpillarDrawer = turtle.Turtle() #will draw the caterpillar
    caterpillarDrawer.speed(0)
    caterpillarDrawer.penup() #This should be the default state of the turtle
    caterpillarDrawer.hideturtle() #This should be the default state of the turtle

    miscDrawer = turtle.Turtle() #will draw miscellaneous stuff: borders, scores, etc
    miscDrawer.speed(0)
    miscDrawer.penup() #This should be the default state of the turtle
    miscDrawer.hideturtle() #This should be the default state of the turtle
    
    global textPrinter
    textPrinter = turtle.Turtle() # will print text on screen when needed
    textPrinter.speed(0)
    textPrinter.penup() #This should be the default state of the turtle
    textPrinter.hideturtle() #This should be the default state of the turtle

    scorePrinter = turtle.Turtle() # will print the score on the screen
    scorePrinter.speed(0)
    scorePrinter.penup() #This should be the default state of the turtle
    scorePrinter.hideturtle() #This should be the default state of the turtle

    bonusObjDrawer = turtle.Turtle() # will draw bonus object on the screen
    bonusObjDrawer.speed(0)
    bonusObjDrawer.penup() #This should be the default state of the turtle
    bonusObjDrawer.hideturtle() #This should be the default state of the turtle

    #drawBackground
    #miscDrawer.setposition(?)
    shapes = [
    #Register images used so they can be used in turtle
    "snake-head-1-thinner.gif", # caterpillar head - up - green circle with two black eyes
    "snake-head-2-thinner.gif", # caterpillar head - left
    "snake-head-3-thinner.gif", # caterpillar head - down
    "snake-head-4-thinner.gif", # caterpillar head - right

    "snake-head-dead-1.gif", # dead caterpillar head - up - green circle with two red crosses
    "snake-head-dead-2.gif", # dead caterpillar head - left
    "snake-head-dead-3.gif", # dead caterpillar head - down
    "snake-head-dead-4.gif", # dead caterpillar head - right   
     
    "snake-body-40px.gif", # caterpillar body - plain green circle
    "snake-body-v-thinner.gif", # caterpillar body - vertical
    "snake-body-h-thinner.gif", # caterpillar body - horizontal
    # caterpillar curve
    "snake-curve-up-right.gif",
    "snake-curve-up-left.gif",
    "snake-curve-down-right.gif",
    "snake-curve-down-left.gif",


    "snake-tail-1.gif", # caterpillar tail - pointing up
    "snake-tail-2.gif", # caterpillar tail - pointing left
    "snake-tail-3.gif", # caterpillar tail - pointing down
    "snake-tail-4.gif", # caterpillar tail - pointing right
    "snake-tail-1-thinner.gif", # caterpillar tail - pointing up
    "snake-tail-2-thinner.gif", # caterpillar tail - pointing left
    "snake-tail-3-thinner.gif", # caterpillar tail - pointing down
    "snake-tail-4-thinner.gif", # caterpillar tail - pointing right

    "apple-2-40px.gif", # Bonus object - alternative apple (not good cuz it has white background)
    "apple-40px.gif", # Bonus object - apple (good cuz it has transparent background,
    "apple-2-40px.gif", # Bonus object - alternative apple (not good cuz it has white background)
    "apple-flash.gif",
    "welcome-background.gif", #  welcome screen leaf background + "caterpilar" text
    "welcome-button-instructions.gif",
    "welcome-button-instructions-hover.gif",
    "welcome-button-settings.gif",
    "welcome-button-settings-hover.gif",
    "welcome-button-start.gif",
    "welcome-button-start-hover.gif",
    "welcome-caterpillar-whole.gif", # caterpillar graphics on the left of welcome screen

    "gameover-button-menu.gif",
    "gameover-button-menu-hover.gif",
    "gameover-button-retry.gif",
    "gameover-button-retry-hover.gif",
    "gameover-text.gif",
    "gamepaused-3.gif",
    "gamepaused-2.gif",
    "gamepaused-1.gif",
    "gamepaused-text.gif",


    # ^^^ ADD NEW IMAGE HERE
    
    "leaf-green-40px.gif" # Bonus object - green leaf (from Khan Academy)
    ]
    for i in shapes:
        wn.register_shape(i)
    '''
    #Register images used so they can be used in turtle
    wn.register_shape("snake-head-1-thinner.gif") # caterpillar head - up - green circle with two black eyes
    wn.register_shape("snake-head-2-thinner.gif") # caterpillar head - left
    wn.register_shape("snake-head-3-thinner.gif") # caterpillar head - down
    wn.register_shape("snake-head-4-thinner.gif") # caterpillar head - right

    wn.register_shape("snake-head-dead-1.gif") # dead caterpillar head - up - green circle with two red crosses
    wn.register_shape("snake-head-dead-2.gif") # dead caterpillar head - left
    wn.register_shape("snake-head-dead-3.gif") # dead caterpillar head - down
    wn.register_shape("snake-head-dead-4.gif") # dead caterpillar head - right   
     
    wn.register_shape("snake-body-40px.gif") # caterpillar body - plain green circle
    wn.register_shape("snake-body-v-thinner.gif") # caterpillar body - vertical
    wn.register_shape("snake-body-h-thinner.gif") # caterpillar body - horizontal
    # caterpillar curve
    wn.register_shape("snake-curve-up-right.gif")

    wn.register_shape("snake-tail-1.gif") # caterpillar tail - pointing up
    wn.register_shape("snake-tail-2.gif") # caterpillar tail - pointing left
    wn.register_shape("snake-tail-3.gif") # caterpillar tail - pointing down
    wn.register_shape("snake-tail-4.gif") # caterpillar tail - pointing right
    wn.register_shape("snake-tail-1-thinner.gif") # caterpillar tail - pointing up
    wn.register_shape("snake-tail-2-thinner.gif") # caterpillar tail - pointing left
    wn.register_shape("snake-tail-3-thinner.gif") # caterpillar tail - pointing down
    wn.register_shape("snake-tail-4-thinner.gif") # caterpillar tail - pointing right

    wn.register_shape("leaf-green-40px.gif") # Bonus object - green leaf (from Khan Academy)
    wn.register_shape("apple-2-40px.gif") # Bonus object - alternative apple (not good cuz it has white background)
    wn.register_shape("apple-40px.gif") # Bonus object - apple (good cuz it has transparent background)
    wn.register_shape("apple-2-40px.gif") # Bonus object - alternative apple (not good cuz it has white background)
    
    '''
    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen after drawing with turtle

    return wn, caterpillarDrawer, miscDrawer, textPrinter, scorePrinter, bonusObjDrawer # returns screen & turtles


def oneGame():
    #Initialize variables
    isDead = False
    global startGame
    loopCount = 0
    loopsSinceLastSpeedIncrease = 0
    gameSpeed = 1
    loopInterval = 1/gameSpeed #Maybe too fast as the initial speed?

    #Variables potentially set by user
    xSquares = 15 #number of virtual squares in a row
    ySquares = 10 #number of virtual squares in a column
    gridSquareSideLength = 40 #in pixels; must be an integer

    #Things done by the program
    if not (xSquares >= 3 and ySquares >= 3):
        raise ValueError("xSquares and ySquares must both be greater than 3")

    screenWidth = xSquares * gridSquareSideLength #integer, in pixels
    screenHeight = ySquares * gridSquareSideLength #integer, in pixels

    wn, caterpillarDrawer, miscDrawer, textPrinter, scorePrinter, bonusObjDrawer = initGraphics(screenWidth,screenHeight)

    #Draw boundaries of game board
    miscDrawer.pensize(3)
    miscDrawer.setpos(0, 0)#top-left corner again
    miscDrawer.pendown()
    miscDrawer.setpos(0, gridSquareSideLength*ySquares) #bottom-left corner
    miscDrawer.setpos(gridSquareSideLength*xSquares, gridSquareSideLength*ySquares) #bottom-right corner
    miscDrawer.setpos(gridSquareSideLength*xSquares, 0) #top-right corner
    miscDrawer.setpos(0, 0)#top-left corner again
    miscDrawer.penup()
    miscDrawer.pensize(1)

    # Build grid, which matches coordinates in the virtual grid with turtle coordinates used to display objects
    grid = []
    for y in range(ySquares): #traverse rows
        grid.append([])    
        for x in range(xSquares): #traverse columns
            grid[y].append((gridSquareSideLength//2 + gridSquareSideLength*x, gridSquareSideLength//2 + gridSquareSideLength*y))

    '''for i in range(ySquares): #For debugging
        print(grid[i])'''

    playerOneCaterpillar = Caterpillar(xSquares,ySquares,caterpillarDrawer,miscDrawer, textPrinter, scorePrinter, bonusObjDrawer, grid) #grid as parameter is temporary
    
    # Welcome page
    stampIDlist = []

    # background + title
    miscDrawer.setpos(300, 200) # where the center of the text is
    miscDrawer.shape("welcome-background.gif")
    stampIDlist.append(miscDrawer.stamp())
    
    # Three buttons
    miscDrawer.setpos(360, 185) # below caterpillar white text
    miscDrawer.shape("welcome-button-start.gif")
    stampIDlist.append(miscDrawer.stamp())
    
    miscDrawer.setpos(360, 255) # below caterpillar white text
    miscDrawer.shape("welcome-button-settings.gif")
    stampIDlist.append(miscDrawer.stamp())
    
    miscDrawer.setpos(360, 325) # below caterpillar white text
    miscDrawer.shape("welcome-button-instructions.gif")
    stampIDlist.append(miscDrawer.stamp())

    # Caterpillar graphics (on the left)
    miscDrawer.setpos(70, 179) # upper-left corner
    miscDrawer.shape("welcome-caterpillar-whole.gif")
    stampIDlist.append(miscDrawer.stamp())
    
    # stampIDlist is now [welcome bkgr, start btn, settings btn, instructions btn]

    # NEED caterpillar graphics on the left

    wn.update()
    wn.onkeypress(playerOneCaterpillar.upKeyHandler,"Up")
    wn.onkeypress(playerOneCaterpillar.downKeyHandler,"Down")
    wn.onkeypress(playerOneCaterpillar.leftKeyHandler,"Left")
    wn.onkeypress(playerOneCaterpillar.rightKeyHandler,"Right")
    #Keys w,a,s,d reserved for player two
    #wn.onkeypress(playerOneCaterpillar.upKeyHandler,"w")
    #wn.onkeypress(playerOneCaterpillar.leftKeyHandler,"a")
    #wn.onkeypress(playerOneCaterpillar.downKeyHandler,"s")
    #wn.onkeypress(playerOneCaterpillar.rightKeyHandler,"d")
    #Note: the caterpillar can't "turn" in the direct opposite direction
    #of the last headDirection, ie if initial default headDirection was "left",
    #key presses of "right" will be ignored
    #Also, only the first valid key press per "turn" will be recorded
    wn.onkeypress(pauseGameHandler,"space") #pause button functionality
    
   
    # get mouse coordinates
    canvas = wn.getcanvas() # get turtle canvas
    canvas.bind('<Motion>', mouseMove) # call "mouseMove" function only when the mouse moves (has something to do with tkinter)
    wn.onscreenclick(buttonDetection)
    # x, y = canvas.winfo_pointerxy() # alternative way to get mouse coordinates, but constantly updates

    wn.listen()

    #Main game loop
    previousTime = time.perf_counter()

    # to help the darkening of the button during mouse hover
    hover = [False, False, False] # each index is a button

    # stay at welcome page until some button is clicked    
    while startGame != True:
        wn.update()             
        # (260, 165) to (465, 200)
        # to darken the "Start creeping" button when the mouse hovers over it (x between 260-465, y between 165-200)
        if mouseX >= 260 and mouseX <= 465 and mouseY >= 165 and mouseY <= 205 and hover[0] == False: # if hovers on "Start" button
            miscDrawer.clearstamp(stampIDlist[1]) # delete start button image
            miscDrawer.setpos(360, 185) # below caterpillar white text
            miscDrawer.shape("welcome-button-start-hover.gif")
            stampIDlist[1] = miscDrawer.stamp()
            hover[0] = True # avoid repeating the execution of this code
        if (mouseX >= 260 and mouseX <= 465 and mouseY >= 165 and mouseY <= 205) == False and hover[0] == True: # if the mouse exits the button boundaries
            hover[0] = False
            miscDrawer.clearstamp(stampIDlist[1]) # delete start button image
            miscDrawer.setpos(360, 185) # below caterpillar white text
            miscDrawer.shape("welcome-button-start.gif")
            stampIDlist[1] = miscDrawer.stamp()

        # (260, 230) to (465, 270)
        # "Settings" button         
        if mouseX >= 260 and mouseX <= 465 and mouseY >= 230 and mouseY <= 270 and hover[1] == False: # if hovers on "Settings" button
            miscDrawer.clearstamp(stampIDlist[2]) # delete start button image
            miscDrawer.setpos(360, 255) # below caterpillar white text
            miscDrawer.shape("welcome-button-settings-hover.gif")
            stampIDlist[2] = miscDrawer.stamp()
            hover[1] = True # avoid repeating the execution of this code
        if (mouseX >= 260 and mouseX <= 465 and mouseY >= 230 and mouseY <= 270) == False and hover[1] == True: # if the mouse exits the button boundaries
            hover[1] = False
            miscDrawer.clearstamp(stampIDlist[2]) # delete start button image
            miscDrawer.setpos(360, 255) # below caterpillar white text
            miscDrawer.shape("welcome-button-settings.gif")
            stampIDlist[2] = miscDrawer.stamp()
        
        # (260, 300) to (465, 335)
        # "Instructions" button         
        if mouseX >= 260 and mouseX <= 465 and mouseY >= 300 and mouseY <= 335 and hover[2] == False: # if hovers on "Settings" button
            miscDrawer.clearstamp(stampIDlist[3]) # delete start button image
            miscDrawer.setpos(360, 325) # below caterpillar white text
            miscDrawer.shape("welcome-button-instructions-hover.gif")
            stampIDlist[3] = miscDrawer.stamp()
            hover[2] = True # avoid repeating the execution of this code
        if (mouseX >= 260 and mouseX <= 465 and mouseY >= 300 and mouseY <= 335) == False and hover[2] == True: # if the mouse exits the button boundaries
            hover[2] = False
            miscDrawer.clearstamp(stampIDlist[3]) # delete start button image
            miscDrawer.setpos(360, 325) # below caterpillar white text
            miscDrawer.shape("welcome-button-instructions.gif")
            stampIDlist[3] = miscDrawer.stamp()
        


        #time.sleep(2) # should be: if start game button pressed
            
    
    # clear welcome page
    for image in stampIDlist:
        miscDrawer.clearstamp(image)
    stampIDlist = []
    
    '''
    "welcome-button-instructions.gif",
    "welcome-button-instructions-hover.gif",
    "welcome-button-settings.gif",
    "welcome-button-settings-hover.gif",
    "welcome-button-start.gif",
    "welcome-button-start-hover.gif",
    "gameover-button-menu.gif",
    "gameover-button-menu-hover.gif",
    "gameover-button-retry.gif",
    "gameover-button-retry-hover.gif",
    "gameover-text.gif",
    "gamepaused-3.gif",
    "gamepaused-2.gif",
    "gamepaused-1.gif",
    "gamepaused-text.gif",
    '''
    
    # play sound    (with numpy)
    try:
        import numpy as np
        numpyInstalled = True
        # calculate note frequencies
        A_freq = 440
        Csh_freq = A_freq * 2 ** (4 / 12)
        E_freq = A_freq * 2 ** (7 / 12)
        # get timesteps for each sample, T is note duration in seconds
        sample_rate = 44100
        T = 0.25
        t = np.linspace(0, T, T * sample_rate, False)
        # generate sine wave notes
        A_note = np.sin(A_freq * t * 2 * np.pi)
        Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
        E_note = np.sin(E_freq * t * 2 * np.pi)
        # concatenate notes
        audio = np.hstack((A_note, Csh_note, E_note))
        # normalize to 16-bit range
        audio *= 32767 / np.max(np.abs(audio))
        # convert to 16-bit data
        audio = audio.astype(np.int16)
        # start playback
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        time.sleep(0.8)
    except:
        numpyInstalled = False

    while isDead != True:
        
        currentTime = time.perf_counter()-pauseElapsed # "-pauseElapsed" added to solve pause lag issue
               
        wn.update() # in order to listen to key presses
        while currentTime - previousTime >= loopInterval and pauseGame == False:
            #print(currentTime - previousTime)
            #out1=currentTime - previousTime
            previousTime = currentTime #start countdown from beginning of loop
        
            #print("game loop {0}".format(count))
            gameSpeed += 0.02 # make the caterpillar speed up gradually :)
            loopInterval = 1/gameSpeed
            """ Alternative speeding up method
            if loopsSinceLastSpeedIncrease > 20:
                gameSpeed += 0.2
                loopsSinceLastSpeedIncrease = 0
            """
            
            wn.update() #apparently needed to listen to key presses
            isDead = playerOneCaterpillar.processFrame()
            wn.update()
            loopCount += 1
            loopsSinceLastSpeedIncrease += 1
                   
            #previousTime = currentTime #start countdown from end of loop?

    #Game over code
    miscDrawer.setpos(300, 110)    
    miscDrawer.shape("gameover-text.gif")
    stampIDlist.append(miscDrawer.stamp())
    miscDrawer.write("          ") # puts nothing; must be here for above gameover text to display properly. Weird
    #miscDrawer.write("GAME OVER", True, align="center", font=("Arial", 48, "bold"))

    # Retry and Main Menu buttons
    miscDrawer.setpos(300, 215)
    miscDrawer.shape("gameover-button-retry.gif")
    stampIDlist.append(miscDrawer.stamp())
    miscDrawer.write("          ")
    
    miscDrawer.setpos(300, 290) 
    miscDrawer.shape("gameover-button-menu.gif")
    stampIDlist.append(miscDrawer.stamp())
    miscDrawer.write("          ")
    

    # when you need to clear the gameover message:
    #miscDrawer.clearstamp(stampIDlist[-1])
    print("Your Caterpillar is Dead! :(") # gameover message
    
    # play wah-wah-wahhhh gameover sound
    # 2 options: with simpleaudio (& numpy) OR with winsound
    if numpyInstalled: 
        # calculate note frequencies
        A_freq = 440
        Bb_freq = A_freq * 2 ** (1 / 12) # <-- formula is pretty handy!
        B_freq = A_freq * 2 ** (2 / 12)
        # get timesteps for each sample, T is note duration in seconds
        sample_rate = 44100

        T = 0.5 # 0.5 sec for B and Bb notes
        t = np.linspace(0, T, T * sample_rate, False)
           
        Bb_note = np.sin(Bb_freq * t * 2 * np.pi)# generate sine wave notes     
        B_note = np.sin(B_freq * t * 2 * np.pi)# generate sine wave notes     

        T = 2 # 2 seconds for A note
        t = np.linspace(0, T, T * sample_rate, False)
        A_note = np.sin(A_freq * t * 2 * np.pi)# generate sine wave notes     
        # concatenate notes
        audio = np.hstack((B_note, Bb_note, A_note))
        # normalize to 16-bit range
        audio *= 32767 / np.max(np.abs(audio))
        # convert to 16-bit data
        audio = audio.astype(np.int16)
        # start playback
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

    """
    elif winsoundInstalled:
        # wah-wah-wahhhh sound A-->Ab-->G
        winsound.Beep(440, 700) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
        winsound.Beep(415, 700)
        winsound.Beep(392, 1500)
        '''# alternative wah-wah-wahhhh sound C-->Bb-->B
        winsound.Beep(523, 700) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
        winsound.Beep(494, 700)
        winsound.Beep(466, 1500)'''
    """

    return True #i.e. exitProgram = True


if __name__ == "__main__":
    exitProgram = False
    while (exitProgram != True):
        exitProgram = oneGame()
    time.sleep(2)
    #wn.bye() #Closes turtle window
