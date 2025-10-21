import pygame
import sys
import time
import random

# Initialize Pygame and the audio mixer
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout Menu")

# Variable to check if the game is running for the first time
first = True
score = 0

# Set up the player
player_color = (255, 1, 0)
player_width = 60
player_length = 20
player_y = 580
player_x = 400
player_speed = 10

# Set up the blocks
blocks = []
block_width = 50
block_height = 30
spacing = 10

for i in range(16):
    row = []
    for j in range(8):
        x = i * (block_width + spacing)
        y = j * (block_height + spacing)
        row.append([(255, 0, 0), x, y, block_width, block_height, 1])
    blocks.append(row)

# Set up the ball
ball_color = (255, 255, 255)
ball_x = 400
ball_y = 350
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
ball = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
width, height = screen.get_size()

# Set up the clock
clock = pygame.time.Clock()

# Power-up variables
power_ups = []
power_up_chance = 0.2
shield_active = False
shield_duration = 0

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (0, 0, 255)
        self.speed = 5

    def fall(self):
        self.rect.y += self.speed

def intro():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("Breakout", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, 100))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    mode = show_menu()
    return mode

def show_menu():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    modes = ["Standard", "No Death", "Hard Mode", "Infinite", "Exit"]
    selected_mode = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_mode = (selected_mode - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    selected_mode = (selected_mode + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    if modes[selected_mode] == "Exit":
                        pygame.quit()
                        sys.exit()
                    else:
                        return modes[selected_mode]

        screen.fill((0, 0, 0))
        for i, mode in enumerate(modes):
            color = (255, 255, 255) if i == selected_mode else (100, 100, 100)
            text = font.render(mode, True, color)
            text_rect = text.get_rect(center=(width / 2, 200 + i * 40))
            screen.blit(text, text_rect)

        pygame.display.flip()

def choose_ball_color():
    font = pygame.font.Font(None, 20)
    screen.fill((0, 0, 0))
    balls = ["White", "Blue", "Green", "Red", "Yellow", "Purple", "Orange"]
    selected_ball = 0
    ball_color = (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_ball = (selected_ball - 1) % len(balls)
                elif event.key == pygame.K_DOWN:
                    selected_ball = (selected_ball + 1) % len(balls)
                elif event.key == pygame.K_RETURN:
                    if balls[selected_ball] == "Exit":
                        pygame.quit()
                        sys.exit()
                    else:
                        return ball_color
        screen.fill((0, 0, 0))

        if balls[selected_ball] == "White":
            ball_color = (255, 255, 255)
        elif balls[selected_ball] == "Blue":
            ball_color = (0, 0, 255)
        elif balls[selected_ball] == "Green":
            ball_color = (0, 255, 0)
        elif balls[selected_ball] == "Red":
            ball_color = (255, 0, 0)
        elif balls[selected_ball] == "Yellow":
            ball_color = (255, 255, 0)
        elif balls[selected_ball] == "Purple":
            ball_color = (128, 0, 128)
        elif balls[selected_ball] == "Orange":
            ball_color = (255, 165, 0)

        color = (255, 255, 255)

        font = pygame.font.Font(None, 60)
        text = font.render("Choose the color of the ball", True, color)
        text_rect = text.get_rect(center=(width / 2, height / 2 - 45))
        screen.blit(text, text_rect)

        up_arrow = font.render("^", True, color)
        up_arrow_rect = up_arrow.get_rect(center=(width / 2, height / 2 + 25))
        screen.blit(up_arrow, up_arrow_rect)

        down_arrow = font.render("v", True, color)
        down_arrow_rect = down_arrow.get_rect(center=(width / 2, height / 2 + 80))
        screen.blit(down_arrow, down_arrow_rect)

        pygame.draw.ellipse(screen, ball_color, ball)

        pygame.display.flip()

def choose_music_track():
    tracks = ["Track 1", "Track 2", "Track 3", "Track 4"]
    selected_track = 0
    music_track = "music/background_music1.mp3"

    pygame.mixer.music.load(music_track)
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_track = (selected_track - 1) % len(tracks)
                    music_track = track_selector(selected_track, tracks)
                    pygame.mixer.music.load(music_track)
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_DOWN:
                    selected_track = (selected_track + 1) % len(tracks)
                    music_track = track_selector(selected_track, tracks)
                    pygame.mixer.music.load(music_track)
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return music_track

        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 60)
        text = font.render("Choose the music track", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width / 2, height / 2 - 45))
        screen.blit(text, text_rect)

        for i, track in enumerate(tracks):
            color = (255, 255, 255) if i == selected_track else (100, 100, 100)
            text = font.render(track, True, color)
            text_rect = text.get_rect(center=(width / 2, height / 2 + i * 40))
            screen.blit(text, text_rect)

        pygame.display.flip()

def track_selector(selected_track, tracks):
    if tracks[selected_track] == "Track 1":
        music_track = "music/background_music1.mp3"
    elif tracks[selected_track] == "Track 2":
        music_track = "music/background_music2.mp3"
    elif tracks[selected_track] == "Track 3":
        music_track = "music/background_music3.mp3"
    elif tracks[selected_track] == "Track 4":
        music_track = "music/background_music4.mp3"
    return music_track

# Function to win the game
def win():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("You Win", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(width / 2, height / 2 + 100))
    screen.blit(score_text, score_rect)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load("music/game_won.wav")
    pygame.mixer.music.play()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Function to lose the game
def lose():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("You Lose", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(width / 2, height / 2 + 100))
    screen.blit(score_text, score_rect)
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load("music/game_lost.wav")
    pygame.mixer.music.play()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Function to control the game clock
def update_time():
    # Update the display title with the current time
    current_time = time.strftime("%H:%M:%S")
    pygame.display.set_caption(f"Breakout - {mode} - Time: {current_time} - Score: {score}")

def draw_objects():
    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw the player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_length))

    # Draw the blocks
    for i in range(16):
        for j in range(8):
            if blocks[i][j][5] == 1:
                pygame.draw.rect(screen, blocks[i][j][0], (blocks[i][j][1], blocks[i][j][2], blocks[i][j][3], blocks[i][j][4]))

    # Draw the ball
    pygame.draw.ellipse(screen, ball_color, ball)

    # Draw power-ups
    for power_up in power_ups:
        pygame.draw.rect(screen, power_up.color, power_up.rect)

    # Draw shield indicator
    if shield_active:
        pygame.draw.rect(screen, (0, 0, 255), (10, height - 30, 20, 20))

