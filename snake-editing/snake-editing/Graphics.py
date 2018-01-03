# Up to date: 1/02/2018

import turtle

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

def initGraphics():
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
    wn.title("Game ???") #Include current score in title?
    wn.colormode(255)

    #Set up the turtle objects
    snakeDrawer = turtle.Turtle() #will draw the snake
    snakeDrawer.speed(0)
    snakeDrawer.penup() #This should be the default state of the turtle
    snakeDrawer.hideturtle() #This should be the default state of the turtle

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

    #drawBackground
    #miscDrawer.setposition(?)

    #Register images used so they can be used in turtle
    wn.register_shape("snake-head-40px-1.gif") # snake head - up - green circle with two eyes - 40 px in diameter
    wn.register_shape("snake-head-40px-2.gif") # snake head - left
    wn.register_shape("snake-head-40px-3.gif") # snake head - down
    wn.register_shape("snake-head-40px-4.gif") # snake head - right
    wn.register_shape("snake-body-40px.gif") # snake body - plain green circle

    ### For testing purposes (temporary) ###
    snakeDrawer.shape("snake-body-40px.gif")
    snakeDrawer.fillcolor(255,255,255)
    snakeDrawer.turtlesize(2,2)
    #miscDrawer.shape("Maple_small.gif")
    ### temp ###

    #draw walls
    miscDrawer.pensize(3)
    miscDrawer.setpos(0, 0)#top-left corner again
    miscDrawer.pendown()
    miscDrawer.setpos(0, gridSquareSideLength*ySquares) #bottom-left corner
    miscDrawer.setpos(gridSquareSideLength*xSquares, gridSquareSideLength*ySquares) #bottom-right corner
    miscDrawer.setpos(gridSquareSideLength*xSquares, 0) #top-right corner
    miscDrawer.setpos(0, 0)#top-left corner again
    miscDrawer.penup()
    miscDrawer.pensize(1)

    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen after drawing with turtle

    return wn, snakeDrawer, miscDrawer, textPrinter, scorePrinter # returns window & two turtles

# runs initGraphics() and creates global variables wn, snakeDrawer, and miscDrawer
wn, snakeDrawer, miscDrawer, textPrinter, scorePrinter = initGraphics()


# Build grid, which matches coordinates in the virtual grid with turtle coordinates used to display objects
grid = []
for y in range(ySquares): #traverse rows
    grid.append([])    
    for x in range(xSquares): #traverse columns
        grid[y].append((gridSquareSideLength//2 + gridSquareSideLength*x, gridSquareSideLength//2 + gridSquareSideLength*y))

for i in range(ySquares): #For debugging
    print(grid[i])


'''
### Jonathan's Testing
from ClassSnake import *
playerOneSnake = Snake(xSquares,ySquares,snakeDrawer,miscDrawer, scorePrinter, grid) #grid as parameter is temporary
wn.update()
isDead = False
lastHeadDirection = "left"
import random
import time
rng = random.Random()
d = {1: "left",2:"right",3:"up",4:"down"}

def opp(headDirection):
    if headDirection == "left":
        return "right"
    elif headDirection == "right":
        return "left"
    elif headDirection == "up":
        return "down"
    elif headDirection == "down":
        return "up"

while isDead != True:  
    while True:
        newHeadDirection = d[rng.randint(1,4)]
        if newHeadDirection != opp(lastHeadDirection):
            break;
    isDead = playerOneSnake.processFrame(newHeadDirection)
    wn.update()
    lastHeadDirection = newHeadDirection
    time.sleep(1)

#GAMEOVER message
miscDrawer.setpos(300, 200) # where the center of the text is
miscDrawer.write("GAME OVER", True, align="center", font=("Arial", 48, "bold"))
print("Your Snake is Dead! :(") # gameover message
### ###
'''

#wn.mainloop() #We need to figure out where this line should go in the overall project
