# Copied from Graphics.py, 1/02/2018

import turtle
import random
import winsound
class BonusObj:
    """Class for Bonus objects that affect a snake's
        properLength, points, etc."""
    
    
    '''ISSUE:  Add a class attribute that describes all the parameters for a BonusObj type?'''

    def __init__(self,turtleObj,bonusTypeStr,gridX, gridY,lifetime,pointsValue,snakeLengthChange, gridList):
        """Initializes variables for a BonusObj instance. See comments
            in method for explanation of parameters"""
        #Make pointsValue linked to bonusTypeStr?
        turtleShape = {"apple":"apple-40px.gif",
                       "apple2":"apple-2-40px.gif",
                   "leaf":"leaf-green-40px.gif"}
        self.turtleObj = turtleObj
        self.positionTuple = (gridX, gridY) #The BonusObj's position in the virtual grid ALTHOUGH not used in drawing the object
        self.turtleObj.shape(turtleShape[bonusTypeStr])
        self.turtleObj.setpos(gridList[gridY][gridX]) #Assumes turtleObj already has penup() and speed 0
        self.stampID = self.turtleObj.stamp() #screen.update() will be done elsewhere
        self.pointsValue = pointsValue #The number of points the player will get; could be negative
        self.snakeLengthChange = snakeLengthChange
        self.earned = False #If the player has earned the BonusObj
        self.lifetime = lifetime #The number of game loops the object will exist

    def update(self,snakeHeadPositionTuple,snakeCurrentScore):
        """This method should be called once per game loop.
            Since BonusObj's never spawn on spaces occupied by a snake,
            only need to check the snake head's position each loop"""
        self.lifetime -= 1
        if snakeHeadPositionTuple == self.positionTuple:
            self.earned = True
            # makes a high-pitched beep when the snake gets the object
            winsound.Beep(1000, 200) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
            # see https://docs.python.org/3/library/winsound.html

            return self.destroy()
        if self.lifetime == 0: #if BonusObj's lifetime is up
            return self.destroy()
        return None,None

    def destroy(self):
        """Removes BonusObj from screen, processes points change"""
        self.turtleObj.clearstamp(self.stampID)
        if self.earned == True:
            return self.pointsValue, self.snakeLengthChange
        else:
            return 0,0 #Potential future feature: a penalty for not getting the bonus?

