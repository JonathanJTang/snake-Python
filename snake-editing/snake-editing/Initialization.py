import turtle


def init():
    ''' All the initialization of this game. Run only once.
    '''
    screenWidth = 500
    screenHeight = 500
    
    wn = turtle.Screen()
    wn.screensize(screenWidth,screenHeight,bg="white")
    wn.setworldcoordinates(0, 0, screenWidth, screenHeight)
    snake = turtle.Turtle() #draws the snake
    misc = turtle.Turtle() #draws miscellaneous stuff: borders, scores, etc

    #drawBackground

    #misc.setposition(?)


    return wn, snake, misc

init()


#wn.mainloop()
