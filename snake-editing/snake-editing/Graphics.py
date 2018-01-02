# Up to date: 1/02/2018

import turtle

# variables defined in other functions
#Variables potentially set by user
screenWidth = 600 #integer, in pixels
screenHeight = 400 #integer, in pixels
gridSquareSideLength = 40 #must be an integer that is a factor of both screenWidth and screenHeight

#Things done by the program
if screenHeight % gridSquareSideLength != 0 or screenWidth % gridSquareSideLength != 0:
    raise ValueError("gridSquareSideLength must divide both screenHeight and screenWidth")
xSquares = screenHeight//gridSquareSideLength #number of virtual squares in a row
ySquares = screenWidth//gridSquareSideLength #number of virtual squares in a column

if not (xSquares >= 3 and ySquares >= 3):
    raise ValueError


def initGraphics():
    '''Initializes graphics for the game. Run only once.
        '''
    #Set up the screen object
    wn = turtle.Screen()
    wn.setup(screenWidth, screenHeight)
    #Bottom left corner (0,screenHeight), top right corner (screenWidth,0)
    #to make javascript-like coordinate system with (0,0) in the top left corner
    wn.setworldcoordinates(0, screenHeight, screenWidth, 0)
    """temporarily commented for easier debugging"""
    #wn.tracer(0, delay=1) #Turn turtle animation off (only each 0th screen update is performed)
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
    
    #drawBackground
    #miscDrawer.setposition(?)

    #Register images used so they can be used in turtle
    wn.register_shape("snake-head-40px.gif") # snake head - green circle with two eyes - 40 px in diameter
    wn.register_shape("snake-body-40px.gif") # snake body - plain green circle

    ### For testing purposes (temporary) ###
    snakeDrawer.shape("snake-body-40px.gif")
    snakeDrawer.fillcolor(255,255,255)
    snakeDrawer.turtlesize(2,2)
    #miscDrawer.shape("Maple_small.gif")
    ### temp ###

    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen after drawing with turtle

    return wn, snakeDrawer, miscDrawer # returns window & two turtles

# runs initGraphics() and creates global variables wn, snakeDrawer, and miscDrawer
wn, snakeDrawer, miscDrawer = initGraphics()



# Make space in the grid list
grid = [] # contains the coordinates of each square used in turtle to display objects
# set coordinates
for y in range(ySquares):
    grid.append([])    
    for x in range(xSquares):
        grid[y].append((gridSquareSideLength*x,gridSquareSideLength*y))
        #snakeDrawer.setposition(grid[x][y])
        #snakeDrawer.stamp()
for i in range(xSquares): #For debugging
    print(grid[i])

#Needs testing, but below is code for the initial postion of the snake (center of screen)
#snakePos = [grid[len(grid)//2 +1][len(grid[0])//2],grid[len(grid)//2][len(grid[0])//2],grid[len(grid)//2 -1][len(grid[0])//2]]


### Jonathan's Testing
from ClassSnake import *
playerOneSnake = Snake(xSquares,ySquares,snakeDrawer,miscDrawer,grid) #grid as parameter is temporary
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
    #Note for key press listening function: headDirection can't be the direct opposite
    #of the last headDirection, eg if initial default headDirection was "left",
    #key presses of "right" will be ignored
    #Also, only the "first" key press per "turn" will be recorded?
    
    while True:
        currentHeadDirection = d[rng.randint(1,4)]
        if currentHeadDirection != opp(lastHeadDirection):
            break;
    isDead = playerOneSnake.processFrame(currentHeadDirection)
    wn.update()
    lastHeadDirection = currentHeadDirection
    time.sleep(1)
print("Your Snake is Dead! :(") # gameover message
### ###

'''
snakeDrawer.color("green")
snakeDrawer.pensize(4)
wn.register_shape("C:\Joseph\Maple_small.gif")
snakeDrawer.shape("C:\Joseph\Maple_small.gif")
for i in range(2):
    snakeDrawer.forward(screenWidth-20)
    snakeDrawer.left(90)
    snakeDrawer.forward(screenHeight-20)
    snakeDrawer.left(90)
'''

wn.mainloop() #We need to figure out where this line should go in the overall project
