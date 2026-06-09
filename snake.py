import turtle
import random
import pygame.mixer

#laod the sound effect 
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

#set up the screen
n = turtle.Screen()
n.title("Snake Game")
n.bgcolor("Green")
n.setup(width=600, height=600)
n.tracer(0)

#head of the snake
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

#food of the snake
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

#score
score = 0
High_score = 0
game_over = False

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

def go_up():
    if head.direction != "Down":
        head.direction = "Up"

def go_down():
    if head.direction != "Up":
        head.direction = "Down"

def go_left():
    if head.direction != "Right":
        head.direction = "Left"

def go_right():
    if head.direction != "Left":
        head.direction = "Right"

def move():
    if head.direction == "Up":
        head.sety(head.ycor() + 20)
    if head.direction == "Down":
        head.sety(head.ycor() - 20)
    if head.direction == "Left":
        head.setx(head.xcor() - 20)
    if head.direction == "Right":
        head.setx(head.xcor() + 20)
    
# reset game 
def reset_game():
    global score, game_over
    head.goto(0, 0)
    head.direction = "Stop"
    head.showturtle()
    food.goto(0, 100)
    food.showturtle()
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    score = 0
    pen.clear()
    pen.goto(0, 260)
    pen.write("Score: {}  High Score: {}".format(score, High_score),
              align="center", font=("Courier", 24, "normal"))
    game_over = False
    n.listen()
    game_loop()

def end_game():
    global game_over
    game_over = True
    game_over_sound.play()
    head.hideturtle()
    food.hideturtle()
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    pen.clear()
    pen.goto(0, 0)
    pen.write("Game Over! Score: {}  High: {}".format(score, High_score),
              align="center", font=("Courier", 24, "normal"))
    n.update()
    n.ontimer(ask_replay, 700)

def ask_replay():
    choice = n.textinput("Game Over", "Play Again? (y/n):")
    if choice and choice.strip().lower() == "y":
        reset_game()
    else:
        pen.clear()
        pen.goto(0, -50)
        pen.write("Thanks for playing!", align="center", font=("Courier", 24, "normal"))
        n.update()
#main game loop
def game_loop():
    global score, High_score, game_over

    if game_over:
        return
    
    #border collision
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        end_game()
        return
    #collision with food 
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        eat_sound.play()
        score += 10
        if score > High_score:
            High_score = score
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, High_score),
                  align="center", font=("Courier", 24, "normal"))
        
        #Adding new segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    for segment in segments:
        if segment.distance(head) < 20:
            end_game()
            return

    n.update()
    n.ontimer(game_loop, 100)
#keyboard binding 
n.listen()
n.onkeypress(go_up, "Up")
n.onkeypress(go_down, "Down")
n.onkeypress(go_left, "Left")
n.onkeypress(go_right, "Right")

game_loop()
n.mainloop()