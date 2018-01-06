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
'''
firstTime = True
'''
def pauseGameHandler():
    """Called whenever the key for pause game is pressed"""
    print("space key pressed") #For debugging
    global pauseGame
    global pauseElapsed # stores the total time paused (accumulates with every pause)
    '''global firstTime # not the best way, but it makes pauseTimerStart start only once - at the start of the pause
    '''
    if pauseGame == True:
        #unPauseGameGraphics
        textPrinter.undo() #Remove "game paused" message
        textPrinter.setpos(300, 200) # where the center of the text is
        
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
            textPrinter.write("{0}".format(num), True, align="center", font=("Arial", 48, "normal"))
            time.sleep(1)
            textPrinter.undo()  
        # resumes game (after the "3, 2, 1")
        pauseGame = False
        # adds pause time interval to be subtracted from the current time
        pauseElapsed += time.perf_counter()-pauseTimeStart
        '''# allow program to start pauseTimer again for the next time the game is paused
        firstTime = True'''
                    
     
    else:
        pauseGame = True # pauses game
        #pauseGameGraphics
        textPrinter.setpos(300, 200) # where the center of the text is
        textPrinter.write("GAME PAUSED", True, align="center", font=("Arial", 48, "normal"))


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
    wn.register_shape("apple-40px.gif") # Bonus object - apple (good cuz it has transparent background)
    wn.register_shape("apple-2-40px.gif") # Bonus object - alternative apple (not good cuz it has white background)


    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen after drawing with turtle

    return wn, caterpillarDrawer, miscDrawer, textPrinter, scorePrinter, bonusObjDrawer # returns screen & turtles


def oneGame():
    #Initialize variables
    isDead = False
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
    wn.listen()

    #Main game loop
    previousTime = time.perf_counter()

    # variable to delete paused time from currentTime
    pauseElapsed = 0   

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
    miscDrawer.setpos(300, 200) # where the center of the text is
    miscDrawer.write("GAME OVER", True, align="center", font=("Arial", 48, "bold"))
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

    elif winsoundInstalled:
        # wah-wah-wahhhh sound A-->Ab-->G
        winsound.Beep(440, 700) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
        winsound.Beep(415, 700)
        winsound.Beep(392, 1500)
        '''# alternative wah-wah-wahhhh sound C-->Bb-->B
        winsound.Beep(523, 700) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
        winsound.Beep(494, 700)
        winsound.Beep(466, 1500)'''

    return True #i.e. exitProgram = True


if __name__ == "__main__":
    exitProgram = False
    while (exitProgram != True):
        exitProgram = oneGame()
    time.sleep(2)
    #wn.bye() #Closes turtle window
