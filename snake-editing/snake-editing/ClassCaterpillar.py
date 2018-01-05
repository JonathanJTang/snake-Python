# Copied from Graphics.py, 1/02/2018

import turtle
import random

"""To Joseph: Check out module simpleaudio? It appears to be supported on all operating systems.
http://simpleaudio.readthedocs.io/en/latest/capabilities.html"""
try:
    import winsound #Only available on windows devices
    # see https://docs.python.org/3/library/winsound.html
    winsoundInstalled = True
except: #on Macs there will be ImportError
    #print("Module winsound not installed on device. All game sounds will be disabled")
    winsoundInstalled = False



class BonusObj:
    """Class for Bonus objects that affect a caterpillar's
        properLength, points, etc."""
    #Class attributes below can be accessed by all instances of BonusObj
    turtleShape = {"apple": "apple-40px.gif",
                   "apple2": "apple-2-40px.gif",
                   "leaf": "leaf-green-40px.gif"}
    
    '''ISSUE:  Make parameters for all BonusObj types a class attribute?'''

    def __init__(self,turtleObj,bonusTypeStr,positionTuple,turtleDisplayCoordTuple,lifetime,pointsValue,caterpillarLengthChange):
        """Initializes variables for a BonusObj instance. See comments
            in method for explanation of parameters"""
        #Make pointsValue linked to bonusTypeStr?
        
        self.turtleObj = turtleObj
        self.positionTuple = positionTuple #The BonusObj's position in the virtual grid; not used in drawing the object
        self.turtleObj.shape(self.turtleShape[bonusTypeStr])
        self.turtleObj.setpos(turtleDisplayCoordTuple) #Assumes turtleObj already has penup() and speed 0
        self.stampID = self.turtleObj.stamp() #screen.update() will be done elsewhere
        self.pointsValue = pointsValue #The number of points the player will get; could be negative
        self.caterpillarLengthChange = caterpillarLengthChange
        self.earned = False #If the player has earned the BonusObj
        self.lifetime = lifetime #The number of game loops the object will exist

    def update(self,caterpillarHeadPositionTuple):
        """This method should be called once per game loop.
            Since BonusObj's never spawn on spaces occupied by a caterpillar,
            only need to check the caterpillar head's position each loop"""
        self.lifetime -= 1
        if caterpillarHeadPositionTuple == self.positionTuple: #The caterpillar got to the BonusObj
            self.earned = True
            if winsoundInstalled:
                # makes a high-pitched beep when the caterpillar gets the object
                winsound.Beep(1000, 200) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
            return self.destroy()
        if self.lifetime == 0: #if BonusObj's lifetime is up
            return self.destroy()
        return None,None

    def destroy(self):
        """Removes BonusObj from screen, processes points change"""
        self.turtleObj.clearstamp(self.stampID)
        if self.earned == True:
            return self.pointsValue, self.caterpillarLengthChange
        else:
            return 0,0 #Potential future feature: a penalty for not getting the bonus?


