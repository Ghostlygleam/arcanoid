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
text_win = font.render('Win!', True, (255, 255, 255))
text_win_rect = text_win.get_rect()
text_win_rect.center = (W // 2, H // 2)

# Timer for shrinking the paddle
shrink_timer = 0
shrink_interval = 5000  # Shrink paddle every 5 seconds
min_paddleW = 50

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(bg)
    
    # Draw paddle
    pygame.draw.rect(screen, pygame.Color(51, 25, 0), paddle)
    
    # Draw ball (as a circle)
    pygame.draw.circle(screen, pygame.Color(51, 25, 0), (ball.centerx, ball.centery), ballRadius)
    
    # Draw bricks
    for index, brick in enumerate(bricks + unbreakable_bricks + bonus_bricks):
        pygame.draw.rect(screen, brick_colors[index], brick)
    
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
        screen.fill((0, 0, 0))
        screen.blit(text_win, text_win_rect)
    
    # Check for game over
    if ball.y > H or ball.x > W:
        screen.fill((0, 0, 0))
        screen.blit(text_game_over, text_game_over_rect)
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
