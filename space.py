import turtle
import random


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.setup(width=800, height=600)
# wn.tracer(0)


player = turtle.Turtle()
player.speed(0)
player.shape("triangle")
player.color("white")
player.penup()
player.goto(0, -250)
player.setheading(90)
player_speed = 30


bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("circle")
bullet.color("purple")
bullet.shapesize(stretch_wid=0.5, stretch_len=1.5)
bullet.penup()
bullet.hideturtle()
bullet_speed = 50
bullet_state = "ready"

game_over_pen = turtle.Turtle()
game_over_pen.hideturtle()
game_over_pen.color("white")
game_over_pen.penup()
game_over_pen.goto(0, 0)


aliens = []
alien_speed = 10
rows = 3
cols = 6

for i in range(rows):
    for j in range(cols):
        alien = turtle.Turtle()
        alien.speed(0)
        alien.shape("circle")
        alien.color("green")
        alien.penup()
        x = -225 + j * 80
        y = 250 - i * 50
        alien.goto(x, y)
        aliens.append(alien)

alien_direction = 1
game_over = False

def move_left():
    if not game_over:
        x = player.xcor() - player_speed
        if x < -380:
            x = -380
        player.setx(x)

def move_right():
    if not game_over:
        x = player.xcor() + player_speed
        if x > 380:
            x = 380
        player.setx(x)


def fire_bullet():
    global bullet_state
    if not game_over and bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    # distance = t1.distance(t2)
    return t1.distance(t2) < 20


wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# game_over = False
# alien_direction = 1  # 1 = derecha, -1 = izquierda

# while not game_over:
#     wn.update()

def game_loop():
    global alien_direction, bullet_state, game_over

    if game_over:
        return

    edge_reached = False
    for alien in aliens:
        x = alien.xcor() + alien_speed * alien_direction
        alien.setx(x)
        if x > 380 or x < -380:
            edge_reached = True

    if edge_reached:
        alien_direction *= -1
        for alien in aliens:
            alien.sety(alien.ycor() - 40)


    if bullet_state == "fire":
        y = bullet.ycor() + bullet_speed
        bullet.sety(y)
        if y > 290:
            bullet.hideturtle()
            bullet_state = "ready"


    for alien in aliens[:]:
        if is_collision(bullet, alien):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)
            # alien.goto(1000, 1000)
            alien.hideturtle()
            aliens.remove(alien)

        if is_collision(player, alien):
            player.hideturtle()
            alien.hideturtle()
            print("GAME OVER")
            game_over = True
            game_over_pen.write("GAME OVER", align="center", font=("Arial", 36, "normal"))
            return

    if len(aliens) == 0:
        game_over = True
        game_over_pen.write("You Win!", align="center", font=("Arial", 36, "bold"))
        return


    wn.ontimer(game_loop, 50)

# print("Thanks for playing")

game_loop()
wn.mainloop()

