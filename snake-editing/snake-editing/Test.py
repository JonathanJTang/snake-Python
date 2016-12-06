#Test sections of code
import time
import turtle

wn = turtle.Screen()
snake = turtle.Turtle()

isDead = False
count = 0

snake.penup()
snake.speed(0)
wn.register_shape("C:\Joseph\Maple_small.gif")
snake.shape("C:\Joseph\Maple_small.gif")

previous = time.perf_counter()
# set coordinates
grid = []
for x in range(xSquares):
    grid.append([])    
    for y in range(ySquares):
        grid[x].append((squareWidth*x,squareHeight*y))
        snake.setposition(grid[x][y])
        snake.stamp()
print(grid)
current = time.perf_counter()#+1
print(current-previous)



while(isDead != True):
    current = time.perf_counter()
    while(current - previous >= 2):
        print(current - previous)
        print(count)
        
        
        count = 0
        previous = current
    count += 1
