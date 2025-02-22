import turtle

t = turtle.Turtle()
s=turtle.Screen()

s.bgcolor("white")
t.fillcolor("red")
for i in range(4):
    t.forward(100)
    t.left(90)

t.penup()
t.forward(200)
t.pendown()

for i in range(4):
    t.forward(100)
    t.right(90)
    t.forward(50)
    t.right(90)

t.penup()
t.backward(400)
t.pendown()

for i in range(6):
    t.forward(100)
    t.right(60)

turtle.done()