class Snake:
    def __init__(self,xSquares,ySquares,snakeDrawer,miscDrawer,scorePrinter, bonusObjDrawer, grid,obstaclePositionTuples=[]):
        #grid as parameter is temporary
        """Initialize variables for a Snake instance.
            snakeDrawer and miscDrawer are turtle.Turtle() objects.
            Some initial values need to be tweaked, or added in
            game difficulty modes/settings"""
        #TEMP
        self.grid = grid
        #

        #Turtle objects; assumes they have already been set up with penup() and speed 0
        self.snakeDrawer = snakeDrawer
        self.miscDrawer = miscDrawer
        self.scorePrinter = scorePrinter
        self.bonusObjDrawer = bonusObjDrawer

        self.headDirection = "left"
        self.lastDirection = "left"
        self.headDirectionSet = False
        self.xLimit = xSquares - 1
        self.yLimit = ySquares - 1
        
        self.posList = [] #List of (x,y) tuples on the virtual grid; used for internal processing
        self.stampIDList = [] #List of stampIDs for the snake; used for turtle to display the snake on screen
        
        ''' disabled user-set initialPointTuple functionality '''
                
        self.properLength = 5 #initial length of snake
        ''' disabled user-set self.length functionality
        #self.properLength = initialLength #The length of the snake, in number of units on the virtual grid
        '''

        self.currentScore = 0
        """Note to Joseph: Consistency of variable names, such as the one below:
            should each game loop a "turn" or something else?
            Also, should the display be called the "screen", the "board", or something else?"""
        self.turnsSinceLastBonus = 0
        self.bonusMaxFreq = 2 #i.e. x turns minimum between bonuses
        self.bonusObjOnScreen = None

        self.obstaclePositionTuples = obstaclePositionTuples
        #Note: game speed is set by the main game loop: does the
        #Snake object need to know the game speed? It would
        #potentially affect the game score

        #Set up initial graphics for the snake object
        for i in range(-2,-2+self.properLength):
            self.posList.append((xSquares//2-i,ySquares//2))
            self.snakeDrawer.setpos(self.grid[ySquares//2][xSquares//2-i])
            stampID = self.snakeDrawer.stamp()
            self.stampIDList.append(stampID)
        self.scorePrinter.setpos(300, 50) # where the center of the text is
        self.scorePrinter.write("Score: " + str(self.currentScore), True, align="center", font=("Arial", 32, "bold"))
        

    def moveSnake(self,newHeadDirection, lastHeadDirection):
        """Handle both internal variables and screen display to move
            the snake one unit"""
        print("newHeadDirection is", newHeadDirection)
        print("lastHeadDirection is", lastHeadDirection)
        print()
        #Add new head unit of snake
        lastHeadX, lastHeadY = self.posList[len(self.posList)-1]
        if newHeadDirection == "left":
            newHeadX = lastHeadX-1
            newHeadY = lastHeadY
        elif newHeadDirection == "right":
            newHeadX = lastHeadX+1
            newHeadY = lastHeadY
        elif newHeadDirection == "up":
            newHeadX = lastHeadX
            newHeadY = lastHeadY-1 #Coordinate system of display has downwards y-direction as positive
        elif newHeadDirection == "down":
            newHeadX = lastHeadX
            newHeadY = lastHeadY+1 #Coordinate system of display has downwards y-direction as positive
        self.posList.append((newHeadX,newHeadY))

        #Determine if the snake has run into anything that would kill it
        if self.isCollision(self.posList[len(self.posList)-1]):
            #Special graphics, e.g. stunned/dead snake head???
            return True #ie isDead = True
        else:
            self.snakeDrawer.setpos(self.grid[newHeadY][newHeadX])

            # changes the snake head image to make it turn a specific direction
            if newHeadDirection == "up":
                self.snakeDrawer.shape("snake-head-40px-1.gif")
            if newHeadDirection == "left":
                self.snakeDrawer.shape("snake-head-40px-2.gif")
            if newHeadDirection == "down":
                self.snakeDrawer.shape("snake-head-40px-3.gif")
            if newHeadDirection == "right":
                self.snakeDrawer.shape("snake-head-40px-4.gif")
            # stamp new heads
            stampID = self.snakeDrawer.stamp()            
            self.stampIDList.append(stampID)

            # try to overwrite previous "heads"
            self.snakeDrawer.shape("snake-body-40px.gif")
            self.snakeDrawer.setpos(self.grid[lastHeadY][lastHeadX])
            overwriteStampID = self.snakeDrawer.stamp()
            # clear the stamp whose ID is the second-to-last value of StampIDLIst, i.e. the body after the haed
            self.snakeDrawer.clearstamp(self.stampIDList[len(self.stampIDList)-2])
            # overwrite the stamp ID of the previous "head"
            self.stampIDList[len(self.stampIDList)-2] = overwriteStampID

        #Remove tail unit of snake, if necessary
        if len(self.posList) > self.properLength:
            #Because of how the game loop is set up, the snake can only be
            #at most 1 unit over its proper length
            self.posList.pop(0) #remove the tail unit of the snake
            self.snakeDrawer.clearstamp(self.stampIDList.pop(0))
        return False #ie isDead = False

    def isCollision(self,headPosTuple):
        headX, headY = headPosTuple
        if headX < 0 or headY < 0 or headX > self.xLimit or headY > self.yLimit:
            #The snake ran into the borders
            return True
        elif headPosTuple in self.posList[0:len(self.posList)-1]: #a slice from 0 to just before headPosTuple
            #The snake ran into itself
            return True
        elif headPosTuple in self.obstaclePositionTuples:
            #The snake ran into an obstacle
            return True
        else:
            return False

    def updateScore(self):
        """Updates currentScore (add points for time survived &
            bonus items eaten) and displays it"""
        #Points for time survived
        self.currentScore += 1
        #Points for bonus object, if any
        if self.bonusObjOnScreen != None:
            bonusPoints, snakeLengthChange = self.bonusObjOnScreen.update(self.posList[len(self.posList)-1], self.currentScore)
            if bonusPoints != None:
                if bonusPoints == 0: #BonusObj destroyed, but player didn't get it
                    self.bonusObjOnScreen = None
                else:
                    self.currentScore += bonusPoints
                    self.properLength += snakeLengthChange
                    self.bonusObjOnScreen = None

        #Display updated score
        self.scorePrinter.undo()        
        self.scorePrinter.setpos(300, 50) # where the center of the text is
        #self.scorePrinter.clear() No longer needed with manual wn.update()
        self.scorePrinter.write("Score: " + str(self.currentScore), True, align="center", font=("Arial", 32, "bold"))



    def determineBonusSpawn(self):
        """Determines whether or not to spawn a bonus item
            method NOT TESTED YET"""
        self.turnsSinceLastBonus += 1
        if self.bonusObjOnScreen is None: #Only spawn a new bonus item if there isn't already one on the board
            #The variable below could be changed
            bonusSpawnThreshold = 0
            #bonusSpawnThreshold = 0.7
            if self.turnsSinceLastBonus > self.bonusMaxFreq:
                randNumGenerator = random.Random()
                #randNumGenerator.random() returns a decimal number in range [0.0,1.0)
                if randNumGenerator.random() > bonusSpawnThreshold:
                    #Set up a BonusObj
                    while True:
                        #Get place for bonusObj to spawn
                        x = randNumGenerator.randint(0,self.xLimit)
                        y = randNumGenerator.randint(0,self.yLimit)
                        if (x,y) not in self.posList: #bonusObj cannot spawn on a space the snake occupies,
                            break #only break if (x,y) is not a space the snake is on
                    self.bonusObjOnScreen = BonusObj(self.bonusObjDrawer,"apple",x,y,10,10,1, self.grid) #parameters need to be confirmed
                    self.turnsSinceLastBonus = 0
    
    def upKeyHandler(self):
        """Will be called whenever key 'up' is pressed"""
        print("up key pressed") #For debugging
        #Only the first valid key press will be accepted        
        if self.headDirectionSet is False: 
            # And it cannot turn "up" when it's already going up (to remove bugs in the graphics part)
            if self.headDirection != "down" and self.headDirection != "up": #last headDirection cannot be "down"
                self.lastDirection = self.headDirection
                self.headDirection = "up" #Set new headDirection                
                self.headDirectionSet = True

    def downKeyHandler(self):
        """Will be called whenever key 'down' is pressed"""
        print("down key pressed") #For debugging
        if self.headDirectionSet is False: #Only the first valid key press will be accepted
            if self.headDirection != "up" and self.headDirection != "down": #last headDirection cannot be "up"
                self.lastDirection = self.headDirection
                self.headDirection = "down" #Set new headDirection
                self.headDirectionSet = True

    def leftKeyHandler(self):
        """Will be called whenever key 'left' is pressed"""
        print("left key pressed") #For debugging
        if self.headDirectionSet is False: #Only the first valid key press will be accepted
            if self.headDirection != "right" and self.headDirection != "left": #last headDirection cannot be "right"
                self.lastDirection = self.headDirection
                self.headDirection = "left" #Set new headDirection
                self.headDirectionSet = True

    def rightKeyHandler(self):
        """Will be called whenever key 'right' is pressed"""
        print("right key pressed") #For debugging
        if self.headDirectionSet is False: #Only the first valid key press will be accepted
            if self.headDirection != "left" and self.headDirection != "right": #last headDirection cannot be "left"
                self.lastDirection = self.headDirection
                self.headDirection = "right" #Set new headDirection
                self.headDirectionSet = True

    def processFrame(self):
        """The main game loop should call this method once each loop.
            This method updates internal variables and the screen display"""

        # makes a low-pitched beep every time the snake moves
        winsound.Beep(600, 100) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
        # see https://docs.python.org/3/library/winsound.html

        isDead = self.moveSnake(self.headDirection, self.lastDirection)
        
        self.determineBonusSpawn()
        self.headDirectionSet = False
        if isDead == True:            
            return True #ie isDead = True
        self.updateScore()
        #self.determineBonusSpawn()
        #Note: at the moment wn.update() is not done in this class