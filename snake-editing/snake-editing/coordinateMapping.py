# Copied from Graphics 12/5/2016 2:07PM

import turtle

# variables defined in other functions
screenWidth = 500
screenHeight = 500
xSquares = 10 # number of horizontal virtual squares
ySquares = 10 # number of vertical virtual squares
squareWidth = screenWidth/xSquares
squareHeight = screenHeight/ySquares
# Make space in the grid list
grid = [] # contains the actual coordinates of each square


def init():
    ''' All the initialization of this game. Run only once.
    '''
    
    
    global wn
    global snake
    global misc
    wn = turtle.Screen()
    #wn.screensize(screenWidth,screenHeight,bg="white")
    wn.setup(screenWidth, screenHeight)
    wn.setworldcoordinates(0, 0, screenWidth, screenHeight)
    snake = turtle.Turtle() #draws the snake
    misc = turtle.Turtle() #draws miscellaneous stuff: borders, scores, etc
    
    
    #drawBackground
    #misc.setposition(?)

    #return wn, snake, misc


init()

snake.penup()
snake.speed(0)
wn.register_shape("C:\Joseph\Maple_small.gif")
snake.shape("C:\Joseph\Maple_small.gif")
# set coordinates
for x in range(xSquares):
    grid.append([])    
    for y in range(ySquares):
        grid[x].append((squareWidth*x,squareHeight*y))
        snake.setposition(grid[x][y])
        snake.stamp()
print(grid)