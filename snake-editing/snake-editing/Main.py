'''
Project Name:
Authors: Jonathan Tang & Joseph Tang
Created on:

Edited 
'''
import turtle
import time
from ClassSnake import *

pauseGame = False
def pauseGameHandler():
    """Called whenever the key for pause game is pressed"""
    print("space key pressed") #For debugging
    global pauseGame
    global textPrinter
    if pauseGame == True:
        pauseGame = False
        #unPauseGameGraphics
        textPrinter.undo() #Remove "game paused" message
        textPrinter.setpos(300, 200) # where the center of the text is
        for num in range(3,0,-1):
            textPrinter.write("{0}".format(num), True, align="center", font=("Arial", 48, "bold"))
            time.sleep(1)
            textPrinter.undo()
        
    else:
        pauseGame = True
        #pauseGameGraphics
        textPrinter.setpos(300, 200) # where the center of the text is
        textPrinter.write("GAME PAUSED", True, align="center", font=("Arial", 48, "bold"))

if __name__ == "__main__":
    #Initialize variables
    isDead = False
    count = 0
    gameSpeed = 1
    loopInterval = 1/gameSpeed #Maybe too fast?

    """Copied from Graphics.py 1/03/2018"""
    # variables defined in other functions
    #Variables potentially set by user
    xSquares = 15 #number of virtual squares in a row
    ySquares = 10 #number of virtual squares in a column
    gridSquareSideLength = 40 #in pixels; must be an integer

    #Things done by the program
    if not (xSquares >= 3 and ySquares >= 3):
        raise ValueError("xSquares and ySquares must both be greater than 3")

    screenWidth = xSquares * gridSquareSideLength #integer, in pixels
    screenHeight = ySquares * gridSquareSideLength #integer, in pixels

    # Build grid, which matches coordinates in the virtual grid with turtle coordinates used to display objects
    grid = []
    for y in range(ySquares): #traverse rows
        grid.append([])    
        for x in range(xSquares): #traverse columns
            grid[y].append((gridSquareSideLength//2 + gridSquareSideLength*x, gridSquareSideLength//2 + gridSquareSideLength*y))

    for i in range(ySquares): #For debugging
        print(grid[i])

    from Graphics import initGraphics
    wn, snakeDrawer, miscDrawer, textPrinter, scorePrinter = initGraphics()
    """Copied from Graphics.py 1/03/2018"""

    playerOneSnake = Snake(xSquares,ySquares,snakeDrawer,miscDrawer, scorePrinter, grid) #grid as parameter is temporary
    wn.update()
    wn.onkeypress(playerOneSnake.upKeyHandler,"Up")
    wn.onkeypress(playerOneSnake.downKeyHandler,"Down")
    wn.onkeypress(playerOneSnake.leftKeyHandler,"Left")
    wn.onkeypress(playerOneSnake.rightKeyHandler,"Right")
    #Note: the snake can't "turn" in the direct opposite direction
    #of the last headDirection, ie if initial default headDirection was "left",
    #key presses of "right" will be ignored
    #Also, only the "first" key press per "turn" will be recorded
    wn.onkeypress(pauseGameHandler,"space") #pause button functionality
    wn.listen()

    #Main game loop
    previousTime = time.perf_counter()
    while(isDead != True):
        currentTime = time.perf_counter()
        wn.update() #apparently needed to listen to key presses
        while(currentTime - previousTime >= loopInterval and pauseGame == False):
            #print(currentTime - previousTime)
            #out1=currentTime - previousTime
            previousTime = currentTime #start countdown from beginning of loop
        
            print("game loop {0}".format(count))
            wn.update() #apparently needed to listen to key presses
            isDead = playerOneSnake.processFrame()
            wn.update()
            count += 1
                   
            #previousTime = currentTime #start countdown from end of loop?

    #Game over code
    miscDrawer.setpos(300, 200) # where the center of the text is
    miscDrawer.write("GAME OVER", True, align="center", font=("Arial", 48, "bold"))
    print("Your Snake is Dead! :(") # gameover message
    wn.mainloop() #Put this line here???
