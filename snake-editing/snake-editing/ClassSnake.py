# Copied from Graphics.py, 1/02/2018

import turtle
import random

class BonusObj:
    def __init__(turtleObj,positionTuple,lifetime,pointsValue):
        self.positionTuple = positionTuple
        turtleObj.setpos(positionTuple) #Assumes turtleObj already has penup() and speed 0
        self.stampID = turtleObj.stamp()
        self.pointsValue = pointsValue
        self.earned = False
        self.lifetime = lifetime

    def update(self,snakeHeadPositionTuple):
        """Since BonusObj's never spawn on spaces occupied by a snake,
            only need to check the snake head's position each loop"""
        self.lifetime -= 1
        if snakeHeadPositionTuple == self.positionTuple:
            self.earned = True
        if self.lifetime == 0:
            self.destroy()

    def destroy(self):
        turtleObj.clearstamp(self.stampID)
        if self.earned == True:
            return self.pointsValue
        else:
            return 0

class Snake:
    def __init__(self,initialPointTuple,snakeDrawer,miscDrawer):
        """"""
        self.headDirection = "left"
        self.posList = []
        self.turtleStampList = []
        self.currentScore = 0
        self.turnsSinceLastBonus = 0
        self.bonusMaxFreq = 4 #ie x turns minimum between bonuses

        #Note: game speed is set by the main game loop: does the
        #Snake object need to know the game speed? It would
        #potentially affect the game score

    def updateScore(self):
        """Updates currentScore: add points for time survived &
            bonus items eaten"""
        self.currentScore += 1

    def updateScreen(self):
        """Updates the display: moves the snake,
            spawns bonus items if necessary, displays new score"""
        if self.turnsSinceLastBonus > bonusMaxFreq:
            randObj = random.Random()


    def processFrame(self):
        self.updateScore()
        self.updateScreen()