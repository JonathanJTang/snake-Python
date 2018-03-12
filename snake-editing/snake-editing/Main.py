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
mouseX = 0 # instantaneous mouse x-coordinate
mouseY = 0 # instantaneous mouse y-coordinate
mouseMoved = False
mouseClicked = False
nextState = "welcome page"

def mouseClickedHandler(x, y):
    print("Mouse clicked: {0}, {1}".format(x,y))
    global mouseClicked
    mouseClicked = True

def mouseMovedHandler(mousePosition):
    '''Only called when the mouse is moved'''
    global mouseX # had to use global variables
    global mouseY
    global mouseMoved
    # Get mouse coordinates
    '''Note: coordinates in tkinter.Event object mousePosition are
        independent of the coordinate system set by wn.setworldcoordinates().
        mousePosition's (0,0) is the top left corner of the window, so an
        adjustment factor is used to make (0,0) the top left corner of the canvas'''
    mouseX = mousePosition.x - 4
    mouseY = mousePosition.y - 4
    print("{0}, {1}".format(mouseX, mouseY)) # for debugging
    mouseMoved = True


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
    '''Initializes graphics for the game. Run only once.'''

    #Set up the screen object
    wn = turtle.Screen()
    wn.setup(screenWidth+20, screenHeight+20)  #Window dimensions, in pixels
    wn.screensize(screenWidth,screenHeight)  #Canvas dimensions, in pixels
    #Bottom left corner (0,screenHeight), top right corner (screenWidth,0)
    #to make javascript-like coordinate system with (0,0) in the top left corner

    wn.setworldcoordinates(0, screenHeight, screenWidth, 0)
    '''###################################################
                    NOTE TO JOSEPH:
       The follow line is a temporary hack; any better way to do it???
       ####################################################'''
    wn.setup(screenWidth+10,screenHeight+10)  #Resize window to make (0,0) of canvas closer to top left of window
    
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
    for imageName in shapes:
        wn.register_shape(imageName)

    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen after drawing with turtle

    return wn, caterpillarDrawer, miscDrawer, textPrinter, scorePrinter, bonusObjDrawer # returns screen & turtles

def stateController(wn, **keywordParameters):
    """Whenever state is changed, use 'return' to exit the function and have an outside loop call the function again """
    global nextState
    if nextState == "welcome page":
        global mouseMoved, mouseClicked
        startGame = False
        stampIDList = []  #will eventually be [welcome background, caterpillar graphics]
        if "miscDrawer" not in keywordParameters:
            raise NameError("required parameter 'miscDrawer' was not given")
        miscDrawer = keywordParameters["miscDrawer"]

        # Background + title
        miscDrawer.setpos(300, 200) # where the center of the text is
        miscDrawer.shape("welcome-background.gif")
        stampIDList.append(miscDrawer.stamp())

        # Caterpillar graphics (on the left)
        miscDrawer.setpos(70, 179) # close to the upper-left corner
        miscDrawer.shape("welcome-caterpillar-whole.gif")
        stampIDList.append(miscDrawer.stamp())

        # Three buttons
        welcomePageButtons = [
        Button(250,166,460,204,"welcome-button-start.gif","welcome-button-start-hover.gif"),
        Button(250,236,460,274,"welcome-button-settings.gif","welcome-button-settings-hover.gif"),
        Button(250,306,460,344,"welcome-button-instructions.gif","welcome-button-instructions-hover.gif")
        ]

        for button in welcomePageButtons:
            button.enable(miscDrawer)

        wn.update()

        # stay at welcome page until some button is clicked    
        while startGame == False: 
            #To avoid too much resource usage in checking the buttons;
            #Could rewrite this to be a time.perf_counter() subtraction loop
            #ORR...it might not be needed with the global mouseMoved variable
            time.sleep(0.02)
            wn.update()  # statement needed in order to listen to key presses

            if mouseMoved:
                for button in welcomePageButtons:
                    if(button.hover == False and button.mouseCoordsOnButton(mouseX,mouseY)):
                        button.changeToHover(miscDrawer)
                    elif(button.hover == True and not button.mouseCoordsOnButton(mouseX,mouseY)):
                        button.changeToOrig(miscDrawer)
                wn.update()
                mouseMoved = False

            if mouseClicked:
                """There might be a better way to do this"""
                if welcomePageButtons[0].mouseCoordsOnButton(mouseX,mouseY):
                    # 'Start' button clicked
                    startGame = True
                elif welcomePageButtons[1].mouseCoordsOnButton(mouseX,mouseY):
                    # 'Settings' button clicked
                    pass
                elif welcomePageButtons[2].mouseCoordsOnButton(mouseX,mouseY):
                    # 'Instructions' button clicked
                    pass
                mouseClicked = False
                  
        # clear welcome page
        for image in stampIDList:
            miscDrawer.clearstamp(image)
        for button in welcomePageButtons:
            button.disable(miscDrawer)
        stampIDList.clear()
        wn.update()
      
        # play sound (with numpy)
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


        nextState = "main game"
        return False #ie nextGame = False

    elif nextState == "main game":
        #Initialize variables
        isDead = False
        loopCount = 0
        loopsSinceLastSpeedIncrease = 0
        gameSpeed = 1
        loopInterval = 1/gameSpeed #Maybe too fast as the initial speed?

        if "playerOneCaterpillar" not in keywordParameters:
            raise NameError("required parameter 'playerOneCaterpillar' was not given")
        playerOneCaterpillar = keywordParameters["playerOneCaterpillar"]

        #Main game loop
        playerOneCaterpillar.beginGame()
        previousTime = time.perf_counter()

        while(isDead != True):
        
            currentTime = time.perf_counter()-pauseElapsed # "-pauseElapsed" added to solve pause lag issue
               
            wn.update() # statement needed in order to listen to key presses
            while (currentTime - previousTime) >= loopInterval and pauseGame == False:
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
            
                wn.update() #statement apparently needed to listen to key presses
                isDead = playerOneCaterpillar.processFrame()
                wn.update()
                loopCount += 1
                loopsSinceLastSpeedIncrease += 1
                   
                #previousTime = currentTime #start countdown from end of loop?

        nextState = "game over page"
        return False  #ie exitGame = False

    elif nextState == "game over page":
        #Game over code
        exitLoop = False
        stampIDList = []
        if "miscDrawer" not in keywordParameters:
            raise NameError("required parameter 'miscDrawer' was not given")
        miscDrawer = keywordParameters["miscDrawer"]

        miscDrawer.setpos(300, 110)    
        miscDrawer.shape("gameover-text.gif")
        stampIDList.append(miscDrawer.stamp())

        # Retry and Main Menu buttons
        gameoverPageButtons = [
        Button(195,196,405,234,"gameover-button-retry.gif","gameover-button-retry-hover.gif"),
        Button(195,271,405,309,"gameover-button-menu.gif","gameover-button-menu-hover.gif")
        ]

        for button in gameoverPageButtons:
            button.enable(miscDrawer)

        wn.update()
    
        print("Your Caterpillar is Dead! :(") # gameover message
    
        # play wah-wah-wahhhh gameover sound
        # 2 options: with simpleaudio (& numpy) OR with winsound
        
        #temporary
        import numpy as np
        numpyInstalled = True

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

        # stay at gameover page until some button is clicked    
        while exitLoop == False: 
            #To avoid too much resource usage in checking the buttons;
            #Could rewrite this to be a time.perf_counter() subtraction loop
            #ORR...it might not be needed with the global mouseMoved variable
            time.sleep(0.02)
            wn.update()  # statement needed in order to listen to key presses

            if mouseMoved:
                for button in gameoverPageButtons:
                    if(button.hover == False and button.mouseCoordsOnButton(mouseX,mouseY)):
                        button.changeToHover(miscDrawer)
                    elif(button.hover == True and not button.mouseCoordsOnButton(mouseX,mouseY)):
                        button.changeToOrig(miscDrawer)
                wn.update()
                mouseMoved = False

            if mouseClicked:
                """There might be a better way to do this"""
                if gameoverPageButtons[0].mouseCoordsOnButton(mouseX,mouseY):
                    # 'Retry' button clicked
                    pass
                elif gameoverPageButtons[1].mouseCoordsOnButton(mouseX,mouseY):
                    # 'Menu' button clicked
                    exitLoop = True
                mouseClicked = False
        
        #Clearing the gameover screen
        for stamp in stampIDList:
            miscDrawer.clearstamp(stamp)
        wn.update()

        return True  #to exit the loop

