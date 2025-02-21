import turtle

sc = turtle.Screen()
sc.setup(400,400)
sc.bgcolor("yellow")

turtle.title("Welcome to Turtle Window")

board = turtle.Turtle()

for i in range(4):
    board.forward(100)
    board.right(90)

turtle.done()