import pygame
from pygame.locals import *
import random

pygame.init()
screen_width = 800
screen_height = 600
HALF_WIDTH = screen_width // 2
HALF_HEİGHT = screen_height // 2
screen = pygame.display.set_mode((screen_width, (screen_height+21)))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
# define font
font = pygame.font.SysFont(None, 40)

# setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# define snake variables

snake_pos_1 = [(HALF_WIDTH), screen_height // 2]
snake_pos_2 = [(HALF_WIDTH), screen_height // 2]

snake_rev_pos_1 = [(HALF_WIDTH ), screen_height // 2]
snake_rev_pos_2 = [(HALF_WIDTH ), screen_height // 2]

snake_pos = [snake_pos_1, snake_pos_2]

snake_reverse_pos = [snake_rev_pos_1, snake_rev_pos_2]
snake_reverse_pos.reverse()

direction = 4  # 1 is up, 2 is right, 3 is down, 4 is left

# define game variables
cell_size = 10
update_snake = 0
food = [0, 0]
food2= [0,0]
new_food = True
new_piece = [0, 0]
game_over = False
clicked = False
score = 0

# define colors
wall_col = (220, 220, 220)
bg = (0, 0, 0)
body_inner =(64, 255, 64)   # Gövde içi
body_outer =  (32, 200, 32) # snake gövde çevresi
#food_col = (200, 50, 50)
red = (200, 0, 0)
green = (55, 55, 55)

# directions
DIRECTION_UP = 1
DIRECTION_RIGHT = 2
DIRECTION_LEFT = 4
DIRECTION_DOWN = 3


def draw_screen():
    screen.fill(bg)


def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, wall_col)
    screen.blit(score_img, (2, 2))


def check_game_over(game_over):
    # first check is to see if the snake has eaten itself by checking if the head has clashed with the rest of the body
    head_count = 0
    for i in range(0, len(snake_pos)):
        if (snake_pos[0] == snake_pos[i] and head_count > 0) or (snake_reverse_pos[0] == snake_reverse_pos[i] and head_count > 0):
            game_over = True
        head_count += 1

    # second check is to see if the snake has gone out of bounds
    snake_out = snake_pos[0][0] < 0 or snake_pos[0][0] > (screen_width/2) or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height
    reverse_snake_out = snake_reverse_pos[0][0] < 0 or snake_reverse_pos[0][0] < (screen_width/2) or snake_reverse_pos[0][1] < 0 or snake_reverse_pos[0][1] > screen_height

    if snake_out or reverse_snake_out:
        game_over = True

    return game_over


def draw_game_over():
    over_text = "Game Over!"
    over_img = font.render(over_text, True, green)
    pygame.draw.rect(screen, red, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, green)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


def change_direction(key):
    global direction

    if key == pygame.K_UP and direction != DIRECTION_DOWN:
        direction = DIRECTION_UP
    if key == pygame.K_RIGHT and direction != DIRECTION_LEFT:
        direction = DIRECTION_RIGHT
    if key == pygame.K_DOWN and direction != DIRECTION_UP:
        direction = DIRECTION_DOWN
    if key == pygame.K_LEFT and direction != DIRECTION_RIGHT:
        direction = DIRECTION_LEFT

run = True
while run:

    draw_screen()
    draw_score()
    pygame.draw.rect(screen, wall_col, (((screen_width/2)+10), 0, 10, screen_width))
    
    clock.tick(300)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            change_direction(event.key)
#superposition food
    foodcuk2=pygame.Rect(food2[0], food2[1], cell_size, cell_size)
    foodResim2 = pygame.image.load('Artboard1.png')
    screen.blit(foodResim2, foodcuk2)
    
    # create food
    if new_food:
        new_food = False

        food[0] = cell_size * random.randint((HALF_WIDTH+2) // cell_size, (screen_width // cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)
        food2[0] = cell_size * random.randint((HALF_WIDTH+2) // cell_size, (screen_width // cell_size) - 1)
        food2[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)

    # draw food
    #pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))
    foodcuk=pygame.Rect(food[0], food[1], cell_size, cell_size)
    foodResim = pygame.image.load('Artboard1.png')
    screen.blit(foodResim, foodcuk)


    # check if food has been eaten
    # 1 is up, 2 is right, 3 is down, 4 is left
    if snake_reverse_pos[0] == food:
        new_food = True
        # create a new piece at the last point of the snake's tail
        new_piece = list(snake_pos[-1])
        rev_new_piece = list(snake_reverse_pos[-1])
        # add an extra piece to the snake
        if direction == DIRECTION_UP:
            new_piece[1] += cell_size
            rev_new_piece[1] += cell_size
        # heading down
        if direction == DIRECTION_DOWN:
            new_piece[1] -= cell_size
            rev_new_piece[1] -= cell_size
        # heading right
        if direction == DIRECTION_RIGHT:
            new_piece[0] -= cell_size
            rev_new_piece[0] -= cell_size
        # heading left
        if direction == DIRECTION_LEFT:
            new_piece[0] += cell_size
            rev_new_piece[0] -= cell_size

        # attach new piece to the end of the snake
        snake_pos.append(new_piece)
        snake_reverse_pos.append(rev_new_piece)

        # increase score
        score += 1

    if game_over == False:
        # update snake
        if update_snake > 99:
            update_snake = 0
            # first shift the positions of each snake piece back.
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            snake_reverse_pos = snake_reverse_pos[-1:] + snake_reverse_pos[:-1]
            # now update the position of the head based on direction
            # heading up
            if direction == DIRECTION_UP:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
                snake_reverse_pos[0][0] = snake_reverse_pos[1][0]
                snake_reverse_pos[0][1] = snake_reverse_pos[1][1] + cell_size
            # heading down
            if direction == DIRECTION_DOWN:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
                snake_reverse_pos[0][0] = snake_reverse_pos[1][0]
                snake_reverse_pos[0][1] = snake_reverse_pos[1][1] - cell_size
            # heading right
            if direction == DIRECTION_RIGHT:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
                snake_reverse_pos[0][1] = snake_reverse_pos[1][1]
                snake_reverse_pos[0][0] = snake_reverse_pos[1][0] - cell_size
            # heading left
            if direction == DIRECTION_LEFT:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size
                snake_reverse_pos[0][1] = snake_reverse_pos[1][1]
                snake_reverse_pos[0][0] = snake_reverse_pos[1][0] + cell_size

            game_over = check_game_over(game_over)

    #true olduğunda
    if game_over:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            # reset variables
            game_over = False
            update_snake = 0
            food = [0, 0]
            new_food = True
            new_piece = [0, 0]
            # define snake variables
            snake_pos_1 = [(HALF_WIDTH), screen_height // 2]
            snake_pos_2 = [(HALF_WIDTH), screen_height // 2]

            snake_rev_pos_1 = [(HALF_WIDTH ), screen_height // 2]
            snake_rev_pos_2 = [(HALF_WIDTH ), screen_height // 2]
            snake_pos = [snake_pos_1, snake_pos_2, snake_pos_3]

            snake_reverse_pos = [snake_rev_pos_1, snake_rev_pos_2]
            snake_reverse_pos.reverse()
            direction = 4  # 1 is up, 2 is right, 3 is down, 4 is left
            score = 0

    head = 1
    for i in range(0, len(snake_pos)):

        if head == 0:
            # pygame.draw.rect(screen, body_outer, (snake_pos[i][0], snake_pos[i][1], cell_size, cell_size))
            # pygame.draw.rect(screen, body_inner, (snake_pos[i][0] + 1, snake_pos[i][1] + 1, cell_size - 2, cell_size - 2))
            # pygame.draw.rect(screen, body_outer, (snake_reverse_pos[i][0], snake_reverse_pos[i][1], cell_size, cell_size))
            # pygame.draw.rect(screen, body_inner, (snake_reverse_pos[i][0] + 1, snake_reverse_pos[i][1] + 1, cell_size - 2, cell_size - 2))
            govde = pygame.Rect(snake_pos[i][0], snake_pos[i][1], cell_size, cell_size)
            govdeResim = pygame.image.load('SNEAK2.png')
            screen.blit(govdeResim, govde)

            govdeTers = pygame.Rect(snake_reverse_pos[i][0], snake_reverse_pos[i][1], cell_size, cell_size)
            govdeTersResim =  pygame.image.load('SNEAK2.png')
            screen.blit(govdeTersResim, govdeTers)


        if head == 1:
            # pygame.draw.rect(screen, body_outer, (snake_pos[i][0], snake_pos[i][1], cell_size, cell_size))
            # pygame.draw.rect(screen, (255, 0, 0), (snake_pos[i][0] + 1, snake_pos[i][1] + 1, cell_size - 2, cell_size - 2))
            # pygame.draw.rect(screen, body_outer, (snake_reverse_pos[i][0], snake_reverse_pos[i][1], cell_size, cell_size))
            # pygame.draw.rect(screen, (255, 0, 0), (snake_reverse_pos[i][0] + 1, snake_reverse_pos[i][1] + 1, cell_size - 2, cell_size - 2))
            govde = pygame.Rect(snake_pos[i][0], snake_pos[i][1], cell_size, cell_size)
            govdeResim = pygame.image.load('SNEAK1.png')
            screen.blit(govdeResim, govde)

            govdeTers = pygame.Rect(snake_reverse_pos[i][0], snake_reverse_pos[i][1], cell_size, cell_size)
            govdeTersResim =  pygame.image.load('SNEAK1.png')
            screen.blit(govdeTersResim, govdeTers)
            head = 0

    pygame.display.update()

    update_snake += 1

pygame.quit()
