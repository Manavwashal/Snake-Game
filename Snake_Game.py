from tkinter import *   # type:ignore
import random
import pygame

# Initialize pygame for sound
pygame.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("D:\Python Developer\Python Programs\Sounds\eating-sound-effect-36186.mp3")
game_over_sound = pygame.mixer.Sound("D:\Python Developer\Python Programs\Sounds\game-over-80141.mp3")
special_food_sound = pygame.mixer.Sound("D:\Python Developer\Python Programs\Sounds\game-bonus-144751.mp3")



# Initialising Dimensions of Game
WIDTH = 500
HEIGHT = 500
SPEED = 200
SPACE_SIZE = 20
BODY_SIZE = 2
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FFFFFF"
BACKGROUND = "#000000"
SPECIAL_FOOD_COLOR = "#FFD700"
BORDER_COLOR = "#FF6347"

class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, outline="#ADFF2F", width=2, tag="snake") 
            self.squares.append(square)

class Food:
    def __init__(self, special=False):
        self.special = special
        color = SPECIAL_FOOD_COLOR if self.special else FOOD_COLOR
        x = random.randint(0, int(WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(HEIGHT / SPACE_SIZE) + 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="food") 

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y += SPACE_SIZE
    elif direction == "down":
        y -= SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, outline="#ADFF2F", width=2, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, SPEED

        score += 10 if food.special else 1
        SPEED -= 2  # Increase speed as score increases

        label.config(text="Points: {} | High Score: {}".format(score, high_score))

        canvas.delete("food")

        if food.special:
            pygame.mixer.Sound.play(special_food_sound)
        else:
            pygame.mixer.Sound.play(eat_sound)

        if random.randint(1, 10) > 8:  # Randomly add special food
            food = Food(special=True)
        else:
            food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    global high_score, score

    pygame.mixer.Sound.play(game_over_sound)

    if score > high_score:
        high_score = score
        label.config(text="Points: {} | High Score: {}".format(score, high_score))

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70),
                       text="GAME OVER", fill="red", tag="gameover") # type: ignore

# Initialize the main window
window = Tk()
window.title("Snake Game")

score = 0
high_score = 0
direction = 'down'

# Display of Points Scored in Game
label = Label(window, text="Points: 0 | High Score: 0", font=('consolas', 20))
label.pack()

# Creating the Canvas for the game
canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
canvas.pack()

# Center the window on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Binding keys to control the snake's direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Creating a snake and food object to start the game
snake = Snake()
food = Food()

next_turn(snake, food)

# Running the game loop
window.mainloop()

# End of code