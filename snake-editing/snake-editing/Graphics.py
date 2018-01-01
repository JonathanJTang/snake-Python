# Copied from Initialization 12/4/2016 9:12PM

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
        Note: currently all graphics. Rename function if it stays this way?'''
    
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

#Needs testing, but below is code for the initial postion of the snake (center of screen)
#snakePos = [grid[len(grid)//2 +1][len(grid[0])//2],grid[len(grid)//2][len(grid[0])//2],grid[len(grid)//2 -1][len(grid[0])//2]]


'''
snake.color("green")
snake.pensize(4)
wn.register_shape("C:\Joseph\Maple_small.gif")
snake.shape("C:\Joseph\Maple_small.gif")
for i in range(2):
    snake.forward(screenWidth-20)
    snake.left(90)
    snake.forward(screenHeight-20)
    snake.left(90)
'''

wn.mainloop() #We need to figure out where this line should go in the overall project
