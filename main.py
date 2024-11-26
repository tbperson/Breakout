import pygame
import sys
import time

# Initialize Pygame and the audio mixer
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Basic Pygame Window")

# Variable to check if the game is running for the first time
first = True

# Set up the player
player_color = (255, 0, 0)
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

def intro():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("Breakout", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


# Function to check if the player has won the game
def check_win():
    all_destroyed = True
    for i in range(16):
        for j in range(8):
            if blocks[i][j][5] == 1:
                all_destroyed = False
                break
        if not all_destroyed:
            break

    if all_destroyed:
        # End the game and show a win message
        win()

# Function to win the game automatically
def win():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("You Win", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load("game_won.wav")
    pygame.mixer.music.play()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Function to lose the game automatically
def lose():
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("You Lose", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load("game_lost.wav")
    pygame.mixer.music.play()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# Function to control the game clock
def update_time():
    # Update the display title with the current time
    current_time = time.strftime("%H:%M:%S")
    pygame.display.set_caption(f"Breakout - Time: {current_time}")

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

def game_start():
    #Initial delay
    global first
    first = False
    time.sleep(2)
    
    # Starting music
    pygame.mixer.music.load("start_game.mp3")
    pygame.mixer.music.play()

    # Countdown
    draw_number("3")
    draw_number("2")
    draw_number("1")
    draw_number("Go!")
    

    # Start the background music
    pygame.mixer.music.load("background_music.mp3")
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
intro()

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

    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.left <= 0 or ball.right >= width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    if ball.bottom >= height:
        # End the game and show a lose message
        lose()

    # Check for collisions
    if ball.colliderect(pygame.Rect(player_x, player_y, player_width, player_length)):
        ball_speed_y = -ball_speed_y
    for i in range(16):
        for j in range(8):
            if blocks[i][j][5] == 1:
                if ball.colliderect(pygame.Rect(blocks[i][j][1], blocks[i][j][2], blocks[i][j][3], blocks[i][j][4])):
                    blocks[i][j][5] = 0
                    ball_speed_y = -ball_speed_y

                    # Check if all blocks are destroyed
                    check_win()

    update_time()
    draw_objects()

    # Update the display
    pygame.display.flip()

    # Add a 2 second grace period at the game starts to allow the player to get ready
    if first == True:
        game_start()

    # Limit the frame rate to 30 FPS
    clock.tick(30)

pygame.quit()
sys.exit()