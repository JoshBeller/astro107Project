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
    pygame.display.set_caption("Level 5 - The Wormhole Generator")
    
    # Colors
    BLACK = (0, 0, 30)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    
    # Font
    font = pygame.font.Font(None, 36)
    speech_font = pygame.font.Font(None, 28)
    
    # Load Kip Thorne image
    thorne_img = pygame.image.load("thorne.png")  # Ensure the image exists
    thorne_img = pygame.transform.scale(thorne_img, (100, 100))
    
    # Introduction dialogue
    intro_dialogue = [
        "Kip Thorne: Welcome, traveler! You are about to explore the fascinating world of wormholes and spacetime warping!",
        "To escape, you must assemble the Wormhole Generator, a theoretical gateway through space and time.",
        "In Einstein’s relativity, spacetime can bend and fold—potentially creating shortcuts across the cosmos.",
        "Use the arrow keys to collect all the missing pieces of the generator.",
        "But beware! Gravitational distortions can throw you off course!"
    ]

    intro_index = 0
    show_puzzle = False
    game_completed = False
    
    # Player settings
    player = pygame.Rect(WIDTH // 2, HEIGHT - 50, 30, 30)
    player_speed = 5
    
    # Collectible components
    components = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 150), 20, 20) for _ in range(5)]
    collected_count = 0
    
    # Gravity Wells (hazards)
    gravity_wells = [pygame.Rect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200), 40, 40) for _ in range(3)]
    gravity_pull_strength = 2  # Strength of gravitational distortion
    
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
            screen.blit(thorne_img, (50, HEIGHT - 200))
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
            
            # Check for gravitational pull
            for well in gravity_wells:
                if player.colliderect(well):
                    player.x += random.choice([-gravity_pull_strength, gravity_pull_strength])
                    player.y += random.choice([-gravity_pull_strength, gravity_pull_strength])
            
            # Check for component collection
            for component in components[:]:
                if player.colliderect(component):
                    components.remove(component)
                    collected_count += 1
            
            # Check if all components are collected
            if collected_count == 5:
                game_completed = True
            
            # Draw gravity wells
            for well in gravity_wells:
                pygame.draw.rect(screen, RED, well)
            
            # Draw components
            for component in components:
                pygame.draw.rect(screen, YELLOW, component)
            
            # Draw player
            pygame.draw.rect(screen, GREEN, player)
        else:
            completion_text = [
                "Kip Thorne: Incredible work! The Wormhole Generator is complete!",
                "My research helped us understand how wormholes might function within Einstein’s General Relativity.",
                "Though we have yet to discover a stable, traversable wormhole, this concept could one day revolutionize interstellar travel!",
                "The secrets of the universe are yours to explore—who knows what lies beyond?",
                "Press ENTER to return to the main menu."
            ]
            
            screen.blit(thorne_img, (50, HEIGHT - 200))
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
