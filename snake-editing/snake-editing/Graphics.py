# Up to date: 1/02/2018

import turtle

# variables defined in other functions
#Variables potentially set by user
xSquares = 15 #number of virtual squares in a row
ySquares = 10 #number of virtual squares in a column
gridSquareSideLength = 40 #in pixels; must be an integer

#Things done by the program
if not (xSquares >= 3 and ySquares >= 3):
    raise ValueError("xSquares and ySquares must both be greater than 3")

screenWidth = xSquares * gridSquareSideLength #integer, in pixels
screenHeight = ySquares * gridSquareSideLength #integer, in pixels

def initGraphics():
    '''Initializes graphics for the game. Run only once.
        '''
    #Set up the screen object
    wn = turtle.Screen()
    wn.setup(screenWidth, screenHeight)
    #Bottom left corner (0,screenHeight), top right corner (screenWidth,0)
    #to make javascript-like coordinate system with (0,0) in the top left corner
    wn.setworldcoordinates(0, screenHeight, screenWidth, 0)
    #"""temporarily commented for easier debugging"""
    wn.tracer(0, delay=1) #Turn turtle animation off (only each 0th screen update is performed)
    wn.title("Game ???") #Include current score in title?
    wn.colormode(255)

    #Set up the turtle objects
    caterpillarDrawer = turtle.Turtle() #will draw the caterpillar
    caterpillarDrawer.speed(0)
    caterpillarDrawer.penup() #This should be the default state of the turtle
    caterpillarDrawer.hideturtle() #This should be the default state of the turtle

    miscDrawer = turtle.Turtle() #will draw miscellaneous stuff: borders, scores, etc
    miscDrawer.speed(0)
    miscDrawer.penup() #This should be the default state of the turtle
    miscDrawer.hideturtle() #This should be the default state of the turtle
    
    textPrinter = turtle.Turtle() # will print text on screen when needed
    textPrinter.speed(0)
    textPrinter.penup() #This should be the default state of the turtle
    textPrinter.hideturtle() #This should be the default state of the turtle

    scorePrinter = turtle.Turtle() # will print the score on the screen
    scorePrinter.speed(0)
    scorePrinter.penup() #This should be the default state of the turtle
    scorePrinter.hideturtle() #This should be the default state of the turtle

    bonusObjDrawer = turtle.Turtle() # will draw bonus object on the screen
    bonusObjDrawer.speed(0)
    bonusObjDrawer.penup() #This should be the default state of the turtle
    bonusObjDrawer.hideturtle() #This should be the default state of the turtle

    #drawBackground
    #miscDrawer.setposition(?)

    #Register images used so they can be used in turtle
    wn.register_shape("snake-head-40px-1.gif") # caterpillar head - up - green circle with two eyes - 40 px in diameter
    wn.register_shape("snake-head-40px-2.gif") # caterpillar head - left
    wn.register_shape("snake-head-40px-3.gif") # caterpillar head - down
    wn.register_shape("snake-head-40px-4.gif") # caterpillar head - right
    wn.register_shape("snake-body-40px.gif") # caterpillar body - plain green circle
    wn.register_shape("leaf-green-40px.gif") # Bonus object - green leaf (from Khan Academy)
    wn.register_shape("apple-40px.gif") # Bonus object - apple (good cuz it has transparent background)
    wn.register_shape("apple-2-40px.gif") # Bonus object - alternative apple (not good cuz it has white background)
    

    ### For testing purposes (temporary) ###
    caterpillarDrawer.shape("snake-body-40px.gif")
    caterpillarDrawer.fillcolor(255,255,255)
    ### temp ###

    #Draw boundaries of game board
    miscDrawer.pensize(3)
    miscDrawer.setpos(0, 0)#top-left corner again
    miscDrawer.pendown()
    miscDrawer.setpos(0, gridSquareSideLength*ySquares) #bottom-left corner
    miscDrawer.setpos(gridSquareSideLength*xSquares, gridSquareSideLength*ySquares) #bottom-right corner
    miscDrawer.setpos(gridSquareSideLength*xSquares, 0) #top-right corner
    miscDrawer.setpos(0, 0)#top-left corner again
    miscDrawer.penup()
    miscDrawer.pensize(1)

    """Note to Joseph: see below. Pls delete this comment when you've seen this"""
    wn.update() #Use this method to display the updated screen after drawing with turtle

    return wn, caterpillarDrawer, miscDrawer, textPrinter, scorePrinter, bonusObjDrawer # returns window & two turtles

"""We need to figure out where the line below should go in the overall project"""
#wn.mainloop()
