import turtle

def init():
    screenWidth = 500
    screenHeight = 500
    
    wn = turtle.Screen()
    #wn.screensize(?)
    #wn.setworldcoordinates(?)
    snake = turtle.Turtle() #draws the snake
    misc = turtle.Turtle() #draws miscellaneous stuff: borders, scores, etc

    #drawBackground
    wn.bgcolor("white")
    #misc.setposition(?)