def oneGame():

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

    # Build grid, which matches coordinates in the virtual grid with turtle coordinates used to display objects
    grid = []
    for y in range(ySquares): #traverse rows
        grid.append([])    
        for x in range(xSquares): #traverse columns
            grid[y].append((gridSquareSideLength//2 + gridSquareSideLength*x, gridSquareSideLength//2 + gridSquareSideLength*y))

    '''for i in range(ySquares): #For debugging
        print(grid[i])'''

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

    playerOneCaterpillar = Caterpillar(xSquares,ySquares,caterpillarDrawer,miscDrawer, textPrinter, scorePrinter, bonusObjDrawer, grid) #grid as parameter is temporary
    
    # Monitor for key presses
    wn.onkeypress(playerOneCaterpillar.upKeyHandler,"Up")
    wn.onkeypress(playerOneCaterpillar.downKeyHandler,"Down")
    wn.onkeypress(playerOneCaterpillar.leftKeyHandler,"Left")
    wn.onkeypress(playerOneCaterpillar.rightKeyHandler,"Right")
    #Keys w,a,s,d reserved for player two
    #wn.onkeypress(playerTwoCaterpillar.upKeyHandler,"w")
    #wn.onkeypress(playerTwoCaterpillar.leftKeyHandler,"a")
    #wn.onkeypress(playerTwoCaterpillar.downKeyHandler,"s")
    #wn.onkeypress(playerTwoCaterpillar.rightKeyHandler,"d")
    wn.onkeypress(pauseGameHandler,"space") #pause button functionality

    # Monitor for mouse coordinates
    canvas = wn.getcanvas() # get the Tkinter canvas of the turtle Screen object
    canvas.bind('<Motion>', mouseMovedHandler)
    '''Whenever the mouse is moved inside the turtle window, a tkinter.Event
       object will be passed to mouseMovedHandler() that contains the (x,y) coordinates
       of the mouse. These coordinates are independent of wn.setworldcoordinates():
       they seem to always have the top left corner of the window as (0,0)'''
    wn.onscreenclick(mouseClickedHandler)
    # x, y = canvas.winfo_pointerxy() # alternative way to get mouse coordinates, but constantly updates

    wn.listen()

    exitGame = False
    ### Main section ###
    while(exitGame == False):
        exitGame = stateController(wn, miscDrawer=miscDrawer, playerOneCaterpillar=playerOneCaterpillar)

    wn.mainloop()
    return True #i.e. exitProgram = True


if __name__ == "__main__":
    exitProgram = False
    while (exitProgram != True):
        exitProgram = oneGame()
    time.sleep(2)
    #wn.bye() #Closes turtle window
