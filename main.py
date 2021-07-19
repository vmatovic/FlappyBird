import sys
import pygame
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 420))
    screen.blit(floor_surface, (floor_x_pos + 288, 420))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(350, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 420:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*4, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_b_r = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_b_r


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rec = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rec)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rec = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rec)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rec = high_score_surface.get_rect(center=(144, 380))
        screen.blit(high_score_surface, high_score_rec)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 30)

# Game variables
gravity = 0.175
bird_movement = 0
game_active = False
score = 0
high_score = 0

bg_surface = pygame.image.load('sprites/background-day.png').convert()

floor_surface = pygame.image.load('sprites/base.png').convert()
floor_x_pos = 0

# bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center=(100, 256))

bird_downflap = pygame.image.load('sprites/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('sprites/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
pipe_list = []
pipe_height = [200, 250, 325, 360]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_over_surface = pygame.image.load('sprites/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 220))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 256)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index = (bird_index+1) % 3
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
