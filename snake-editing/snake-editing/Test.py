#Test sections of code
import time
import turtle

screenWidth = 500
screenHeight = 500
xSquares = 10 # number of horizontal virtual squares
ySquares = 5 # number of vertical virtual squares
squareWidth = screenWidth/xSquares
squareHeight = screenHeight/ySquares


wn = turtle.Screen()
snake = turtle.Turtle()
wn.setup(screenWidth, screenHeight)
wn.setworldcoordinates(0, 0, screenWidth, screenHeight)


snake.penup()
snake.speed(0)
wn.register_shape("C:\Maple_small.gif")
snake.shape("C:\Maple_small.gif")

# set coordinates
grid = []
for x in range(xSquares):
    grid.append([])    
    for y in range(ySquares):
        grid[x].append((squareWidth*x,squareHeight*y))
print(grid)

isDead = False
count = 0
previousTime = time.perf_counter()
while(isDead != True):
    currentTime = time.perf_counter()
    while(currentTime - previousTime >= 2):
        #print(currentTime - previousTime)
        out1=currentTime - previousTime
        out2=count
        #previousTime = currentTime #start countdown from beginning of loop
        #Proves that turtle drawing does take time (compare "count" values)
        if count > 170000:
            for x in range(xSquares):
                for y in range(ySquares):
                    snake.setposition(grid[x][y])
                    snake.stamp()
        
        count = 0
        #previousTime = currentTime #start countdown from end of loop
    count += 1
