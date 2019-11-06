import random
import sys
import pygame
pygame.mixer.init()
pygame.init()

# Screen Variables
WIDTH = 500
HEIGHT = 500
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND = pygame.image.load('images/space.gif')
icon = pygame.image.load('images/RocketWhite.png')

# Music / Sound eff
music = pygame.mixer_music.load('MP/New_Moon.mp3')
pygame.mixer.music.play(-1)
shatter = pygame.mixer.Sound('MP/Shatter.wav')
# player data
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

# enemy data
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

# speed
SPEED = 10

# displays screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Foundation")
pygame.display.set_icon(icon)
# basic game variables
game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("Times New Roman", 35)


# Correlation between speed of enemy and score
def set_level(score, SPEED):
    if score < 20:
        SPEED = 7
    elif score < 40:
        SPEED = 10
    elif score < 60:
        SPEED = 16
    else:
        SPEED = score / 2 + 1
    return SPEED


# enemy drop rate / delay
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < .10:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


# renders enemy blocks
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


# updates enemy position
def update_enemy_postitions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if 0 <= enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


# Checks if collision occurred
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


# collision equation
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    shatter.play()
    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < (e_y + enemy_size)):
            return True
    return False


# Checks movement event when launched
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

    screen.blit(BACKGROUND, [0, 0])

    drop_enemies(enemy_list)
    score = update_enemy_postitions(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH - 175, HEIGHT - 40))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    # updates display
    pygame.display.update()
