import turtle
import random

screen = turtle.Screen()
screen.title("Tic Tac Toe with Turtle")
screen.bgcolor("black")
screen.setup(width=600, height=600)


pen = turtle.Turtle()
pen.color("white")
pen.pensize(5)
pen.hideturtle()


pen.penup()
pen.goto(-100, 300)
pen.pendown()
pen.goto(-100, -300)

pen.penup()
pen.goto(100, 300)
pen.pendown()
pen.goto(100, -300)


pen.penup()
pen.goto(-300, 100)
pen.pendown()
pen.goto(300, 100)

pen.penup()
pen.goto(-300, -100)
pen.pendown()
pen.goto(300, -100)

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

# Ponerlo como comentario si quieres jugar contra otra persona
# y no la compu
computer = "O"


def draw_x(x, y):
    t = turtle.Turtle()
    t.color("#C68EFD")
    t.pensize(3)
    t.penup()
    t.goto(x-40, y-40)
    t.pendown()
    t.goto(x+40, y+40)
    t.penup()
    t.goto(x-40, y+40)
    t.pendown()
    t.goto(x+40, y-40)
    t.hideturtle()

def draw_o(x, y):
    t = turtle.Turtle()
    t.color("#A7E399")
    t.pensize(3)
    t.penup()
    t.goto(x, y-50)
    t.pendown()
    t.circle(50)
    t.hideturtle()


def has_winner(player):
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False


def get_cell(x, y):
    row = 0 if y > 100 else (1 if y > -100 else 2)
    col = 0 if x < -100 else (1 if x < 100 else 2)
    return row, col

# Ponlo como comentario si quieres jugar contra una persona
def computer_move():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        cx = -200 + col*200
        cy = 200 - row*200
        draw_o(cx, cy)
        board[row][col] = computer
        if has_winner(computer):
            print("Computer wins!")
            screen.bye()

def click(x, y):
    row, col = get_cell(x, y)
    if board[row][col] == "":
        cx = -200 + col*200
        cy = 200 - row*200
        draw_x(cx, cy)
        board[row][col] = current_player
        if has_winner(current_player):
            print("Player wins!")
            screen.bye()
            return

        computer_move()

# Descomentalo si quieres jugar contra alguna persona y
# no la computadora

# def click(x, y):
#     global current_player
#     row, col = get_cell(x, y)
#     if board[row][col] == "":
#         cx = -200 + col*200
#         cy = 200 - row*200
#         if current_player == "X":
#             draw_x(cx, cy)
#             board[row][col] = "X"
#             if has_winner("X"):
#                 print("Player X wins!")
#                 screen.bye()
#             current_player = "O"
#         else:
#             draw_o(cx, cy)
#             board[row][col] = "O"
#             if has_winner("O"):
#                 print("Player O wins!")
#                 screen.bye()
#             current_player = "X"


screen.onclick(click)
screen.mainloop()
