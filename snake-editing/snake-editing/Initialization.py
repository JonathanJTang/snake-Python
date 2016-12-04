import turtle


def init():
    screenWidth = 500
    screenHeight = 500
    
    global wn
    wn = turtle.Screen()
    #wn.screensize(?)
    #wn.setworldcoordinates(?)
    global snake
    snake = turtle.Turtle() #draws the snake
    global misc
    misc = turtle.Turtle() #draws miscellaneous stuff: borders, scores, etc

    #drawBackground
    wn.bgcolor("white")
    #misc.setposition(?)
    return wn, snake, misc

init()
wn.mainloop()
