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
ball = pygame.Rect(random.randrange(ballRadius, W - ballRadius), H // 2, ballRadius * 2, ballRadius * 2)
dx, dy = 1, -1

# Bricks setup
brickW = 50
brickH = 20
bricks = []
brick_cols = W // (brickW + 5)  # Number of bricks per row (50 width + 5 spacing)
for i in range(brick_cols):
    bricks.append(pygame.Rect(i * (brickW + 5) + 5, 50, brickW, brickH))

# Game over text
font = pygame.font.SysFont('comicsansms', 40)
text_game_over = font.render('Game Over', True, (255, 255, 255))
text_game_over_rect = text_game_over.get_rect()
text_game_over_rect.center = (W // 2, H // 2)

# Win text
text_win = font.render('Win!', True, (255, 255, 255))
text_win_rect = text_win.get_rect()
text_win_rect.center = (W // 2, H // 2)

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
    for brick in bricks:
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), brick)
    
    # Paddle control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddleSpeed
    if key[pygame.K_RIGHT] and paddle.right < W:
        paddle.right += paddleSpeed

    # Ball movement
    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

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
            bricks.remove(brick)
            dy = -dy
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
