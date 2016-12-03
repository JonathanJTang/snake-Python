import turtle

def init():
    wn = turtle.Screen()
    #wn.screensize(?)
    #wn.setworldcoordinates(?)
    snake = turtle.Turtle()
    draw = turtle.Turtle()

    #drawBackground
    wn.bgcolor("white")
    draw.setposition(0,0)