import pygame
import sys
import time
import random

# Dimensions constants
SIZE = WIDTH, HEIGHT = 800, 600
GRID_LENGTH = min(HEIGHT * 0.85 , WIDTH)
HEIGHT_SPACE = HEIGHT - GRID_LENGTH
WIDTH_SPACE = WIDTH - GRID_LENGTH

# Game settings constants
STARTING_LEVEL = 1
INITIAL_LIVES = 1
DELAY = 1000
ALLOWED_MISTAKES = 2

# Color constants
WHITE = 255,255,255
BLACK = 0,0,0
LIGHT_BLUE = 0,150,255
DARK_BLUE = 0,120,205

# Global variables
level = STARTING_LEVEL
lives = INITIAL_LIVES
mistakes = 0
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

    pygame.init()   # Initialize pygame
    screen = pygame.display.set_mode(SIZE)    # Create the screen
    pygame.display.set_caption("Visual Memory")     # Set the window title

    clock = pygame.time.Clock()

    running = True
    while running:
        pygame_event_loop()
        menu(screen)
        clock.tick(60)

def pygame_event_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def menu(surface):
    """
    Main menu function, where the player can play the game, modify the
    settings, or quit the program.
    """
    play_rect, settings_rect, quit_rect = print_menu(surface)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    play_game(surface)
                if settings_rect.collidepoint(pygame.mouse.get_pos()):
                    settings(surface)
                if quit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

