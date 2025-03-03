# This is my simple snake game with difficulty selector and game over message and arrow key controls for movement

import turtle 
import time 
import random

# Global variables
delay = 0.1  # Default delay, will be set by difficulty
score = 0
high_score = 0
game_started = False  # Flag to track if game has started

# Main startup screen 
wn = turtle.Screen()
wn.title("Snake Game v1 by Joshua C")
wn.bgcolor("white")
wn.setup(width=600, height=600)
wn.tracer(0) # Turns off screen updates 

# Snake's head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food 
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Game over message turtle
game_over = turtle.Turtle()
game_over.speed(0)
game_over.penup()
game_over.hideturtle()
game_over.goto(0, -250)  # Position at bottom of screen

# Difficulty selector turtles
easy = turtle.Turtle()
medium = turtle.Turtle()
hard = turtle.Turtle()

# Function to setup or reset difficulty selector
def setup_difficulty_selector():
    # Clear game over message when resetting
    game_over.clear()
    # Easy
    easy.clear()  # Clear any previous text
    easy.speed(0)
    easy.penup()
    easy.goto(-148, 0)  # 2-character spacing (~48px between options)
    easy.write("Easy", align="center", font=("Courier", 24, "normal"))
    easy.onclick(lambda x, y: set_difficulty("easy"))
    easy.showturtle()
    
    # Medium
    medium.clear()
    medium.speed(0)
    medium.penup()
    medium.goto(0, 0)  # Center stays at 0
    medium.write("Medium", align="center", font=("Courier", 24, "normal"))
    medium.onclick(lambda x, y: set_difficulty("medium"))
    medium.showturtle()
    
    # Hard
    hard.clear()
    hard.speed(0)
    hard.penup()
    hard.goto(148, 0)  # 2-character spacing
    hard.write("Hard", align="center", font=("Courier", 24, "normal"))
    hard.onclick(lambda x, y: set_difficulty("hard"))
    hard.showturtle()

# Function to set difficulty and start game
def set_difficulty(difficulty):
    global delay, game_started
    if difficulty == "easy":
        delay = 0.15
    elif difficulty == "medium":
        delay = 0.1
    elif difficulty == "hard":
        delay = 0.05
    game_started = True
    # Hide difficulty options and clear text
    easy.hideturtle()
    easy.clear()
    medium.hideturtle()
    medium.clear()
    hard.hideturtle()
    hard.clear()
    start_game()

# Movement functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right": 
        x = head.xcor()
        head.setx(x + 20)

# Keybindings
wn.listen()
wn.onkeypress(go_up, "w" or "Up")
wn.onkeypress(go_down, "s" or "Down")
wn.onkeypress(go_left, "a" or "Left")
wn.onkeypress(go_right, "d" or "Right")

# Main game function
def start_game():
    global score, high_score, delay, segments, game_started
    while game_started:
        wn.update()

        # Check for collision with border
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = delay  # Keep the selected difficulty
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
            # Clear difficulty text and show game over
            easy.clear()
            medium.clear()
            hard.clear()
            game_over.clear()  # Clear any previous message
            game_over.write("Game Over", align="center", font=("Courier", 24, "normal"))
            wn.update()  # Force screen update to show "Game Over"
            time.sleep(1)  # Delay to make "Game Over" visible
            game_started = False  # End game
            setup_difficulty_selector()  # Show difficulty options again

        # Check for collision with food
        if head.distance(food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("green")
            new_segment.penup()
            segments.append(new_segment)
            delay -= 0.001  # Still increases speed as you eat
            score += 10
            if score > high_score:
                high_score = score
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Move segments
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for collision with body
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                score = 0
                delay = delay  # Keep the selected difficulty
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
                # Clear difficulty text and show game over
                easy.clear()
                medium.clear()
                hard.clear()
                game_over.clear()  # Clear any previous message
                game_over.write("Game Over", align="center", font=("Courier", 24, "normal"))
                wn.update()  # Force screen update to show "Game Over"
                time.sleep(1)  # Delay to make "Game Over" visible
                game_started = False  # End game
                setup_difficulty_selector()  # Show difficulty options again

        time.sleep(delay)

# Setup difficulty selector initially
setup_difficulty_selector()

# Keep window open until difficulty is chosen and during game
while True:
    wn.update()
    if not game_started:
        wn.update()  # Keep screen responsive while waiting for difficulty choice
