# Copied from Initialization 12/4/2016 9:12PM

import turtle

# variables defined in other functions
screenWidth = 400
screenHeight = 500

def init():
    ''' All the initialization of this game. Run only once.
    '''
    
    
    global wn
    global snake
    global misc
    wn = turtle.Screen()
    wn.screensize(screenWidth,screenHeight,bg="white")
    wn.setworldcoordinates(0, 0, screenWidth, screenHeight)
    snake = turtle.Turtle() #draws the snake
    misc = turtle.Turtle() #draws miscellaneous stuff: borders, scores, etc

    #drawBackground

    #misc.setposition(?)


    #return wn, snake, misc

init()

snake.color("green")
snake.pensize(4)
wn.register_shape("C:\Joseph\Maple_small.gif")
snake.shape("C:\Joseph\Maple_small.gif")
for i in range(2):
    snake.forward(screenWidth-20)
    snake.left(90)
    snake.forward(screenHeight-20)
    snake.left(90)

wn.mainloop()