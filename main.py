import pygame
import sys
import time
import random

# Constants
SIZE = WIDTH, HEIGHT = 800, 600
WHITE = 255,255,255
BLACK = 0,0,0
LIGHT_BLUE = 0,150,255
DARK_BLUE = 0,120,205

# Global variables
level = 1
lives = 3
difficulty_settings = {1: [3, 3],
                    2: [3, 4],
                    3: [4, 5],
                    4: [4, 6],
                    5: [4, 7],
                    6: [5, 8],
                    7: [5, 9],
                    8: [5, 10],
                    9: [6, 11],
                    10: [6, 12],
                    11: [6, 13],
                    12: [6, 14],
                    13: [6, 15],
                    14: [7, 16],
                    15: [7, 17],
                    16: [7, 18],
                    17: [7, 19],
                    18: [7, 20],
                    19: [8, 21],
                    20: [8, 22],
                    21: [8, 23]
}

def main():
    global level
    global lives

    pygame.init()   # Initialize pygame
    screen = pygame.display.set_mode(SIZE)    # Create the screen
    pygame.display.set_caption("Visual Memory")     # Set the window title

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(LIGHT_BLUE)     # Fill the screen background

        # Determine grid size and number of flashing squares
        grid_size, num_flash_squares = get_difficulty()
        grid = [[0 for x in range(grid_size)] for y in range(grid_size)] # Generate grid from grid size

        # Randomly determine which squares will flash on the grid
        generate_flash_squares(grid, grid_size, num_flash_squares)

        # Draw the grid with the flashing squares
        rectangles = draw_grid(screen, grid, grid_size)
        pygame.display.flip()
        time.sleep(.2)

        # Go back to showing an empty grid on the screen
        clear_grid(screen, grid_size)
        pygame.display.flip()

        # Let the user attempt to click the square that previously flashed
        if click_squares(rectangles, screen, grid, num_flash_squares):
            level += 1      # Increase the difficulty if the grid is successfully completed
        else:
            lives -= 1      # Decrease the lives of the player in case of failure
        time.sleep(.5)

        clear_grid(screen, grid_size)
        pygame.display.flip()
        time.sleep(1.5)

        if lives == 0:
            restart_game()

def get_difficulty():
    """
    Return the grid size and the number of flashing squares depending on
    the level achieved by the player
    """
    global level
    global difficulty_settings

    return difficulty_settings[level]

def restart_game():
    """
    Restart the game if the player has no lives left
    """
    global lives
    global level
    level = 1
    lives = 3


def draw_grid(surface, grid, grid_dimension):
    """
    Draw the initial grid on the screen, with the flashing squares
    """
    rectangles = []
    block_size, margin = get_block_dimensions(grid_dimension)
    for x in range(grid_dimension):
        for y in range(grid_dimension):
            rect = pygame.Rect(x*block_size + x*margin, y*block_size + y*margin, block_size, block_size)
            rectangles.append([rect, [x,y]])

            if grid[x][y] == 0:
                color = DARK_BLUE
            elif grid[x][y] == 1:
                color = WHITE
            pygame.draw.rect(surface, color, rect)

    return rectangles

def clear_grid(surface, grid_dimension):
    """
    Clear the white squares on the grid, so that the grid becomes composed of only
    blue squares
    """
    block_size, margin = get_block_dimensions(grid_dimension)
    for x in range(grid_dimension):
        for y in range(grid_dimension):
            rect = pygame.Rect(x*block_size + x*margin, y*block_size + y*margin, block_size, block_size)
            pygame.draw.rect(surface, DARK_BLUE, rect)

def click_squares(rectangles, surface, grid, num_flash_squares):
    """
    The user must now click the squares that previously flashed and disappeared
    """
    i = 0
    while i < num_flash_squares:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in rectangles:
                    if rect[0].collidepoint(pygame.mouse.get_pos()):
                        state = change_color(surface, grid, rect[0], rect[1][0], rect[1][1])
                        if state:
                            i += 1
                        elif not state:
                            return False    # Return False if player failed

    return True     # Return True if player clicks all the flashed squares

def change_color(surface, grid, rect, x, y):
    """
    Change the color of a square that was clicked
    """
    if grid[x][y] == 0:
        pygame.draw.rect(surface, BLACK, rect)
        pygame.display.flip()
        return False    # Return False if player clicks the wrong square

    elif grid[x][y] == 1:
        pygame.draw.rect(surface, WHITE, rect)
        pygame.display.flip()
        return True     # Return True if the player clicks the right square


def generate_flash_squares(grid, grid_dimension, num_flash_squares):
    """
    Generate random x and y values where the squares on the grid will
    flash and disappear
    """
    i = 0
    while i < num_flash_squares:
        x = random.randint(0, grid_dimension - 1)
        y = random.randint(0, grid_dimension - 1)
        if grid[x][y] == 0:
            grid[x][y] = 1
            i += 1

def get_block_dimensions(grid_dimension):
    margin = 7
    block_size = (HEIGHT - (grid_dimension - 1)*margin) / grid_dimension
    return block_size, margin

main()
pygame.quit()
