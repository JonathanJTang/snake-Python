'''
Project Name:
Authors: Jonathan Tang & Joseph Tang
Created on:

Edited 
'''
import turtle
import time


def gameMain():
    #Initialize variables
    isDead = False
    count = 0
    previousTime = time.perf_counter()
    gameSpeed = 1
    loopInterval = 1/gameSpeed

    #Main game loop
    while(isDead != True):
        currentTime = time.perf_counter()
        while(currentTime - previousTime >= loopInterval):
            #print(currentTime - previousTime)
            #out1=currentTime - previousTime
            #out2=count

            previousTime = currentTime #start countdown from beginning of loop
        
            #[Insert Code]
        
            #count = 0
            #previousTime = currentTime #start countdown from end of loop
        #count += 1

    #Game over code

if __name__ == "__main__":
    gameMain()