import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Explorer")

# Load spaceship sprite (placeholder rectangle for now)
spaceship = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
spaceship_speed = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Boundaries
LEFT_BOUND, RIGHT_BOUND = 100, WIDTH - 100
TOP_BOUND, BOTTOM_BOUND = 100, HEIGHT - 100

# Tutorial text
font = pygame.font.Font(None, 36)
tutorial_text = [
    "Welcome, explorer!", 
    "Use W/A/S/D to move.", 
    "Find the first scientist to begin your journey."
]
tutorial_flash = True
flash_timer = 0

# Game loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and spaceship.y > TOP_BOUND:  # Move up
        spaceship.y -= spaceship_speed
    if keys[pygame.K_s] and spaceship.y < BOTTOM_BOUND - spaceship.height:  # Move down
        spaceship.y += spaceship_speed
    if keys[pygame.K_a] and spaceship.x > LEFT_BOUND:  # Move left
        spaceship.x -= spaceship_speed
    if keys[pygame.K_d] and spaceship.x < RIGHT_BOUND - spaceship.width:  # Move right
        spaceship.x += spaceship_speed
    
    # Draw spaceship (placeholder)
    pygame.draw.rect(screen, WHITE, spaceship)
    
    # Flashing tutorial text
    flash_timer += 1
    if (flash_timer // 30) % 2 == 0:  # Flash every 30 frames
        for i, line in enumerate(tutorial_text):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 30))
            screen.blit(text_surface, text_rect)
    
    # Update display
    pygame.display.flip()
    
    # Limit frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