def game_start():
    # Initial delay
    global first
    first = False
    time.sleep(2)

    # Starting music
    pygame.mixer.music.load("music/start_game.mp3")
    pygame.mixer.music.play()

    # Countdown
    draw_number("3")
    draw_number("2")
    draw_number("1")
    draw_number("Go!")

    # Start the background music
    pygame.mixer.music.load(music_track)
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

def draw_number(number):
    font = pygame.font.Font(None, 74)
    text = font.render(number, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, 400))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000)
    draw_objects()

# Main game loop
running = True
mode = intro()
ball_color = choose_ball_color()
music_track = choose_music_track()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_width < 800:
        player_x += player_speed

    # Cheat codes
    if keys[pygame.K_q]:
        win()
    if keys[pygame.K_w]:
        lose()
    if keys[pygame.K_e]:
        player_speed = 20
    if keys[pygame.K_r]:
        player_width += 5

    if mode == "Hard Mode":
        if random.randint(0, 200) == 12:
            ball_speed_x = -ball_speed_x
        if random.randint(0, 200) == 24:
            ball_speed_y = -ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0 or ball.right >= width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    if ball.bottom >= height:
        if shield_active:
            ball_speed_y = -ball_speed_y
            shield_duration = 0
        elif mode != "No Death":
            # End the game and show a lose message
            lose()
        else:
            # Bounce the ball back up
            ball_speed_y = -ball_speed_y

    # Check for collisions
    if ball.colliderect(pygame.Rect(player_x, player_y, player_width, player_length)):
        ball_speed_y = -ball_speed_y
    for i in range(16):
        for j in range(8):
            if blocks[i][j][5] == 1:
                if ball.colliderect(pygame.Rect(blocks[i][j][1], blocks[i][j][2], blocks[i][j][3], blocks[i][j][4])):
                    ball_speed_y = -ball_speed_y
                    blocks[i][j][5] = 0
                    score += 1

                    # Check if all blocks are destroyed
                    if score == 112:
                        if mode == "Infinite":
                            pass
                        else:
                            win()

                    # Chance to drop a power-up
                    if random.random() < power_up_chance:
                        power_ups.append(PowerUp(blocks[i][j][1], blocks[i][j][2]))

    # Update power-ups
    for power_up in power_ups[:]:
        power_up.fall()
        if power_up.rect.colliderect(pygame.Rect(player_x, player_y, player_width, player_length)):
            power_ups.remove(power_up)
            shield_active = True
            shield_duration = pygame.time.get_ticks() + 20000  # 20 seconds

    # Check shield duration
    if shield_active and pygame.time.get_ticks() > shield_duration:
        shield_active = False

    update_time()
    draw_objects()

    # Draw shield timer
    if shield_active:
        pygame.draw.rect(screen, (0, 0, 255), (0, 590, 800, 10))
        remaining_time = (shield_duration - pygame.time.get_ticks()) // 1000
        font = pygame.font.Font(None, 20)
        timer_text = font.render(str(remaining_time), True, (255, 255, 255))
        screen.blit(timer_text, (10, height - 30))

    # Update the display
    pygame.display.flip()

    if first:
        game_start()

    # Limit the frame rate to 30 FPS
    clock.tick(30)

pygame.quit()
sys.exit()

