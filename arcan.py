import pygame
import random

pygame.init()

W, H = 800, 600
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (0, 255, 255)

# Player (paddle) setup
paddleW = 200
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball setup
ballRadius = 20
ballSpeed = 6
ballSpeedIncrease = 0.01  # Increment speed
ball = pygame.Rect(random.randrange(ballRadius, W - ballRadius), H // 2, ballRadius * 2, ballRadius * 2)
dx, dy = 1, -1

# Bricks setup
brickW = 50
brickH = 20
brick_cols = W // (brickW + 5)  # Number of bricks per row (50 width + 5 spacing)
brick_rows = 3  # Number of rows

bricks = []
brick_colors = []
unbreakable_bricks = []
bonus_bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * (brickW + 5) + 5
        brick_y = row * (brickH + 5) + 50
        brick = pygame.Rect(brick_x, brick_y, brickW, brickH)
        
        # Randomly assign some bricks as unbreakable and bonus bricks
        if random.random() < 0.1:  # 10% chance of being unbreakable
            unbreakable_bricks.append(brick)
            brick_colors.append((128, 128, 128))  # Grey for unbreakable bricks
        elif random.random() < 0.2:  # 20% chance of being a bonus brick
            bonus_bricks.append(brick)
            brick_colors.append((255, 255, 0))  # Yellow for bonus bricks
        else:
            bricks.append(brick)
            brick_colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

# Game over text
font = pygame.font.SysFont('comicsansms', 40)
text_game_over = font.render('Game Over', True, (255, 255, 255))
text_game_over_rect = text_game_over.get_rect()
text_game_over_rect.center = (W // 2, H // 2)

# Win text
text_win = font.render('You Win!', True, (255, 255, 255))
text_win_rect = text_win.get_rect()
text_win_rect.center = (W // 2, H // 2)

# Timer for shrinking the paddle
shrink_timer = 0
shrink_interval = 5000  # Shrink paddle every 5 seconds
min_paddleW = 50

# States
PLAYING = 1
PAUSED = 2
SETTINGS = 3
GAME_OVER = 4
WIN = 5
game_state = PLAYING

# Settings variables
ball_speed_settings = [4, 6, 8, 10]
current_ball_speed_index = 1

# Lives
lives = 3
font_lives = pygame.font.SysFont('comicsansms', 30)

def draw_menu():
    font = pygame.font.SysFont('comicsansms', 50)
    text_pause = font.render('Pause Menu', True, (255, 255, 255))
    text_pause_rect = text_pause.get_rect()
    text_pause_rect.center = (W // 2, H // 2 - 100)
    
    font_small = pygame.font.SysFont('comicsansms', 30)
    text_resume = font_small.render('Press R to Resume', True, (255, 255, 255))
    text_resume_rect = text_resume.get_rect()
    text_resume_rect.center = (W // 2, H // 2)
    
    text_settings = font_small.render('Press S for Settings', True, (255, 255, 255))
    text_settings_rect = text_settings.get_rect()
    text_settings_rect.center = (W // 2, H // 2 + 50)
    
    screen.blit(text_pause, text_pause_rect)
    screen.blit(text_resume, text_resume_rect)
    screen.blit(text_settings, text_settings_rect)

def draw_settings():
    font = pygame.font.SysFont('comicsansms', 50)
    text_settings = font.render('Settings', True, (255, 255, 255))
    text_settings_rect = text_settings.get_rect()
    text_settings_rect.center = (W // 2, H // 2 - 100)
    
    font_small = pygame.font.SysFont('comicsansms', 30)
    text_speed = font_small.render(f'Ball Speed: {ball_speed_settings[current_ball_speed_index]}', True, (255, 255, 255))
    text_speed_rect = text_speed.get_rect()
    text_speed_rect.center = (W // 2, H // 2)
    
    button_plus = pygame.Rect(W // 2 + 100, H // 2 - 15, 30, 30)
    button_minus = pygame.Rect(W // 2 - 130, H // 2 - 15, 30, 30)
    
    text_plus = font_small.render('+', True, (255, 255, 255))
    text_minus = font_small.render('-', True, (255, 255, 255))
    
    pygame.draw.rect(screen, (0, 255, 0), button_plus)
    pygame.draw.rect(screen, (255, 0, 0), button_minus)
    
    screen.blit(text_plus, (W // 2 + 105, H // 2 - 15))
    screen.blit(text_minus, (W // 2 - 125, H // 2 - 15))
    
    text_back = font_small.render('Press B to go back', True, (255, 255, 255))
    text_back_rect = text_back.get_rect()
    text_back_rect.center = (W // 2, H // 2 + 100)
    
    screen.blit(text_settings, text_settings_rect)
    screen.blit(text_speed, text_speed_rect)
    screen.blit(text_back, text_back_rect)
    
    return button_plus, button_minus

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == SETTINGS:
            mouse_pos = event.pos
            button_plus, button_minus = draw_settings()
            if button_plus.collidepoint(mouse_pos):
                current_ball_speed_index = (current_ball_speed_index + 1) % len(ball_speed_settings)
                ballSpeed = ball_speed_settings[current_ball_speed_index]
            elif button_minus.collidepoint(mouse_pos):
                current_ball_speed_index = (current_ball_speed_index - 1) % len(ball_speed_settings)
                ballSpeed = ball_speed_settings[current_ball_speed_index]

    if game_state == PLAYING:
        screen.fill(bg)
        
        # Draw paddle
        pygame.draw.rect(screen, pygame.Color(51, 25, 0), paddle)
        
        # Draw ball (as a circle)
        pygame.draw.circle(screen, pygame.Color(51, 25, 0), (ball.centerx, ball.centery), ballRadius)
        
        # Draw bricks
        for index, brick in enumerate(bricks + unbreakable_bricks + bonus_bricks):
            pygame.draw.rect(screen, brick_colors[index], brick)
        
        # Draw lives
        lives_text = font_lives.render(f'Lives: {lives}', True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))
        
        # Paddle control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddleSpeed
        if key[pygame.K_RIGHT] and paddle.right < W:
            paddle.right += paddleSpeed

        # Ball movement
        ball.x += ballSpeed * dx
        ball.y += ballSpeed * dy

        # Increase ball speed over time
        ballSpeed += ballSpeedIncrease

        # Shrink paddle over time
        shrink_timer += clock.get_time()
        if shrink_timer >= shrink_interval and paddle.width > min_paddleW:
            paddle.width -= 10
            paddle.x = max(0, min(W - paddle.width, paddle.x))
            shrink_timer = 0

        # Collision left or right 
        if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
            dx = -dx
        # Collision top
        if ball.centery < ballRadius: 
            dy = -dy
        # Collision with paddle
        if ball.colliderect(paddle) and dy > 0:
            dy = -dy
        
        # Collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                index = bricks.index(brick)
                bricks.remove(brick)
                brick_colors.pop(index)
                dy = -dy
                break

        # Collision with unbreakable bricks
        for brick in unbreakable_bricks:
            if ball.colliderect(brick):
                dy = -dy
                break
        
        # Collision with bonus bricks
        for brick in bonus_bricks[:]:
            if ball.colliderect(brick):
                index = bonus_bricks.index(brick)
                bonus_bricks.remove(brick)
                brick_colors.pop(len(bricks) + index)
                dy = -dy
                # Bonus: Increase paddle size
                paddle.width = min(paddle.width + 20, W)
                break
        
        # Check for win
        if not bricks:
            game_state = WIN
        
        # Check for game over
        if ball.y > H:
            lives -= 1
            if lives == 0:
                game_state = GAME_OVER
            else:
                ball.x = W // 2
                ball.y = H // 2
                dx, dy = 1, -1
        
        if key[pygame.K_p]:
            game_state = PAUSED
    
    elif game_state == PAUSED:
        screen.fill((0, 0, 0))
        draw_menu()
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            game_state = PLAYING
        elif key[pygame.K_s]:
            game_state = SETTINGS

    elif game_state == SETTINGS:
        screen.fill((0, 0, 0))
        button_plus, button_minus = draw_settings()
        key = pygame.key.get_pressed()
        if key[pygame.K_b]:
            game_state = PAUSED
    
    elif game_state == GAME_OVER:
        screen.fill((0, 0, 0))
        screen.blit(text_game_over, text_game_over_rect)
    
    elif game_state == WIN:
        screen.fill((0, 0, 0))
        screen.blit(text_win, text_win_rect)
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

