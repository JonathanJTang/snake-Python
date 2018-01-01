# Up to date: 1/02/2018

import turtle

# variables defined in other functions
#Variables potentially set by user
screenWidth = 500 #integer, in pixels
screenHeight = 500 #integer, in pixels
xSquares = 10 #integer, number of horizontal virtual squares (determines the size of the board)
ySquares = 10 #integer, number of vertical virtual squares (determines the size of the board)

#Things done by the program
squareWidth = screenWidth/xSquares
squareHeight = screenHeight/ySquares
# Make space in the grid list
grid = [] # contains the actual coordinates of each square


def initGraphics():
    '''Initializes graphics for the game. Run only once.
        '''
    #Set up the screen object
    wn = turtle.Screen()
    wn.setup(screenWidth, screenHeight)
    #Bottom left corner (0,screenHeight), top right corner (screenWidth,0)
    #to make javascript-like coordinate system with (0,0) in the top left corner
    wn.setworldcoordinates(0, screenHeight, screenWidth, 0)
    wn.tracer(0, delay=1) #Turn turtle animation off (only each 0th screen update is performed)
    wn.title("Game ???") #Include current score in title?

    #Set up the turtle objects
    snake = turtle.Turtle() #will draw the snake
    snake.speed(0)
    snake.penup() #This should be the default state of the turtle

    misc = turtle.Turtle() #will draw miscellaneous stuff: borders, scores, etc
    misc.speed(0)
    misc.penup() #This should be the default state of the turtle
    
    #drawBackground
    #misc.setposition(?)

    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen

    return wn, snake, misc # returns window & two turtles

# runs initGraphics() and creates global variables wn, snake, and misc
wn, snake, misc = initGraphics() 


#wn.register_shape("C:\Joseph\Maple_small.gif")
#snake.shape("C:\Joseph\Maple_small.gif")
wn.register_shape("Maple_small.gif")
snake.shape("Maple_small.gif")

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