def print_menu(surface):
    """
    This function prints the menu text and buttons
    """

    surface.fill(LIGHT_BLUE)     # Fill the screen background

    # Print the title
    font = pygame.font.Font("freesansbold.ttf", 80)
    title_text = font.render("Visual Memory", True, WHITE, LIGHT_BLUE)
    title_rect = title_text.get_rect()
    title_rect.center = (WIDTH // 2, HEIGHT // 4)
    surface.blit(title_text, title_rect)

    # Print the "play" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    play_text = font.render("Play", True, DARK_BLUE, WHITE)
    play_rect = play_text.get_rect()
    play_rect.center = (WIDTH // 2, HEIGHT // 2)
    surface.blit(play_text, play_rect)

    # Print the "settings" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    settings_text = font.render("Settings", True, DARK_BLUE, WHITE)
    settings_rect = settings_text.get_rect()
    settings_rect.center = (WIDTH // 2, (HEIGHT // 2) + 65)
    surface.blit(settings_text, settings_rect)

    # Print the "quit" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    quit_text = font.render("Quit", True, DARK_BLUE, WHITE)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (WIDTH // 2, (HEIGHT // 2) + 130)
    surface.blit(quit_text, quit_rect)

    pygame.display.flip()

    return play_rect, settings_rect, quit_rect

def play_game(screen):
    """
    Main game loop that is run when the player starts a new game,
    either from the main menu or the end screen
    """
    while True:
        screen.fill(LIGHT_BLUE)     # Fill the screen background
        print_top_text(screen)      # Show "level" in the top of the screen
        show_lives(screen)          # Show remaining lives in the top of the screen

        # Determine grid size and number of flashing squares according to the level
        grid_size, num_flash_squares = difficulty_settings[level]
        grid = [[0 for x in range(grid_size)] for y in range(grid_size)] # Generate grid from grid size

        # Initialize the empty grid
        clear_grid(screen, grid_size)
        time.sleep(1.5)

        # Randomly determine which squares will flash on the grid
        generate_flash_squares(grid, grid_size, num_flash_squares)

        # Draw the grid with the flashing squares
        rectangles = draw_grid(screen, grid, grid_size)
        time.sleep(DELAY / 1000)  # DELAY / 1000 to convert milliseconds in seconds

        # Go back to showing an empty grid on the screen
        clear_grid(screen, grid_size)

        # Let the player attempt to click the squares
        end_of_level(rectangles, screen, grid, num_flash_squares)

def settings(surface):

    # Constants
    global STARTING_LEVEL
    global DELAY
    global INITIAL_LIVES
    global ALLOWED_MISTAKES

    # Variables
    global level
    global lives
    global mistakes

    level_rect, delay_rect, lives_rect, mistakes_rect, menu_rect = print_all_settings(surface)

    level_setting_active = False
    delay_setting_active = False
    lives_setting_active = False
    mistakes_setting_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if level_rect.collidepoint(pygame.mouse.get_pos()):
                    level_setting_active = True
                    print_level_settings(surface, DARK_BLUE, WHITE)
                else:
                    level_setting_active = False
                    print_level_settings(surface, WHITE, LIGHT_BLUE)
                if delay_rect.collidepoint(pygame.mouse.get_pos()):
                    delay_setting_active = True
                    print_delay_settings(surface, DARK_BLUE, WHITE)
                else:
                    delay_setting_active = False
                    print_delay_settings(surface, WHITE, LIGHT_BLUE)
                if lives_rect.collidepoint(pygame.mouse.get_pos()):
                    lives_setting_active = True
                    print_lives_settings(surface, DARK_BLUE, WHITE)
                else:
                    lives_setting_active = False
                    print_lives_settings(surface, WHITE, LIGHT_BLUE)
                if mistakes_rect.collidepoint(pygame.mouse.get_pos()):
                    mistakes_setting_active = True
                    print_mistakes_settings(surface, DARK_BLUE, WHITE)
                else:
                    mistakes_setting_active = False
                    print_mistakes_settings(surface, WHITE, LIGHT_BLUE)
                if menu_rect.collidepoint(pygame.mouse.get_pos()):
                    menu(surface)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if level_setting_active:
                        STARTING_LEVEL += 1
                        print_all_settings(surface)
                        print_level_settings(surface, DARK_BLUE, WHITE)
                        level = STARTING_LEVEL
                    if delay_setting_active:
                        DELAY += 50
                        print_all_settings(surface)
                        print_delay_settings(surface, DARK_BLUE, WHITE)
                    if lives_setting_active:
                        INITIAL_LIVES += 1
                        print_all_settings(surface)
                        print_lives_settings(surface, DARK_BLUE, WHITE)
                        lives = INITIAL_LIVES
                    if mistakes_setting_active:
                        ALLOWED_MISTAKES += 1
                        print_all_settings(surface)
                        print_mistakes_settings(surface, DARK_BLUE, WHITE)

                if event.key == pygame.K_DOWN:
                    if level_setting_active:
                        STARTING_LEVEL -= 1
                        print_all_settings(surface)
                        print_level_settings(surface, DARK_BLUE, WHITE)
                        level = STARTING_LEVEL
                    if delay_setting_active:
                        DELAY -= 50
                        print_all_settings(surface)
                        print_delay_settings(surface, DARK_BLUE, WHITE)
                    if lives_setting_active:
                        INITIAL_LIVES -= 1
                        print_all_settings(surface)
                        print_lives_settings(surface, DARK_BLUE, WHITE)
                        lives = INITIAL_LIVES
                    if mistakes_setting_active:
                        ALLOWED_MISTAKES -= 1
                        print_all_settings(surface)
                        print_mistakes_settings(surface, DARK_BLUE, WHITE)

    pygame.display.flip()

def print_all_settings(surface):
    """
    Print the text and buttons of the settings menu
    """

    surface.fill(LIGHT_BLUE)     # Fill the screen background

    font = pygame.font.Font("freesansbold.ttf", 80)
    settings_text = font.render("Settings", True, WHITE, LIGHT_BLUE)
    settings_rect = settings_text.get_rect()
    settings_rect.center = (WIDTH // 2, HEIGHT // 4)
    surface.blit(settings_text, settings_rect)

    level_rect = print_level_settings(surface, WHITE, LIGHT_BLUE)
    delay_rect = print_delay_settings(surface, WHITE, LIGHT_BLUE)
    lives_rect = print_lives_settings(surface, WHITE, LIGHT_BLUE)
    mistakes_rect = print_mistakes_settings(surface, WHITE, LIGHT_BLUE)
    menu_rect = print_back_to_menu(surface, WHITE, LIGHT_BLUE)

    return level_rect, delay_rect, lives_rect, mistakes_rect, menu_rect

def print_level_settings(surface, fg_color, bg_color):
    # Print the "Initial level" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    level_text = font.render("Initial level: " + str(STARTING_LEVEL), True, fg_color, bg_color)
    level_rect = level_text.get_rect()
    level_rect.center = (WIDTH // 2, HEIGHT // 2)
    surface.blit(level_text, level_rect)

    pygame.display.flip()
    return level_rect

def print_delay_settings(surface, fg_color, bg_color):
    # Print the "Flashing Delay" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    delay_text = font.render("Flashing delay: " + str(DELAY), True, fg_color, bg_color)
    delay_rect = delay_text.get_rect()
    delay_rect.center = (WIDTH // 2, (HEIGHT // 2) + 65)
    surface.blit(delay_text, delay_rect)

    pygame.display.flip()
    return delay_rect

def print_lives_settings(surface, fg_color, bg_color):
    # Print the "Initial lives" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    lives_text = font.render("Initial lives: " + str(INITIAL_LIVES), True, fg_color, bg_color)
    lives_rect = lives_text.get_rect()
    lives_rect.center = (WIDTH // 2, (HEIGHT // 2) + 130)
    surface.blit(lives_text, lives_rect)

    pygame.display.flip()
    return lives_rect

def print_mistakes_settings(surface, fg_color, bg_color):
    # Print the "Allowed mistakes" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    mistakes_text = font.render("Allowed mistakes: " + str(ALLOWED_MISTAKES), True, fg_color, bg_color)
    mistakes_rect = mistakes_text.get_rect()
    mistakes_rect.center = (WIDTH // 2, (HEIGHT // 2) + 195)
    surface.blit(mistakes_text, mistakes_rect)

    pygame.display.flip()
    return mistakes_rect

def print_back_to_menu(surface, fg_color, bg_color):
    # Print the "Back to menu" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    menu_text = font.render("Back to menu", True, fg_color, bg_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WIDTH // 2, (HEIGHT // 2) + 260)
    surface.blit(menu_text, menu_rect)

    pygame.display.flip()
    return menu_rect

def draw_grid(surface, grid, grid_dimension):
    """
    Draw the initial grid on the screen, with the flashing squares
    """
    rectangles = []
    block_size, margin = get_block_dimensions(grid_dimension)
    for x in range(grid_dimension):
        for y in range(grid_dimension):
            rect = pygame.Rect(x*block_size + x*margin + WIDTH_SPACE // 2,
                            y*block_size + y*margin + HEIGHT_SPACE * 0.9,
                            block_size, block_size)
            rectangles.append([rect, [x,y]])

            if grid[x][y] == 0:
                color = DARK_BLUE
            elif grid[x][y] == 1:
                color = WHITE
            pygame.draw.rect(surface, color, rect)

    pygame.display.flip()
    return rectangles

def clear_grid(surface, grid_dimension):
    """
    Clear the white squares on the grid, so that the grid becomes composed of only
    blue squares
    """
    block_size, margin = get_block_dimensions(grid_dimension)
    for x in range(grid_dimension):
        for y in range(grid_dimension):
            rect = pygame.Rect(x*block_size + x*margin + WIDTH_SPACE // 2,
                            y*block_size + y*margin + HEIGHT_SPACE*0.9,
                            block_size, block_size)
            pygame.draw.rect(surface, DARK_BLUE, rect)
    pygame.display.flip()

def end_of_level(rectangles, surface, grid, num_flash_squares):
    """
    - If the player clicks all the square, level up
    - If not, the player loses a life
    - When no lives are left, the game restarts
    """
    global level
    global lives
    global mistakes

    if click_squares(rectangles, surface, grid, num_flash_squares):
        level += 1      # Increase the difficulty if the grid is successfully completed
        mistakes = 0    # Reset the mistake counter
    else:
        lives -= 1      # Decrease the lives of the player in case of failure
        mistakes = 0    # Reset the mistake counter
    time.sleep(.25)

    if lives < 1:
        end_screen(surface)

def click_squares(rectangles, surface, grid, num_flash_squares):
    """
    The user must now click the squares that previously flashed
    """
    global mistakes

    i = 0
    while i < num_flash_squares:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect in rectangles:
                    if rect[0].collidepoint(pygame.mouse.get_pos()):
                        state = change_color(surface, grid, rect[0], rect[1][0], rect[1][1])
                        if state == 1:   # If player clicked on a correct square
                            i += 1
                        elif state == 0:     # If player clicked on the wrong square
                            mistakes += 1
                            if mistakes > ALLOWED_MISTAKES:
                                pygame.display.flip()
                                return False    # Return False if player failed

        pygame.display.flip()


    return True     # Return True if player clicks all the flashed squares

def change_color(surface, grid, rect, x, y):
    """
    Change the color of a square that was clicked
    """
    if grid[x][y] == 0:
        pygame.draw.rect(surface, BLACK, rect)
        grid[x][y] = 2
        return 0    # Return 0 if player clicks the wrong square

    elif grid[x][y] == 1:
        pygame.draw.rect(surface, WHITE, rect)
        grid[x][y] = 2
        return 1     # Return 1 if the player clicks the right square


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
    """
    Determine the dimensions of the blocks that constitute the grid
    """
    margin = int(GRID_LENGTH // 80)
    block_size = (GRID_LENGTH - (grid_dimension - 1)*margin) / grid_dimension
    return block_size, margin

def end_screen(surface):
    """
    End screen when the player has no lives left
    """

    global lives
    global level

    # Print the end screen text and return the button rectangles variables
    play_again_rect, menu_rect = print_end_screen(surface)

    level = STARTING_LEVEL      # Reset the starting level
    lives = INITIAL_LIVES       # Reset the lives

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(pygame.mouse.get_pos()):
                    play_game(surface)
                if menu_rect.collidepoint(pygame.mouse.get_pos()):
                    menu(surface)

def print_end_screen(surface):
    """
    This function prints the end screen text and buttons
    """

    surface.fill(LIGHT_BLUE)     # Fill the screen background

    # Print the level achieved during the game
    font = pygame.font.Font("freesansbold.ttf", 81)
    level_text = font.render("Level " + str(level), True, WHITE, LIGHT_BLUE)
    level_rect = level_text.get_rect()
    level_rect.center = (WIDTH // 2, HEIGHT // 3)
    surface.blit(level_text, level_rect)

    # Print the "play again" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    play_again_text = font.render("Play again", True, DARK_BLUE, WHITE)
    play_again_rect = play_again_text.get_rect()
    play_again_rect.center = (WIDTH // 2, HEIGHT // 2)
    surface.blit(play_again_text, play_again_rect)

    # Print the "back to main menu" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    menu_text = font.render("Back to main menu", True, DARK_BLUE, WHITE)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WIDTH // 2, (HEIGHT // 2) + 65)
    surface.blit(menu_text, menu_rect)

    pygame.display.flip()

    return play_again_rect, menu_rect

def print_top_text(surface):
    font = pygame.font.Font("freesansbold.ttf", 40)
    top_text = font.render("Level " + str(level), True, WHITE, LIGHT_BLUE)
    top_rect = top_text.get_rect()
    top_rect.center = (WIDTH // 2, HEIGHT_SPACE // 2)
    surface.blit(top_text, top_rect)

def show_lives(surface):
    """
    Draw the circles that represent the player remaining lives
    """
    for i in range(lives):
        pygame.draw.circle(surface, DARK_BLUE, (int(WIDTH // 2) +
                        int(GRID_LENGTH // 2) - 18 - i * 42,
                        int(HEIGHT_SPACE // 2)), 18)

main()
pygame.quit()
