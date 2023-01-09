import pygame
from random import randint
pygame.init()
pygame.mixer.init()

jump_v = pygame.mixer.Sound('jump.wav')
super_jump_v = pygame.mixer.Sound('jetpack.wav')

#lib
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128, 128, 128)
WIDHT = 400
HEIGHT = 500
RED = 255,36,0
#back = WHITE

player = pygame.transform.scale(pygame.image.load('doodle.png'), (70, 70))
FPS = 60
font = pygame.font.Font('Baskerville Bold italic.ttf', 26)
font2 = pygame.font.Font('Baskerville Bold italic.ttf', 16)
font3 = pygame.font.Font('Baskerville Bold italic.ttf', 20)
timer = pygame.time.Clock()

#game variables
player_x = 170
player_y = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 250, 70, 10], [85, 180, 70, 10], [265, 180, 70, 10], [175, 90, 70, 10], [85, 40, 70, 10], [265, 40, 70, 10]]
jump = False
y_change = 0
x_change = 0
player_speed = 3
score = 0
top_score = 0
game_over = False
space_jumps = 2
jump_last = 0
back = pygame.transform.scale(pygame.image.load('screen_image.jpg'), (400, 600))

#create screen
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption('Dooble Jump')

#check collisions
def check_collisions(rect_list, jump):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 20, player_y + 60, 35, 5]) and jump == False and y_change > 0:
            jump = True
    return jump
#upd player
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = 0.4
    if jump:
        jump_v.play()
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

# update platforms
def update_platforms(mylist, y_pos, change):
    global score
    if y_pos < 300 and change < 0:
        for i in range(len(mylist)):
            mylist[i][1] -= change
    else:
        pass
    for item in range(len(mylist)):
        if mylist[item][1] > 500:
            mylist[item] = [randint(10, 330), randint(-30, -10), 70, 10]
            score += 1
    return mylist
running = True
while running:
    timer.tick(FPS)
    screen.blit(back, (0,0))
    screen.blit(player, (player_x, player_y))
    blocks = []
    score_text = font.render(('SCORE: ' + str(score)), True, BLACK)
    screen.blit(score_text, (0,0))

    score_text = font2.render(('HIGH_SCORE: ' + str(top_score)), True, BLACK)
    screen.blit(score_text, (10, 30))

    space_text = font2.render(('Space jumpeds (spacebar) ' + str(space_jumps)), True, BLACK)
    screen.blit(space_text, (180, 0))
    if game_over:
        game_over_text = font3.render(('GAME OVER PRESS SPACEBAR'), True, RED, WHITE)
        screen.blit(game_over_text, (60, 190))

    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, BLACK, platforms[i], 0, 3)
        blocks.append(block)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                player_x = 170
                player_y = 400
                platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 250, 70, 10],
                             [85, 180, 70, 10], [265, 180, 70, 10], [175, 90, 70, 10], [85, 40, 70, 10],
                             [265, 40, 70, 10]]
                space_jumps = 2
                jump_last = 0
            elif event.key == pygame.K_SPACE and space_jumps > 0:
                super_jump_v.play()
                space_jumps -= 1
                y_change = -20
            if event.key == pygame.K_a:
                x_change = -player_speed
            if event.key == pygame.K_d:
                x_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_d:
                x_change = 0


    player_x += x_change
    player_y = update_player(player_y)
    platforms = update_platforms(platforms, player_y, y_change)
    jump = check_collisions(blocks, jump)
    if player_y < 100:
        platforms = update_platforms(platforms, player_y, y_change)
    if player_y < 80:
        platforms = update_platforms(platforms, player_y, y_change)

    if player_y > 440:
        game_over = True
        y_change = 0
        x_change = 0

    if score - jump_last > 50:
        jump_last = score
        space_jumps += 1

    if player_x < 0:
        player_x = 380

    if player_x > 400:
        player_x = 20

    if top_score < score:
        top_score = score

    if x_change < 0:
        player = pygame.transform.scale(pygame.image.load('doodle.png'), (70, 70))
    if x_change > 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('doodle.png'), (70, 70)), 1, 0)
    pygame.display.flip()
pygame.quit()