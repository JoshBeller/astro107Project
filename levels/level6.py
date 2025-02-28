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
    pygame.display.set_caption("Final Level - Beyond the Event Horizon")
    
    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)
    
    # Load Roger Penrose image
    penrose_img = pygame.image.load("penrose.png")  # Ensure the image exists
    penrose_img = pygame.transform.scale(penrose_img, (100, 100))
    
    # Introduction dialogue
    intro_dialogue = [
        "Roger Penrose: Welcome, traveler! You stand at the edge of the ultimate cosmic mystery—the singularity.",
        "This is your final test... Can you escape the inescapable?",
        "Inside a black hole, gravity warps spacetime so extremely that even light cannot escape.",
        "Navigate carefully through the chaotic distortions, where time and space behave in unexpected ways!",
        "Reach the wormhole exit before you cross the event horizon and are lost forever!"
    ]
    intro_index = 0
    show_puzzle = False
    game_completed = False
    
    # Player settings
    player = pygame.Rect(WIDTH // 2, HEIGHT - 50, 30, 30)
    player_speed = 5
    
    # Spacetime distortions (moving obstacles)
    distortions = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200), 40, 40) for _ in range(5)]
    distortion_speed = 2
    
    # Wormhole exit
    exit_portal = pygame.Rect(WIDTH // 2 - 25, 50, 50, 50)
    
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
                    return "game_completed"  # Trigger the ending sequence
        
        if not show_puzzle:
            screen.blit(penrose_img, (50, HEIGHT - 200))
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
            
            # Move distortions randomly
            for distortion in distortions:
                distortion.x += random.choice([-distortion_speed, distortion_speed])
                distortion.y += random.choice([-distortion_speed, distortion_speed])
            
            # Check for collisions
            for distortion in distortions:
                if player.colliderect(distortion):
                    player.x, player.y = WIDTH // 2, HEIGHT - 50  # Reset position if hit
            
            # Check if player reaches exit
            if player.colliderect(exit_portal):
                game_completed = True
            
            # Draw distortions
            for distortion in distortions:
                pygame.draw.rect(screen, RED, distortion)
            
            # Draw exit
            pygame.draw.rect(screen, BLUE, exit_portal)
            
            # Draw player
            pygame.draw.rect(screen, GREEN, player)
        else:
            completion_text = [
                "Roger Penrose: Remarkable! You have stabilized the wormhole and escaped beyond the event horizon!",
                "My work helped uncover the nature of singularities—regions of infinite density hidden within black holes.",
                "Understanding these extreme objects is key to unraveling the mysteries of gravity and quantum mechanics.",
                "You have ventured where few dare to imagine. What lies beyond remains an open question.",
                "Press ENTER to continue to the final reflection."
            ]
            
            screen.blit(penrose_img, (50, HEIGHT - 200))
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
