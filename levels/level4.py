import pygame
import sys
import random

def wrap_text(text, font, max_width):
    """Splits text into multiple lines if it exceeds max_width."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)
    return lines

def run_level():
    pygame.init()
    
    # Screen settings
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level 4 - Ghez’s Galactic Map")
    
    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    
    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)
    
    # Load Andrea Ghez image
    ghez_img = pygame.image.load("ghez.png")  # Ensure the image exists
    ghez_img = pygame.transform.scale(ghez_img, (100, 100))
    
    # Introduction dialogue
    intro_dialogue = [
        "Andrea Ghez: Welcome, explorer!",
        "I study the stars orbiting the supermassive black hole in our galaxy.",
        "By tracking their movements, we map the unseen!",
        "Use arrow keys to navigate through the starfield.",
        "Find the correct path to the black hole!"
    ]
    intro_index = 0
    show_puzzle = False
    game_completed = False
    
    # Player settings
    player = pygame.Rect(WIDTH // 2, HEIGHT - 50, 30, 30)
    player_speed = 5
    
    # Star positions (maze-like navigation challenge)
    stars = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 150), 10, 10) for _ in range(10)]
    goal = pygame.Rect(WIDTH // 2, 50, 40, 40)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not show_puzzle:
                    if event.key == pygame.K_RETURN:
                        intro_index += 1
                        if intro_index >= len(intro_dialogue):
                            show_puzzle = True
                elif game_completed and event.key == pygame.K_RETURN:
                    return  # Exit to main menu
        
        if not show_puzzle:
            screen.blit(ghez_img, (50, HEIGHT - 200))
            speech_bubble = pygame.Rect(170, HEIGHT - 200, 500, 100)
            pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
            
            lines = wrap_text(intro_dialogue[intro_index], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                screen.blit(text_surface, (180, HEIGHT - 190 + i * 25))
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            screen.blit(instruction_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        elif not game_completed:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
                player.x += player_speed
            if keys[pygame.K_UP] and player.y > 0:
                player.y -= player_speed
            if keys[pygame.K_DOWN] and player.y < HEIGHT - player.height:
                player.y += player_speed
            
            # Check for goal
            if player.colliderect(goal):
                game_completed = True
            
            # Draw stars
            for star in stars:
                pygame.draw.rect(screen, YELLOW, star)
            
            # Draw goal
            pygame.draw.rect(screen, BLUE, goal)
            
            # Draw player
            pygame.draw.rect(screen, GREEN, player)
        else:
            completion_text = [
                "Well done! You've navigated the galactic map!",
                "Andrea Ghez’s research helped confirm the supermassive black hole at the Milky Way’s center.",
                "By mapping stellar orbits, we see the invisible!",
                "Press ENTER to return to the main menu."
            ]
            
            screen.blit(ghez_img, (50, HEIGHT - 200))
            speech_bubble = pygame.Rect(170, HEIGHT - 200, 500, 100)
            pygame.draw.rect(screen, WHITE, speech_bubble, border_radius=10)
            
            lines = wrap_text(completion_text[0], speech_font, 480)
            for i, line in enumerate(lines):
                text_surface = speech_font.render(line, True, BLACK)
                screen.blit(text_surface, (180, HEIGHT - 190 + i * 25))
            instruction_surface = font.render("Press ENTER to continue", True, WHITE)
            screen.blit(instruction_surface, (WIDTH // 2 - 100, HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run_level()
