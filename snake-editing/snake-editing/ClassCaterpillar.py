# Copied from Graphics.py, 1/02/2018

import turtle
import random
"""Module simpleaudio: appears to be supported on all operating systems.
http://simpleaudio.readthedocs.io/en/latest/capabilities.html """
try:
    import simpleaudio as sa
    simpleaudioInstalled = True
except:
    #print("Module simpleaudio not installed on device. All game sounds will be disabled")
    simpleaudioInstalled = False
    pass

'''
try:
    import winsound #Only available on windows devices
    # see https://docs.python.org/3/library/winsound.html
    winsoundInstalled = True
except: #on Macs there will be ImportError
    #print("Module winsound not installed on device. All game sounds will be disabled")
    winsoundInstalled = False
'''

class Button:
    """Class for buttons on the turtle window.
        Will change color when mouse hovers over it;
        Will lead to an action/change of state when clicked"""

    #Keep in mind that turtleObj used in this class are shared among all buttons
    #It's assumed that the turtleObj will be penup

    def __init__(self, topLeftX, topLeftY, bottomRightX, bottomRightY, origImageStr, hoverImageStr, turtleObj):
        """Initialize button object by saving required variables and
            displaying the original state of the button"""
        #Note: topLeft and bottomRight coordinates are turtle coordinates
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.posTuple = ((topLeftX+bottomRightX)//2, (topLeftY+bottomRightY)//2)
        self.origImageStr = origImageStr
        self.hoverImageStr = hoverImageStr
        self.hover = False

        #Display button
        turtleObj.setpos(posTuple)
        turtleObj.shape(self.origImageStr)
        self.currentStamp = turtleObj.stamp()

    def isHover(self):
        return self.hover

    def changeToHover(self, turtleObj):
        """Change the button's appearance to the hover image"""
        turtleObj.clearstamp(self.currentStamp)
        turtleObj.shape(self.hoverImageStr)
        turtleObj.setpos(posTuple)
        self.currentStamp = turtleObj.stamp()
        self.hover = True

    def changeToOrig(self, turtleObj):
        """Change the button's appearance to the original image"""
        turtleObj.clearstamp(self.currentStamp)
        turtleObj.shape(self.origImageStr)
        turtleObj.setpos(posTuple)
        self.currentStamp = turtleObj.stamp()
        self.hover = False

    def mouseCoordsOnButton(self, mouseXCoord, mouseYCoord):
        """Check if the given mouse coordinates are within
            the boundaries of the button"""
        return (self.topLeftX <= mouseXCoord and mouseXCoord <= self.bottomRightX and
               self.topLeftY <= mouseYCoord and mouseYCoord <= self.bottomRightY)

    def clicked(self):
        pass


class BonusObj:
    """Class for Bonus objects that affect a caterpillar's
        properLength, points, etc."""
    #Class attributes below can be accessed by all instances of BonusObj
    turtleShape = {"apple": "apple-40px.gif",
                   "apple2": "apple-2-40px.gif",
                   "leaf": "leaf-green-40px.gif",
                   "blank":"apple-flash.gif"}
    
    '''ISSUE:  Make parameters for all BonusObj types a class attribute?'''

    def __init__(self,turtleObj,bonusTypeStr,positionTuple,turtleDisplayCoordTuple,lifetime,pointsValue,caterpillarLengthChange):
        """Initializes variables for a BonusObj instance. See comments
            in method for explanation of parameters"""
        #Make pointsValue linked to bonusTypeStr?
        
        self.turtleObj = turtleObj
        self.positionTuple = positionTuple #The BonusObj's position in the virtual grid; not used in drawing the object
        self.turtleObj.shape(self.turtleShape[bonusTypeStr])
        self.coordinates = turtleDisplayCoordTuple
        self.turtleObj.setpos(turtleDisplayCoordTuple) #Assumes turtleObj already has penup() and speed 0
        self.stampID = self.turtleObj.stamp() #screen.update() will be done elsewhere
        self.pointsValue = pointsValue #The number of points the player will get; could be negative
        self.caterpillarLengthChange = caterpillarLengthChange
        self.earned = False #If the player has earned the BonusObj
        self.lifetime = lifetime #The number of game loops the object will exist

        self.flashOn = False # if true, then cover up apple; if false, reveal apple
        self.flashStampID = 0
        print(self.lifetime) # lifetime is random number (see line 372)

    def update(self,caterpillarHeadPositionTuple):
        """This method should be called once per game loop.
            Since BonusObj's never spawn on spaces occupied by a caterpillar,
            only need to check the caterpillar head's position each loop"""
        self.lifetime -= 1

        # flash if about to disappear in 5 seconds         
        self.flash()
        
        if caterpillarHeadPositionTuple == self.positionTuple: #The caterpillar got to the BonusObj
            self.earned = True
            # make sure the blank/flash block gets removed in the end        
            self.turtleObj.clearstamp(self.flashStampID) # remove blank square, revealing the apple
            
            '''
            # makes a high-pitched beep when the caterpillar gets the object
            if winsoundInstalled:
                winsound.Beep(1000, 200) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
            '''
            return self.destroy()
               

        if self.lifetime == 0: #if BonusObj's lifetime is up
            return self.destroy()
        return None,None
    
    def flash(self):
        """Flashes for 5 seconds before it disappears"""
        if self.lifetime < 5:
            print("flash--" + str(self.lifetime))
            if self.flashOn == False and self.lifetime != 0:   # if apple is showing
                self.turtleObj.shape(self.turtleShape["blank"])
                self.turtleObj.setpos(self.coordinates) #Assumes turtleObj already has penup() and speed 0
                self.flashStampID = self.turtleObj.stamp() # stamp blank square, covering up the apple
                self.flashOn = True
            elif self.flashOn == True:            
                self.turtleObj.clearstamp(self.flashStampID) # remove blank square, revealing the apple
                self.flashOn = False


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
    headShape = {"up": "snake-head-1-thinner.gif",
                "down": "snake-head-3-thinner.gif",
                "left": "snake-head-2-thinner.gif",
                "right": "snake-head-4-thinner.gif"}
    bodyShape = {"vertical": "snake-body-v-thinner.gif",
                 "horizontal": "snake-body-h-thinner.gif",
                 "curveUpRight": "snake-curve-up-right.gif", # curveUpRight = has straight line borders on up and right side of the body
                 "curveUpLeft": "snake-curve-up-left.gif", #Add here
                 "curveDownRight": "snake-curve-down-right.gif", #Add here
                 "curveDownLeft": "snake-curve-down-left.gif", #Add here
                 "oldGeneric": "snake-body-40px.gif"} #Eventually delete this entry
    tailShape = {"up": "snake-tail-1-thinner.gif",
                "down": "snake-tail-3-thinner.gif",
                "left": "snake-tail-2-thinner.gif",
                "right": "snake-tail-4-thinner.gif"}
    deadHeadShape = {"up": "snake-head-dead-1.gif",
                "down": "snake-head-dead-3.gif",
                "left": "snake-head-dead-2.gif",
                "right": "snake-head-dead-4.gif"}

    def __init__(self,xSquares,ySquares,caterpillarDrawer,miscDrawer,textPrinter,scorePrinter, bonusObjDrawer, grid,obstaclePositionTuples=[]):
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
        self.textPrinter = textPrinter
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
        """NOTE: there should be a better way to do this"""
        for i in range(-2,-2+self.properLength):
            self.posList.append((xSquares//2-i,ySquares//2))
            self.caterpillarDrawer.setpos(self.grid[ySquares//2][xSquares//2-i])
            self.caterpillarDrawer.shape(self.bodyShape["horizontal"])
            if i == -2: #Switch image for caterpillar tail
                self.caterpillarDrawer.shape(self.tailShape["right"])
            if i == 2: #Switch image for caterpillar head
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
        #In case instance attributes change in the middle of method
        newHeadDirection = self.currentHeadDirection
        previousHeadDirection = self.lastHeadDirection

        ''' For debugging
        print("newHeadDirection is", newHeadDirection)
        print("previousHeadDirection is", previousHeadDirection)
        print()'''

        #Find and record new headPosTuple of caterpillar
        lastHeadX, lastHeadY = self.posList[-1] # list[-1] gets the value of the last index
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
        if self.hasCollision(self.posList[-1]):
            """Special graphics, e.g. stunned/dead caterpillar head???"""            
            self.caterpillarDrawer.clearstamp(self.stampIDList[-1])   # erase alive head

            # the next two lines use "previousHeadDirection" and "lastHeadX & Y" 
            # because
            self.caterpillarDrawer.shape(self.deadHeadShape[previousHeadDirection])
            self.caterpillarDrawer.setpos(self.grid[lastHeadY][lastHeadX])           
            stampID = self.caterpillarDrawer.stamp()
            stampID = self.stampIDList[-1]
            
            return True #ie isDead = True
        else:
            #Stamp new head
            self.caterpillarDrawer.shape(self.headShape[newHeadDirection])
            self.caterpillarDrawer.setpos(self.grid[newHeadY][newHeadX])
            stampID = self.caterpillarDrawer.stamp()            
            self.stampIDList.append(stampID)

            #Remove and replace previous head image with appropriate body unit
            if (previousHeadDirection == "left" and newHeadDirection == "left") \
                or (previousHeadDirection == "left" and newHeadDirection == "right") \
                or (previousHeadDirection == "right" and newHeadDirection == "left") \
                or (previousHeadDirection == "right" and newHeadDirection == "right"):
                bodyShapeType = "horizontal"
            elif (previousHeadDirection == "up" and newHeadDirection == "up") \
                or (previousHeadDirection == "up" and newHeadDirection == "down") \
                or (previousHeadDirection == "down" and newHeadDirection == "up") \
                or (previousHeadDirection == "down" and newHeadDirection == "down"):
                bodyShapeType = "vertical"
            elif (previousHeadDirection == "down" and newHeadDirection == "right") \
                or (previousHeadDirection == "left" and newHeadDirection == "up"):
                bodyShapeType = "curveUpRight"
            #else: #Delete this after all curve images have been added
                #bodyShapeType = "oldGeneric"
            #Uncomment this section after all curve images have been added
            elif (previousHeadDirection == "up" and newHeadDirection == "right") \
                or (previousHeadDirection == "left" and newHeadDirection == "down"):
                bodyShapeType = "curveDownRight"
            elif (previousHeadDirection == "up" and newHeadDirection == "left") \
                or (previousHeadDirection == "right" and newHeadDirection == "down"):
                bodyShapeType = "curveDownLeft"
            elif (previousHeadDirection == "down" and newHeadDirection == "right") \
                or (previousHeadDirection == "left" and newHeadDirection == "up"):
                bodyShapeType = "curveUpRight"
            elif (previousHeadDirection == "down" and newHeadDirection == "left") \
                or (previousHeadDirection == "right" and newHeadDirection == "up"):
                bodyShapeType = "curveUpLeft"
            
            
            self.caterpillarDrawer.shape(self.bodyShape[bodyShapeType])
            self.caterpillarDrawer.setpos(self.grid[lastHeadY][lastHeadX])
            overwriteStampID = self.caterpillarDrawer.stamp() #stamp new body image
            #Remove the stamp whose ID is the second-to-last value of StampIDLIst, i.e. the body unit after the head
            self.caterpillarDrawer.clearstamp(self.stampIDList[-2]) # list[-2] is the second-to-last value in the list
            #Overwrite the stamp ID of the previous "head"
            self.stampIDList[-2] = overwriteStampID

        #Remove tail unit of caterpillar if necessary
        if len(self.posList) > self.properLength:
            #Because of how the game loop is set up, the caterpillar can only be
            #at most 1 unit over its proper length
            self.posList.pop(0) #remove the tail unit of the caterpillar
            self.caterpillarDrawer.clearstamp(self.stampIDList.pop(0))

        #Put in new tail image
        tailX, tailY = self.posList[0]
        secondLastUnitX, secondLastUnitY = self.posList[1]
        #4 possibilities: tailUnit is either to the left, right, up, or down of the secondLastUnit
        if tailX == secondLastUnitX:
            if tailY > secondLastUnitY:
                tailShapeType = "down" #tail below secondLastUnit
            else:
                tailShapeType = "up" #tail above secondLastUnit
        else: #means tailY == secondLastUnitY
            if tailX > secondLastUnitX:
                tailShapeType = "right" #tail right of secondLastUnit
            else:
                tailShapeType = "left" #tail left of secondLastUnit
        self.caterpillarDrawer.shape(self.tailShape[tailShapeType])
        self.caterpillarDrawer.setpos(self.grid[tailY][tailX])
        overwriteStampID = self.caterpillarDrawer.stamp() #stamp new tail
        #Remove the image of the previous "tail"
        self.caterpillarDrawer.clearstamp(self.stampIDList[0])
        #Overwrite the stamp ID of the previous "tail"
        self.stampIDList[0] = overwriteStampID

        self.currentHeadDirectionSet = False
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
        elif headPosTuple in self.posList[0:-1]: #a slice from 0 to just before headPosTuple
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
            bonusPoints, caterpillarLengthChange = self.bonusObjOnScreen.update(self.posList[-1])
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
                    self.bonusObjOnScreen = BonusObj(self.bonusObjDrawer,"apple",(x,y),self.grid[y][x],random.randint(8,20),10,3)
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
        
        '''
        if winsoundInstalled:
            # makes a low-pitched beep every time the caterpillar moves
            winsound.Beep(600, 100) # winsound.Beep takes two parameters: frequency(in Hz), duration (in milleseconds)
        '''

        nowDead = self.moveCaterpillar()
        self.determineBonusSpawn()
        if nowDead == True:            
            return True #ie isDead = True
        self.updateScore()
        #Note: at the moment wn.update() is not done in this class