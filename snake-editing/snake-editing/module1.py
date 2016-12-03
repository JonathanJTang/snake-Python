#From solution "co-op programs", last edited Dec 2, 2016
import turtle

snakePos = 0

grid = range(10)
# initialize 2D list
for i in range(10):
    grid[i] = range(10)

def createCanvas():
    wn = turtle.Screen()
    wn.bgcolor("lightgreen")
    snake = turtle.Turtle()

    return wn

