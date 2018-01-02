# Copied from Graphics.py, 1/02/2018

import turtle
import random

class BonusObj:
    """Class for Bonus objects that affect a snake's
        properLength, points, etc."""
    turtleShape = {"apple":"apple.jpeg"}
    
    '''ISSUE:  Add a class attribute that describes all the parameters for a BonusObj type?'''

    def __init__(turtleObj,bonusTypeStr,positionTuple,lifetime,pointsValue,snakeLengthChange):
        """Initializes variables for a BonusObj instance. See comments
            in method for explanation of parameters"""
        #Make pointsValue linked to bonusTypeStr?
        self.positionTuple = positionTuple #The BonusObj's position in the virtual grid
        turtleObj.setpos(positionTuple) #Assumes turtleObj already has penup() and speed 0
        self.stampID = turtleObj.stamp() #screen.update() will be done elsewhere
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
            return self.destroy()
        if self.lifetime == 0: #if BonusObj's lifetime is up
            return self.destroy()
        return None,None

    def destroy(self):
        turtleObj.clearstamp(self.stampID)
        if self.earned == True:
            return self.pointsValue, self.snakeLengthChange
        else:
            return None,None #Potential future feature: a penalty for not getting the bonus?

class Snake:
    def __init__(self,xSquares,ySquares,snakeDrawer,miscDrawer,grid,obstaclePositionTuples=[]):
        #grid as parameter is temporary
        """Initialize variables for a Snake instance.
            snakeDrawer and miscDrawer are turtle.Turtle() objects"""
        #TEMP
        self.grid = grid
        #

        #Turtle objects; assumes they have already been set up with penup() and speed 0
        self.snakeDrawer = snakeDrawer
        self.miscDrawer = miscDrawer

        self.headDirection = "left"
        self.xLimit = xSquares - 1
        self.yLimit = ySquares - 1
        
        self.posList = [] #List of (x,y) tuples on the virtual grid; used for internal processing
        self.stampIDList = [] #List of stampIDs for the snake; used for turtle to display the snake on screen
        
        ''' disabled user-set initialPointTuple functionality '''

        self.properLength = 3 #initial length of snake
        for i in range(self.properLength):
            self.posList.append((xSquares//2-i,ySquares//2))
            self.snakeDrawer.setpos(self.grid[ySquares//2][xSquares//2-i])
            stampID = self.snakeDrawer.stamp()
            self.stampIDList.append(stampID)

        ''' disabled user-set self.length functionality
        #self.properLength = initialLength #The length of the snake, in number of units on the virtual grid
        '''

        self.currentScore = 0
        """Note to Joseph: Consistency of variable names, such as the one below:
            should each game loop a "turn" or something else?
            Also, should the display be called the "screen", the "board", or something else?"""
        self.turnsSinceLastBonus = 0
        self.bonusMaxFreq = 4 #i.e. x turns minimum between bonuses
        self.bonusObjOnScreen = None

        self.obstaclePositionTuples = obstaclePositionTuples
        #Note: game speed is set by the main game loop: does the
        #Snake object need to know the game speed? It would
        #potentially affect the game score

        

    def moveSnake(self,newHeadDirection):
        """Handle both internal variables and screen display to move
            the snake one unit"""
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

        #Remove tail unit of snake, if necessary
        if len(self.posList) > self.properLength:
            #Because of how the game loop is set up, the snake can only be
            #at most 1 unit over its proper length
            self.posList.pop(0) #remove the tail unit of the snake
            self.snakeDrawer.clearstamp(self.stampIDList.pop(0))

        #Determine if the snake has run into anything that would kill it
        if self.isCollision(self.posList[len(self.posList)-1]):
            #Special graphics, e.g. stunned/dead snake head???
            return -1
        else:
            self.snakeDrawer.setpos(self.grid[newHeadY][newHeadX])
            stampID = self.snakeDrawer.stamp()
            self.stampIDList.append(stampID)

    def isCollision(self,headPosTuple):
        headX, headY = headPosTuple
        if headX < 0 or headY < 0 or headX > self.xLimit or headY > self.yLimit:
            #The snake ran into the borders
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
            bonusPoints, snakeLengthChange = self.bonusObjOnScreen.update()
            if bonusPoints != None:
                self.currentScore += bonusPoints
                self.length += snakeLengthChange
                self.bonusObjOnScreen = None

        #Display updated score
        pass


    def determineBonusSpawn(self):
        """Determines whether or not to spawn a bonus item
            method NOT TESTED YET"""
        self.turnsSinceLastBonus += 1
        if self.bonusObjOnScreen is None: #Only spawn a new bonus item if there isn't already one on the board
            #The variable below could be changed
            bonusSpawnThreshold = 0.7
            if self.turnsSinceLastBonus > self.bonusMaxFreq:
                randNumGenerator = random.Random()
                if randNumGenerator.random() > 0.7: #random decimal number in range [0.0,1.0)
                    #Set up a BonusObj
                    while True:
                        #Get place for bonusObj to spawn
                        x = randNumGenerator.randint(0,self.xLimit)
                        y = randNumGenerator.randint(0,self.yLimit)
                        if (x,y) not in self.posList: #bonusObj cannot spawn on a space the snake occupies,
                            break; #only break if (x,y) is not a space the snake is on
                    self.bonusObjOnScreen = BonusObj("apple",(x,y),10,10,2) #parameters need to be confirmed
                    self.turnsSinceLastBonus = 0


    def processFrame(self,snakeHeadDirection):
        """The main game loop should call this method once each loop.
            Given the snake head's current heading, the method updates
            internal variables and the screen display"""
        #For now, we'll put keyboard listening code outside the class.
        #It could potentially be moved inside here though"""
        if self.moveSnake(snakeHeadDirection) == -1:
            return True #ie isDead = True
        self.updateScore()
        #self.determineBonusSpawn()
        #Note: at the moment wn.update() is not done in this class