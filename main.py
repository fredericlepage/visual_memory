import pygame
import sys
import time
import random
import math

# Dimensions constants
SIZE = WIDTH, HEIGHT = 800, 600
GRID_LENGTH = min(HEIGHT * 0.85 , WIDTH)
HEIGHT_SPACE = HEIGHT - GRID_LENGTH
WIDTH_SPACE = WIDTH - GRID_LENGTH

# Color constants
WHITE = 255,255,255
BLACK = 0,70,118
LIGHT_BLUE = 0,150,255
DARK_BLUE = 0,120,205
PURPLE = 48,25,52

# Game settings constants
STARTING_LEVEL = 1
INITIAL_LIVES = 3
DELAY = 1000
ALLOWED_MISTAKES = 2

# Global variables
level = STARTING_LEVEL
lives = INITIAL_LIVES
mistakes = 0
grid_size = 0
lost = False

def main():

    pygame.init()   # Initialize pygame
    screen = pygame.display.set_mode(SIZE)    # Create the screen
    pygame.display.set_caption("Visual Memory")     # Set the window title

    pygame.key.set_repeat(250,125)

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

            if event.type == pygame.QUIT:
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
    global grid_size
    global lost

    grid_size = 0       # Set grid_size back to zero so that get_difficulty()
                        # can calculate it back from the initial level
    lost = False        # New game is started, so reset the lost variable

    while True:
        screen.fill(LIGHT_BLUE)     # Fill the screen background
        print_top_text(screen)      # Show "level" in the top of the screen
        show_lives(screen)          # Show remaining lives in the top of the screen

        # Determine grid size and number of flashing squares according to the level
        num_flash_squares = get_difficulty()
        grid = [[0 for x in range(grid_size)] for y in range(grid_size)] # Generate grid from grid size

        # Initialize the empty grid
        clear_grid(screen)
        time.sleep(1.5)

        # Randomly determine which squares will flash on the grid
        generate_flash_squares(grid, num_flash_squares)

        # Draw the grid with the flashing squares
        rectangles = draw_grid(screen, grid)
        time.sleep(DELAY / 1000)  # DELAY / 1000 to convert milliseconds in seconds

        # Go back to showing an empty grid on the screen
        clear_grid(screen)

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
                    print_level_settings(surface, WHITE, PURPLE)
                if delay_rect.collidepoint(pygame.mouse.get_pos()):
                    delay_setting_active = True
                    print_delay_settings(surface, DARK_BLUE, WHITE)
                else:
                    delay_setting_active = False
                    print_delay_settings(surface, WHITE, PURPLE)
                if lives_rect.collidepoint(pygame.mouse.get_pos()):
                    lives_setting_active = True
                    print_lives_settings(surface, DARK_BLUE, WHITE)
                else:
                    lives_setting_active = False
                    print_lives_settings(surface, WHITE, PURPLE)
                if mistakes_rect.collidepoint(pygame.mouse.get_pos()):
                    mistakes_setting_active = True
                    print_mistakes_settings(surface, DARK_BLUE, WHITE)
                else:
                    mistakes_setting_active = False
                    print_mistakes_settings(surface, WHITE, PURPLE)
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
                        if INITIAL_LIVES < 4:
                            INITIAL_LIVES += 1
                        print_all_settings(surface)
                        print_lives_settings(surface, DARK_BLUE, WHITE)
                        lives = INITIAL_LIVES
                    if mistakes_setting_active:
                        if ALLOWED_MISTAKES < 3:
                            ALLOWED_MISTAKES += 1
                        print_all_settings(surface)
                        print_mistakes_settings(surface, DARK_BLUE, WHITE)

                if event.key == pygame.K_DOWN:
                    if level_setting_active:
                        if STARTING_LEVEL > 1:
                            STARTING_LEVEL -= 1
                        print_all_settings(surface)
                        print_level_settings(surface, DARK_BLUE, WHITE)
                        level = STARTING_LEVEL
                    if delay_setting_active:
                        if DELAY > 50:
                            DELAY -= 50
                        print_all_settings(surface)
                        print_delay_settings(surface, DARK_BLUE, WHITE)
                    if lives_setting_active:
                        if INITIAL_LIVES > 1:
                            INITIAL_LIVES -= 1
                        print_all_settings(surface)
                        print_lives_settings(surface, DARK_BLUE, WHITE)
                        lives = INITIAL_LIVES
                    if mistakes_setting_active:
                        if ALLOWED_MISTAKES > 0:
                            ALLOWED_MISTAKES -= 1
                        print_all_settings(surface)
                        print_mistakes_settings(surface, DARK_BLUE, WHITE)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    pygame.display.flip()