class Caterpillar:
    """Manages code to process and display a caterpillar.
        Note: wn.update() not done in this class"""
    oppositeKeys = {"up": "down",
                    "down": "up",
                    "left": "right",
                    "right": "left"}
    headShape = {"up": "snake-head-40px-1.gif",
                      "down": "snake-head-40px-3.gif",
                      "left": "snake-head-40px-2.gif",
                      "right": "snake-head-40px-4.gif"}

    def __init__(self,xSquares,ySquares,caterpillarDrawer,miscDrawer,scorePrinter, bonusObjDrawer, grid,obstaclePositionTuples=[]):
        #grid as parameter is temporary
        """Initialize variables for a Caterpillar instance.
            caterpillarDrawer and miscDrawer are turtle.Turtle() objects.
            Some initial values need to be tweaked, or added in
            game difficulty modes/settings"""
        #TEMP ??
        self.grid = grid #For Cartesian coords (x,y), use grid[y][x] to access
        #Turtle display coords
        #

        #Turtle objects; assumes they have already been set up with penup() and speed 0
        self.caterpillarDrawer = caterpillarDrawer
        self.miscDrawer = miscDrawer
        self.scorePrinter = scorePrinter
        self.bonusObjDrawer = bonusObjDrawer

        self.currentHeadDirection = "left"
        self.lastHeadDirection = "left"
        self.currentHeadDirectionSet = False
        self.xLimit = xSquares - 1
        self.yLimit = ySquares - 1
        
        self.posList = [] #List of (x,y) tuples on the virtual grid; used for internal processing
        self.stampIDList = [] #List of stampIDs for the caterpillar; used for turtle to display the caterpillar on screen
        
        ''' disabled user-set initialPointTuple functionality '''
                
        self.properLength = 5 #initial length of caterpillar
        ''' disabled user-set self.length functionality
        #self.properLength = initialLength #The length of the caterpillar, in number of units on the virtual grid
        '''

        self.currentScore = 0
        """Note to Joseph: Consistency of variable names, such as the one below:
            should each game loop a "turn" or something else?
            Also, should the display be called the "screen", the "board", or something else?"""
        self.turnsSinceLastBonus = 0
        #variable below temporarily decreased for debugging
        self.bonusMaxFreq = 2 #i.e. x turns minimum between bonuses
        self.bonusObjOnScreen = None

        self.obstaclePositionTuples = obstaclePositionTuples
        #Note: game speed is set by the main game loop: does the
        #Caterpillar object need to know the game speed? It would
        #potentially affect the game score

        #Set up initial graphics for the caterpillar object
        self.caterpillarDrawer.shape("snake-body-40px.gif")
        for i in range(-2,-2+self.properLength):
            self.posList.append((xSquares//2-i,ySquares//2))
            self.caterpillarDrawer.setpos(self.grid[ySquares//2][xSquares//2-i])
            if i == 2: #Switch image for catepillar head
                """NOTE: there should be a better way to do this"""
                self.caterpillarDrawer.shape(self.headShape[self.currentHeadDirection])
            stampID = self.caterpillarDrawer.stamp()
            self.stampIDList.append(stampID)
        self.scorePrinter.setpos(300, 50) # where the center of the text is
        self.scorePrinter.write("Score: " + str(self.currentScore), True, align="center", font=("Arial", 32, "bold"))
        

    def moveCaterpillar(self): #Removed parameters newHeadDirection, lastHeadDirection as self has them as attributes
        """Handle both internal variables and screen display to move
            the caterpillar one unit"""
        if self.currentHeadDirectionSet == False: #No key press from user detected
            self.lastHeadDirection = self.currentHeadDirection #Update self.lastHeadDirection
        newHeadDirection = self.currentHeadDirection

        print("newHeadDirection is", newHeadDirection)
        print("lastHeadDirection is", self.lastHeadDirection)
        print()

        #Find and record new headPosTuple of caterpillar
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

        #Determine if the caterpillar has run into anything that would kill it
        if self.hasCollision(self.posList[len(self.posList)-1]):
            """Special graphics, e.g. stunned/dead caterpillar head???"""
            return True #ie isDead = True
        else:
            #Stamp new head
            self.caterpillarDrawer.shape(self.headShape[newHeadDirection])
            self.caterpillarDrawer.setpos(self.grid[newHeadY][newHeadX])
            stampID = self.caterpillarDrawer.stamp()            
            self.stampIDList.append(stampID)

            #Remove and replace previous head image
            self.caterpillarDrawer.shape("snake-body-40px.gif")
            self.caterpillarDrawer.setpos(self.grid[lastHeadY][lastHeadX])
            overwriteStampID = self.caterpillarDrawer.stamp()
            #Remove the stamp whose ID is the second-to-last value of StampIDLIst, i.e. the body unit after the head
            self.caterpillarDrawer.clearstamp(self.stampIDList[len(self.stampIDList)-2])
            #Overwrite the stamp ID of the previous "head"
            self.stampIDList[len(self.stampIDList)-2] = overwriteStampID

        #Remove tail units of caterpillar if necessary and put in new tail image
        """Update last body image to tail image around this part of code"""
        if len(self.posList) > self.properLength:
            #Because of how the game loop is set up, the caterpillar can only be
            #at most 1 unit over its proper length
            self.posList.pop(0) #remove the tail unit of the caterpillar
            self.caterpillarDrawer.clearstamp(self.stampIDList.pop(0))
        return False #i.e. isDead = False

    def hasCollision(self,headPosTuple):
        """Determine if the caterpillar has collided with something
            that will kill it; Returns True or False.
            Only the caterpillar head's new coordinates are needed,
            since it's the only coordinate changing each game loop"""
        headX, headY = headPosTuple
        if headX < 0 or headY < 0 or headX > self.xLimit or headY > self.yLimit:
            #The caterpillar ran into the borders
            return True
        elif headPosTuple in self.posList[0:len(self.posList)-1]: #a slice from 0 to just before headPosTuple
            #The caterpillar ran into itself
            return True
        elif headPosTuple in self.obstaclePositionTuples:
            #The caterpillar ran into an obstacle
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
            bonusPoints, caterpillarLengthChange = self.bonusObjOnScreen.update(self.posList[len(self.posList)-1])
            if bonusPoints != None:
                if bonusPoints == 0: #BonusObj destroyed, but player didn't get it
                    self.bonusObjOnScreen = None
                    self.turnsSinceLastBonus = 0
                else:
                    self.currentScore += bonusPoints
                    self.properLength += caterpillarLengthChange
                    self.bonusObjOnScreen = None
                    self.turnsSinceLastBonus = 0

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
                    for i in range(self.xLimit*self.yLimit): #set a maximum of attempts for finding a suitable bonus position
                        #Get place for bonusObj to spawn
                        x = randNumGenerator.randint(0,self.xLimit)
                        y = randNumGenerator.randint(0,self.yLimit)
                        if (x,y) not in self.posList: #bonusObj cannot spawn on a space the caterpillar occupies,
                            break #only break if (x,y) is not a space the caterpillar is on
                    self.bonusObjOnScreen = BonusObj(self.bonusObjDrawer,"apple",(x,y),self.grid[y][x],10,10,3)
                    """parameters of BonusObj.__init__() need to be confirmed"""
    
    def processKeyPress(self,pressedKeyStr):
        """Processes genuine key presses (first press per turn)"""
        if pressedKeyStr != self.currentHeadDirection and pressedKeyStr != self.oppositeKeys[self.currentHeadDirection]:
            #Logically, new headDirection cannot be the opposite of the current headDirection,
            #nor the same as the current headDirection
            self.lastHeadDirection = self.currentHeadDirection #save old headDirection
            self.currentHeadDirection = pressedKeyStr #Set new headDirection                
            self.currentHeadDirectionSet = True

    def upKeyHandler(self):
        """Will be called whenever key 'up' is pressed"""
        #print("up key pressed") #For debugging
        if self.currentHeadDirectionSet is False: #Only the first valid key press will be accepted
            self.processKeyPress("up")

    def downKeyHandler(self):
        """Will be called whenever key 'down' is pressed"""
        #print("down key pressed") #For debugging
        if self.currentHeadDirectionSet is False: #Only the first valid key press will be accepted
            self.processKeyPress("down")

    def leftKeyHandler(self):
        """Will be called whenever key 'left' is pressed"""
        #print("left key pressed") #For debugging
        if self.currentHeadDirectionSet is False: #Only the first valid key press will be accepted
            self.processKeyPress("left")

    def rightKeyHandler(self):
        """Will be called whenever key 'right' is pressed"""
        #print("right key pressed") #For debugging
        if self.currentHeadDirectionSet is False: #Only the first valid key press will be accepted
            self.processKeyPress("right")

    def processFrame(self):
        """The main game loop should call this method once each loop.
            This method updates internal variables and the screen display"""
        
        if winsoundInstalled:
            # makes a low-pitched beep every time the caterpillar moves
            winsound.Beep(600, 100) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)

        nowDead = self.moveCaterpillar()
        self.currentHeadDirectionSet = False
        self.determineBonusSpawn()
        if nowDead == True:            
            return True #ie isDead = True
        self.updateScore()
        #Note: at the moment wn.update() is not done in this class