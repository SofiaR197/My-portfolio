import turtle
import time
import random

WIDTH, HEIGHT = 800, 600
wn = turtle.Screen()
wn.title("Breakout Python Turtle")
wn.bgcolor("black")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)


class Paddle:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.shape("square")
        self.t.color("white")
        self.t.shapesize(stretch_wid=1, stretch_len=6)  # paddle ~120px wide
        self.t.penup()
        self.t.goto(0, -250)

    def move_left(self):
        x = self.t.xcor() - 40
        if x < -WIDTH // 2 + 60:
            x = -WIDTH // 2 + 60
        self.t.setx(x)

    def move_right(self):
        x = self.t.xcor() + 40
        if x > WIDTH // 2 - 60:
            x = WIDTH // 2 - 60
        self.t.setx(x)

    def goto_center(self):
        self.t.goto(0, -250)


class Ball:
    def __init__(self, speed=3):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color("#EBD6FB")
        self.t.penup()
        self.t.goto(0, -100)

        angle = random.choice([30, 45, 60])
        sign = random.choice([-1, 1])
        self.dx = speed * sign
        self.dy = speed

    def move(self):
        self.t.setx(self.t.xcor() + self.dx)
        self.t.sety(self.t.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1

    def speed_up(self, factor=1.1):
        self.dx *= factor
        self.dy *= factor

    def reset(self, speed=3):
        self.t.goto(0, -100)
        angle_sign = random.choice([-1, 1])
        self.dx = speed * angle_sign
        self.dy = speed


class Brick:
    def __init__(self, x, y, color):
        self.t = turtle.Turtle()
        self.t.shape("square")
        self.t.color(color)
        self.t.shapesize(stretch_wid=1.2, stretch_len=3)
        self.t.penup()
        self.t.goto(x, y)

    def destroy(self):
        self.t.hideturtle()


class HUD:
    def __init__(self):
        self.writer = turtle.Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.color("white")
        self.writer.goto(0, HEIGHT // 2 - 40)

    def draw(self, score, lives, level):
        self.writer.clear()
        text = f"Score: {score}    Lives: {lives}    Level: {level}"
        self.writer.write(text, align="center", font=("Courier", 18, "normal"))


def create_bricks(rows=5, cols=8, start_y=200):
    bricks = []
    gap_x = 70
    gap_y = 30
    total_width = (cols - 1) * gap_x
    start_x = -total_width / 2
    colors = ["#570A57", "#C5B0CD", "#B3FFAE", "#FF6464", "#F11A7B", "#982176"]
    for row in range(rows):
        y = start_y - row * gap_y
        color = colors[row % len(colors)]
        for col in range(cols):
            x = start_x + col * gap_x
            bricks.append(Brick(x, y, color))
    return bricks


paddle = Paddle()
ball = Ball(speed=3)
hud = HUD()
score = 0
lives = 3
level = 1
bricks = create_bricks(rows=5, cols=8, start_y=200)

wn.listen()
wn.onkeypress(paddle.move_left, "Left")
wn.onkeypress(paddle.move_right, "Right")
wn.onkeypress(paddle.move_left, "a")
wn.onkeypress(paddle.move_right, "d")


def restart_level():
    global ball
    paddle.goto_center()
    ball.reset(speed=3 + (level - 1) * 0.8)
    time.sleep(0.6)


hud.draw(score, lives, level)

game_over = False
while True:
    wn.update()
    if game_over:
        break

    ball.move()

    bx = ball.t.xcor()
    by = ball.t.ycor()

    if bx > WIDTH // 2 - 10:
        ball.t.setx(WIDTH // 2 - 10)
        ball.bounce_x()
    if bx < -WIDTH // 2 + 10:
        ball.t.setx(-WIDTH // 2 + 10)
        ball.bounce_x()

    # Top wall
    if by > HEIGHT // 2 - 10:
        ball.t.sety(HEIGHT // 2 - 10)
        ball.bounce_y()

    if by < -HEIGHT // 2 - 10:
        lives -= 1
        hud.draw(score, lives, level)
        if lives <= 0:
            over = turtle.Turtle()
            over.hideturtle()
            over.color("white")
            over.penup()
            over.goto(0, 0)
            over.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
            over.goto(0, -40)
            over.write(f"Final Score: {score}", align="center", font=("Courier", 18, "normal"))
            game_over = True
            continue

        restart_level()

    if (by < paddle.t.ycor() + 20 and by > paddle.t.ycor() - 10) and (abs(bx - paddle.t.xcor()) < 80):
        offset = bx - paddle.t.xcor()

        norm = offset / 80

        ball.t.sety(paddle.t.ycor() + 20)
        ball.dy = abs(ball.dy)

        ball.dx += norm * 1.5

    for brick in bricks[:]:
        if brick.t.isvisible() and ball.t.distance(brick.t) < 45:
            brick.destroy()
            try:
                bricks.remove(brick)
            except ValueError:
                pass
            score += 10
            hud.draw(score, lives, level)

            ball.bounce_y()

            ball.speed_up(1.03)
            break

    if not bricks:
        level += 1

        msg = turtle.Turtle()
        msg.hideturtle()
        msg.penup()
        msg.color("white")
        msg.goto(0, 0)
        msg.write(f"Level {level}", align="center", font=("Courier", 28, "bold"))
        time.sleep(1.0)
        msg.clear()

        rows = min(7, 4 + level)
        cols = 8
        bricks = create_bricks(rows=rows, cols=cols, start_y=220)

        ball.reset(speed=3 + (level - 1) * 0.8)
        hud.draw(score, lives, level)
        continue

    time.sleep(0.01)

wn.mainloop()
