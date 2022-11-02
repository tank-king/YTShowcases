import time
import turtle

screen = turtle.Screen()
screen.bgcolor('#111111')
# screen.setup(500, 500, 50, 0)

W, H = 500, 500

screen.setup(W, H)
screen.tracer(0)
pen = turtle.Turtle()
pen.hideturtle()


def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))


canvas = turtle.getcanvas()
canvas.configure()


def draw_rect(_rect, color='white'):
    pen.penup()
    pen.setheading(0)
    pen.goto(_rect[0], _rect[1])
    pen.color(color)
    pen.fillcolor('black')
    pen.begin_fill()
    pen.pendown()
    for i in range(2):
        pen.forward(_rect[2])
        pen.right(90)
        pen.forward(_rect[3])
        pen.right(90)
    pen.penup()
    pen.end_fill()


def get_mouse_pos():
    global canvas
    x = canvas.winfo_pointerx() - canvas.winfo_rootx() - canvas.winfo_reqwidth() // 4
    y = canvas.winfo_pointery() - canvas.winfo_rooty() - canvas.winfo_reqheight() // 4
    x -= canvas.winfo_width() // 2
    y -= canvas.winfo_height() // 2
    y *= -1
    # print(canvas.winfo_reqwidth())
    return x, y


rect = (-50, 50, 200, 50)

while True:
    pen.clear()
    color = 'white'
    mx, my = get_mouse_pos()
    print(mx, my)
    if rect[0] <= mx <= rect[0] + rect[2]:
        if rect[1] - rect[3] <= my <= rect[1]:
            color = 'green'
    draw_rect(rect, color)
    screen.update()
    time.sleep(0.01)
