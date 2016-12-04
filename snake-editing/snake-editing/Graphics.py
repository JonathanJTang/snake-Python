# Copied from Initialization 12/4/2016 9:12PM

import turtle


def init():
    ''' All the initialization of this game. Run only once.
    '''
    screenWidth = 500
    screenHeight = 500
    
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
wn.register_shape("C:\Maple.gif")
snake.shape("C:\Maple.gif")
for i in range(4):
    snake.forward(500)
    snake.left(90)

wn.mainloop()