def print_all_settings(surface):
    """
    Print the text and buttons of the settings menu
    """

    surface.fill(PURPLE)     # Fill the screen background

    font = pygame.font.Font("freesansbold.ttf", 70)
    settings_text = font.render("Settings", True, WHITE, PURPLE)
    settings_rect = settings_text.get_rect()
    settings_rect.left = WIDTH // 10
    settings_rect.centery = HEIGHT // 5
    surface.blit(settings_text, settings_rect)

    level_rect = print_level_settings(surface, WHITE, PURPLE)
    delay_rect = print_delay_settings(surface, WHITE, PURPLE)
    lives_rect = print_lives_settings(surface, WHITE, PURPLE)
    mistakes_rect = print_mistakes_settings(surface, WHITE, PURPLE)
    menu_rect = print_back_to_menu(surface, WHITE, PURPLE)

    return level_rect, delay_rect, lives_rect, mistakes_rect, menu_rect

def print_level_settings(surface, fg_color, bg_color):
    # Print the "Initial level" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    level_text = font.render("Initial level: " + str(STARTING_LEVEL), True, fg_color, bg_color)
    level_rect = level_text.get_rect()
    level_rect.left = WIDTH // 10
    level_rect.centery = (HEIGHT // 2) - 65
    surface.blit(level_text, level_rect)

    pygame.display.flip()
    return level_rect

def print_delay_settings(surface, fg_color, bg_color):
    # Print the "Flashing Delay" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    delay_text = font.render("Flashing delay: " + str(DELAY), True, fg_color, bg_color)
    delay_rect = delay_text.get_rect()
    delay_rect.left = WIDTH // 10
    delay_rect.centery= HEIGHT // 2
    surface.blit(delay_text, delay_rect)

    pygame.display.flip()
    return delay_rect

def print_lives_settings(surface, fg_color, bg_color):
    # Print the "Initial lives" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    lives_text = font.render("Initial lives: " + str(INITIAL_LIVES), True, fg_color, bg_color)
    lives_rect = lives_text.get_rect()
    lives_rect.left = WIDTH // 10
    lives_rect.centery= (HEIGHT // 2) + 65
    surface.blit(lives_text, lives_rect)

    pygame.display.flip()
    return lives_rect

def print_mistakes_settings(surface, fg_color, bg_color):
    # Print the "Allowed mistakes" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    mistakes_text = font.render("Allowed mistakes: " + str(ALLOWED_MISTAKES), True, fg_color, bg_color)
    mistakes_rect = mistakes_text.get_rect()
    mistakes_rect.left = WIDTH // 10
    mistakes_rect.centery= (HEIGHT // 2) + 130
    surface.blit(mistakes_text, mistakes_rect)

    pygame.display.flip()
    return mistakes_rect

def print_back_to_menu(surface, fg_color, bg_color):
    # Print the "Back to menu" button
    font = pygame.font.Font("freesansbold.ttf", 40)
    menu_text = font.render("Back to menu", True, fg_color, bg_color)
    menu_rect = menu_text.get_rect()
    menu_rect.right = WIDTH * 0.9
    menu_rect.centery= HEIGHT * 0.9
    surface.blit(menu_text, menu_rect)

    pygame.display.flip()
    return menu_rect

def draw_grid(surface, grid):
    """
    Draw the initial grid on the screen, with the flashing squares
    """
    rectangles = []
    block_size, margin = get_block_dimensions()
    for x in range(grid_size):
        for y in range(grid_size):
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

def clear_grid(surface):
    """
    Clear the white squares on the grid, so that the grid becomes composed of only
    blue squares
    """
    block_size, margin = get_block_dimensions()
    for x in range(grid_size):
        for y in range(grid_size):
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
    global lost

    if click_squares(rectangles, surface, grid, num_flash_squares):
        lost = False
        level += 1      # Increase the difficulty if the grid is successfully completed
        mistakes = 0    # Reset the mistake counter
    else:
        lost = True
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

            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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


def generate_flash_squares(grid, num_flash_squares):
    """
    Generate random x and y values where the squares on the grid will
    flash and disappear
    """
    i = 0
    while i < num_flash_squares:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        if grid[x][y] == 0:
            grid[x][y] = 1
            i += 1

def get_block_dimensions():
    """
    Determine the dimensions of the blocks that constitute the grid
    """
    margin = int(GRID_LENGTH // (40 + (7*grid_size)))
    block_size = (GRID_LENGTH - (grid_size - 1)*margin) / grid_size
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
    
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

    if level < 7:
        # Show image
        joe = pygame.image.load('src/images/joe.jpg')
        joe = pygame.transform.scale(joe, (150,150))
        surface.blit(joe, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        joe_text = font.render("c'mon man", True, WHITE, LIGHT_BLUE)
        joe_rect = joe_text.get_rect()
        joe_rect.top = 183
        joe_rect.centerx = 692
        surface.blit(joe_text, joe_rect)

    elif level < 9:
        # Show image
        beetlejuice = pygame.image.load('src/images/lester.jpg')
        beetlejuice = pygame.transform.scale(beetlejuice, (150,150))
        surface.blit(beetlejuice, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        beetlejuice_text = font.render("smooth brain", True, WHITE, LIGHT_BLUE)
        beetlejuice_rect = beetlejuice_text.get_rect()
        beetlejuice_rect.top = 183
        beetlejuice_rect.centerx = 692
        surface.blit(beetlejuice_text, beetlejuice_rect)

    elif level < 11:
        # Show image
        white_claw = pygame.image.load('src/images/white_claw.jpg')
        white_claw = pygame.transform.scale(white_claw, (150,150))
        surface.blit(white_claw, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        gabe_text = font.render("drunk?", True, WHITE, LIGHT_BLUE)
        gabe_rect = gabe_text.get_rect()
        gabe_rect.top = 183
        gabe_rect.centerx = 692
        surface.blit(gabe_text, gabe_rect)

    elif level < 13:
        # Show image
        ben = pygame.image.load('src/images/ben.png')
        ben = pygame.transform.scale(ben, (150,150))
        surface.blit(ben, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        ben_text = font.render("mediocre", True, WHITE, LIGHT_BLUE)
        ben_rect = ben_text.get_rect()
        ben_rect.top = 183
        ben_rect.centerx = 692
        surface.blit(ben_text, ben_rect)

    elif level == 13:
        # Show image
        phil = pygame.image.load('src/images/phil.jpg')
        phil = pygame.transform.scale(phil, (150,150))
        surface.blit(phil, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        phil_text = font.render("average", True, WHITE, LIGHT_BLUE)
        phil_rect = phil_text.get_rect()
        phil_rect.top = 183
        phil_rect.centerx = 692
        surface.blit(phil_text, phil_rect)

    elif level < 16:
        # Show image
        monke = pygame.image.load('src/images/monke.jpg')
        monke = pygame.transform.scale(monke, (150,150))
        surface.blit(monke, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        monke_text = font.render("monke", True, WHITE, LIGHT_BLUE)
        monke_rect = monke_text.get_rect()
        monke_rect.top = 183
        monke_rect.centerx = 692
        surface.blit(monke_text, monke_rect)

    elif level < 18:
        # Show image
        chad = pygame.image.load('src/images/chad.jpeg')
        chad = pygame.transform.scale(chad, (150,150))
        surface.blit(chad, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        chad_text = font.render("High IQ", True, WHITE, LIGHT_BLUE)
        chad_rect = chad_text.get_rect()
        chad_rect.top = 183
        chad_rect.centerx = 692
        surface.blit(chad_text, chad_rect)

    elif level < 20:
        # Show image
        putin = pygame.image.load('src/images/putin.jpeg')
        putin = pygame.transform.scale(putin, (150,150))
        surface.blit(putin, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        putin_text = font.render("Wide IQ", True, WHITE, LIGHT_BLUE)
        putin_rect = putin_text.get_rect()
        putin_rect.top = 183
        putin_rect.centerx = 692
        surface.blit(putin_text, putin_rect)

    elif level > 19:
        # Show image
        poire = pygame.image.load('src/images/image.png')
        poire = pygame.transform.scale(poire, (150,150))
        surface.blit(poire, (617, 33))

        # Print text
        font = pygame.font.Font("freesansbold.ttf", 30)
        poire_text = font.render("genius", True, WHITE, LIGHT_BLUE)
        poire_rect = poire_text.get_rect()
        poire_rect.top = 183
        poire_rect.centerx = 692
        surface.blit(poire_text, poire_rect)

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

def get_difficulty():
    """
    Return the grid size nd th number of flashing square depending on
    the level achieved by the player
    """
    global grid_size

    num_flash_squares = level + 2

    if not lost:
        if grid_size:
            # If the current grid size is known, verify if
            # the grid size must be increased for the next level
            if isqrt((num_flash_squares)*3 + 1) or isqrt((num_flash_squares)*3 + 3):
                grid_size += 1

        else:
            # If there is no current grid size, find the grid size from
            # the number of flashing squares
            i = num_flash_squares
            while i > 0:
                if isqrt((i*3) + 1):
                    grid_size = int(math.sqrt((i * 3) + 1))
                    return num_flash_squares
                elif isqrt((i*3) + 3):
                    grid_size = int(math.sqrt((i * 3) + 3))
                    return num_flash_squares
                i -= 1

    return num_flash_squares


def isqrt(n):
    """
    return True if n is a perfect square
    return False if n is not a perfect square
    """
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2

    return x**2 == n

main()
pygame.quit()
sys.exit()
