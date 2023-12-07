import os
import random
import ctypes
import sys
import time
import keyboard
from PIL import Image, ImageDraw

# Constants
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)
CELL_SIZE = 50

# Calculate the number of rows and columns for the game grid
Row_Count, Col_Count = screen_height // CELL_SIZE, screen_width // CELL_SIZE
x_offset = Row_Count // 2
y_offset = Col_Count // 2

# Define color constants
SNAKE_COLOR = (36, 224, 29)
BG_COLOR = (0, 0, 0)
FOOD_COLOR = (255, 0, 0)
END_COLOR = (252, 183, 3)

# Create the wallpaper image
image = Image.new('RGB', (screen_width, screen_height), BG_COLOR)
image.save('snakeeee.jpg')

def set_background(path):
    '''Sets the desktop background with the given image path.'''
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

def draw_rect(shape, img, color):
    '''Draws a rectangle on the image.'''
    new_image = ImageDraw.Draw(img)
    new_image.rectangle(shape, fill=color)

def new_grid():
    '''Creates an empty grid.'''
    return [[0 for _ in range(Col_Count)] for _ in range(Row_Count)]

def place_apple():
    '''Places apple randomly.'''
    while True:
        apple_pos = (random.randint(0, Row_Count - 1), random.randint(0, Col_Count - 1))
        if (apple_pos not in snake_body) and grid[apple_pos[0]][apple_pos[1]] != 1:
            break
    return apple_pos

def update(grid):
    global apple_pos, apple_eaten, snake_body, current_direction, image
    lost = False
    old_grid = grid
    grid = new_grid()
    # Move the snake
    for pos in snake_body:
        grid[pos[0]][pos[1]] = 1
        grid[apple_pos[0]][apple_pos[1]] = 2

    #Check if an apple has been eaten
    if snake_body[0] == apple_pos:
        apple_pos = place_apple()
        grid[snake_body[0][0]][snake_body[0][1]] = 1
        grid[apple_pos[0]][apple_pos[1]] = 2
        apple_eaten = True

    # Adjust the head position to loop around the edges 
    new_head = (snake_body[0][0] + DIRECTIONS[current_direction][0], snake_body[0][1] + DIRECTIONS[current_direction][1])
    new_head = (new_head[0] % Row_Count, new_head[1] % Col_Count)

    # Make snake longer if it has eaten an apple this frame
    snake_body.insert(0, new_head)
    if not apple_eaten:
        snake_body.pop()
    apple_eaten = False

    # End the game if snake collides with itself
    if snake_body[0] in snake_body[1:]: lost = True

    # Update the image based on the game grid
    for row in range(Row_Count):
        for col in range(Col_Count):
            if lost and grid[row][col] == 1:
                color = END_COLOR
                draw_rect(
                    (col * CELL_SIZE + x_offset, row * CELL_SIZE + y_offset, (col + 1) * CELL_SIZE + x_offset,
                     (row + 1) * CELL_SIZE + y_offset), image, color)
            elif grid[row][col] != old_grid[row][col]:
                if grid[row][col] == 1:
                    color = SNAKE_COLOR
                elif grid[row][col] == 2:
                    color = FOOD_COLOR
                else:
                    color = BG_COLOR
                draw_rect(
                    (col * CELL_SIZE + x_offset, row * CELL_SIZE + y_offset, (col + 1) * CELL_SIZE + x_offset,
                     (row + 1) * CELL_SIZE + y_offset), image, color)

    # Set the image as the desktop background
    image.save('snakeeee.jpg')
    set_background(os.path.abspath('snakeeee.jpg'))

    if lost:
        sys.exit()
    return grid

# Initialize snake_body, DIRECTIONS, and current_direction
snake_body = [(5, 6), (5, 7)]
DIRECTIONS = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
current_direction = 'right'

set_background(os.path.abspath('snakeeee.jpg'))

grid = new_grid()
start = False
update_interval = 0.25
last_update_time = time.time()

apple_pos = place_apple()
apple_eaten = False

while True:
    #wait for the player to press 'enter'
    if not start:
        if keyboard.is_pressed('enter'):
            start = True

    #Keyboard input
    if start:
        if keyboard.is_pressed('right') and current_direction != 'left':
            current_direction = 'right'
        if keyboard.is_pressed('left') and current_direction != 'right':
            current_direction = 'left'
        if keyboard.is_pressed('up') and current_direction != 'down':
            current_direction = 'up'
        if keyboard.is_pressed('down') and current_direction != 'up':
            current_direction = 'down'

        # Update the game at regular intervals
        current_time = time.time()
        if current_time - last_update_time >= update_interval:
            grid = update(grid)
            last_update_time = current_time
